# Copyright (C) 2020 Daniel Barattini.
# Copyright (C) 2012 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import json
import ast
import base64
import datetime

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller import dpset
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.exception import RyuException
from ryu.ofproto import ofproto_v1_0
from ryu.ofproto import ofproto_v1_2
from ryu.ofproto import ofproto_v1_3
from ryu.ofproto import ofproto_v1_4
from ryu.ofproto import ofproto_v1_5
from ryu.lib import ofctl_v1_0
from ryu.lib import ofctl_v1_2
from ryu.lib import ofctl_v1_3
from ryu.lib import ofctl_v1_4
from ryu.lib import ofctl_v1_5
from ryu.app.wsgi import ControllerBase
from ryu.app.wsgi import Response
from ryu.app.wsgi import WSGIApplication
from ryu.app.wsgi import websocket
from wsgiref.simple_server import make_server
from wsgiref.util import setup_testing_defaults
from ryu.app.wsgi import WebSocketRPCServer
from ryu.app.wsgi import WebSocketRPCClient
import json

LOG = logging.getLogger('ryu.app.ofctl_rest')

# supported ofctl versions in this restful app
supported_ofctl = {
    ofproto_v1_0.OFP_VERSION: ofctl_v1_0,
    ofproto_v1_2.OFP_VERSION: ofctl_v1_2,
    ofproto_v1_3.OFP_VERSION: ofctl_v1_3,
    ofproto_v1_4.OFP_VERSION: ofctl_v1_4,
    ofproto_v1_5.OFP_VERSION: ofctl_v1_5,
}

# REST API
#

# Retrieve the switch stats
#
# get the list of all switches
# GET /stats/switches
#
# get the desc stats of the switch
# GET /stats/desc/<dpid>
#
# get flows desc stats of the switch
# GET /stats/flowdesc/<dpid>
#
# get flows desc stats of the switch filtered by the fields
# POST /stats/flowdesc/<dpid>
#
# get flows stats of the switch
# GET /stats/flow/<dpid>
#
# get flows stats of the switch filtered by the fields
# POST /stats/flow/<dpid>
#
# get aggregate flows stats of the switch
# GET /stats/aggregateflow/<dpid>
#
# get aggregate flows stats of the switch filtered by the fields
# POST /stats/aggregateflow/<dpid>
#
# get table stats of the switch
# GET /stats/table/<dpid>
#
# get table features stats of the switch
# GET /stats/tablefeatures/<dpid>
#
# get ports stats of the switch
# GET /stats/port/<dpid>[/<port>]
# Note: Specification of port number is optional
#
# get queues stats of the switch
# GET /stats/queue/<dpid>[/<port>[/<queue_id>]]
# Note: Specification of port number and queue id are optional
#       If you want to omitting the port number and setting the queue id,
#       please specify the keyword "ALL" to the port number
#       e.g. GET /stats/queue/1/ALL/1
#
# get queues config stats of the switch
# GET /stats/queueconfig/<dpid>[/<port>]
# Note: Specification of port number is optional
#
# get queues desc stats of the switch
# GET /stats/queuedesc/<dpid>[/<port>[/<queue_id>]]
# Note: Specification of port number and queue id are optional
#       If you want to omitting the port number and setting the queue id,
#       please specify the keyword "ALL" to the port number
#       e.g. GET /stats/queuedesc/1/ALL/1
#
# get meter features stats of the switch
# GET /stats/meterfeatures/<dpid>
#
# get meter config stats of the switch
# GET /stats/meterconfig/<dpid>[/<meter_id>]
# Note: Specification of meter id is optional
#
# get meter desc stats of the switch
# GET /stats/meterdesc/<dpid>[/<meter_id>]
# Note: Specification of meter id is optional
#
# get meters stats of the switch
# GET /stats/meter/<dpid>[/<meter_id>]
# Note: Specification of meter id is optional
#
# get group features stats of the switch
# GET /stats/groupfeatures/<dpid>
#
# get groups desc stats of the switch
# GET /stats/groupdesc/<dpid>[/<group_id>]
# Note: Specification of group id is optional (OpenFlow 1.5 or later)
#
# get groups stats of the switch
# GET /stats/group/<dpid>[/<group_id>]
# Note: Specification of group id is optional
#
# get ports description of the switch
# GET /stats/portdesc/<dpid>[/<port_no>]
# Note: Specification of port number is optional (OpenFlow 1.5 or later)

# Update the switch stats
#
# add a flow entry
# POST /stats/flowentry/add
#
# modify all matching flow entries
# POST /stats/flowentry/modify
#
# modify flow entry strictly matching wildcards and priority
# POST /stats/flowentry/modify_strict
#
# delete all matching flow entries
# POST /stats/flowentry/delete
#
# delete flow entry strictly matching wildcards and priority
# POST /stats/flowentry/delete_strict
#
# delete all flow entries of the switch
# DELETE /stats/flowentry/clear/<dpid>
#
# add a meter entry
# POST /stats/meterentry/add
#
# modify a meter entry
# POST /stats/meterentry/modify
#
# delete a meter entry
# POST /stats/meterentry/delete
#
# add a group entry
# POST /stats/groupentry/add
#
# modify a group entry
# POST /stats/groupentry/modify
#
# delete a group entry
# POST /stats/groupentry/delete
#
# modify behavior of the physical port
# POST /stats/portdesc/modify
#
# modify role of controller
# POST /stats/role
#
#
# send a experimeter message
# POST /stats/experimenter/<dpid>
#
# send a packet to a switch
# POST /stats/sendpacket


class CommandNotFoundError(RyuException):
    message = 'No such command : %(cmd)s'


class PortNotFoundError(RyuException):
    message = 'No such port info: %(port_no)s'


def stats_method(method):
    def wrapper(self, req, dpid, *args, **kwargs):
        # Get datapath instance from DPSet
        try:
            dp = self.dpset.get(int(str(dpid), 0))
        except ValueError:
            LOG.exception('Invalid dpid: %s', dpid)
            return Response(status=400)
        if dp is None:
            LOG.error('No such Datapath: %s', dpid)
            return Response(status=404)

        # Get lib/ofctl_* module
        try:
            ofctl = supported_ofctl.get(dp.ofproto.OFP_VERSION)
        except KeyError:
            LOG.exception('Unsupported OF version: %s',
                          dp.ofproto.OFP_VERSION)
            return Response(status=501)

        # Invoke StatsController method
        try:
            ret = method(self, req, dp, ofctl, *args, **kwargs)
            return Response(content_type='application/json',
                            body=json.dumps(ret))
        except ValueError:
            LOG.exception('Invalid syntax: %s', req.body)
            return Response(status=400)
        except AttributeError:
            LOG.exception('Unsupported OF request in this version: %s',
                          dp.ofproto.OFP_VERSION)
            return Response(status=501)

    return wrapper


def command_method(method):
    def wrapper(self, req, *args, **kwargs):
        # Parse request json body
        try:
            if req.body:
                # We use ast.literal_eval() to parse request json body
                # instead of json.loads().
                # Because we need to parse binary format body
                # in send_experimenter().
                body = ast.literal_eval(req.body.decode('utf-8'))
            else:
                body = {}
        except SyntaxError:
            LOG.exception('Invalid syntax: %s', req.body)
            return Response(status=400)

        # Get datapath_id from request parameters
        dpid = body.get('dpid', None)
        if not dpid:
            try:
                dpid = kwargs.pop('dpid')
            except KeyError:
                LOG.exception('Cannot get dpid from request parameters')
                return Response(status=400)

        # Get datapath instance from DPSet
        try:
            dp = self.dpset.get(int(str(dpid), 0))
        except ValueError:
            LOG.exception('Invalid dpid: %s', dpid)
            return Response(status=400)
        if dp is None:
            LOG.error('No such Datapath: %s', dpid)
            return Response(status=404)

        # Get lib/ofctl_* module
        try:
            ofctl = supported_ofctl.get(dp.ofproto.OFP_VERSION)
        except KeyError:
            LOG.exception('Unsupported OF version: version=%s',
                          dp.ofproto.OFP_VERSION)
            return Response(status=501)

        # Invoke StatsController method
        try:
            method(self, req, dp, ofctl, body, *args, **kwargs)
            return Response(status=200)
        except ValueError:
            LOG.exception('Invalid syntax: %s', req.body)
            return Response(status=400)
        except AttributeError:
            LOG.exception('Unsupported OF request in this version: %s',
                          dp.ofproto.OFP_VERSION)
            return Response(status=501)
        except CommandNotFoundError as e:
            LOG.exception(e.message)
            return Response(status=404)
        except PortNotFoundError as e:
            LOG.exception(e.message)
            return Response(status=404)

    return wrapper


class StatsController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(StatsController, self).__init__(req, link, data, **config)
        self.app = data['app']
        self.dpset = data['dpset']
        self.waiters = data['waiters']
        self.websocket_connections = []
    
    @websocket('root', '/')
    def websocket_handler(self, ws):
        self.websocket_connections.append(ws)
        try:
            while True:
                msg = ws.receive()
                if msg is None:
                    break
                self.handle_message(msg)
        finally:
            self.websocket_connections.remove(ws)

    def handle_message(self, message):
        # Handle incoming WebSocket message
        parsed_message = json.loads(message)
        # Process the message and send a response back if needed
        req = self.req
        dpid = parsed_message['dpid']
        dp = self.dpset.get(dpid=dpid)
        ofctl = self.app_manager.get_app('ofctl_rest')
        body = parsed_message
        
        # Call the send_packet function with the required arguments
        self.send_packet(req, dp, ofctl, body)

    def get_dpids(self, req, **_kwargs):
        dps = list(self.dpset.dps.keys())
        body = json.dumps(dps)
        return Response(content_type='application/json', body=body)

    @stats_method
    def get_desc_stats(self, req, dp, ofctl, **kwargs):
        return ofctl.get_desc_stats(dp, self.waiters)

    @stats_method
    def get_flow_desc(self, req, dp, ofctl, **kwargs):
        flow = req.json if req.body else {}
        return ofctl.get_flow_desc(dp, self.waiters, flow)

    @stats_method
    def get_flow_stats(self, req, dp, ofctl, **kwargs):
        flow = req.json if req.body else {}
        return ofctl.get_flow_stats(dp, self.waiters, flow)

    @stats_method
    def get_aggregate_flow_stats(self, req, dp, ofctl, **kwargs):
        flow = req.json if req.body else {}
        return ofctl.get_aggregate_flow_stats(dp, self.waiters, flow)

    @stats_method
    def get_table_stats(self, req, dp, ofctl, **kwargs):
        return ofctl.get_table_stats(dp, self.waiters)

    @stats_method
    def get_table_features(self, req, dp, ofctl, **kwargs):
        return ofctl.get_table_features(dp, self.waiters)

    @stats_method
    def get_port_stats(self, req, dp, ofctl, port=None, **kwargs):
        if port == "ALL":
            port = None

        return ofctl.get_port_stats(dp, self.waiters, port)

    @stats_method
    def get_queue_stats(self, req, dp, ofctl,
                        port=None, queue_id=None, **kwargs):
        if port == "ALL":
            port = None

        if queue_id == "ALL":
            queue_id = None

        return ofctl.get_queue_stats(dp, self.waiters, port, queue_id)

    @stats_method
    def get_queue_config(self, req, dp, ofctl, port=None, **kwargs):
        if port == "ALL":
            port = None

        return ofctl.get_queue_config(dp, self.waiters, port)

    @stats_method
    def get_queue_desc(self, req, dp, ofctl,
                       port=None, queue=None, **_kwargs):
        if port == "ALL":
            port = None

        if queue == "ALL":
            queue = None

        return ofctl.get_queue_desc(dp, self.waiters, port, queue)

    @stats_method
    def get_meter_features(self, req, dp, ofctl, **kwargs):
        return ofctl.get_meter_features(dp, self.waiters)

    @stats_method
    def get_meter_config(self, req, dp, ofctl, meter_id=None, **kwargs):
        if meter_id == "ALL":
            meter_id = None

        return ofctl.get_meter_config(dp, self.waiters, meter_id)

    @stats_method
    def get_meter_desc(self, req, dp, ofctl, meter_id=None, **kwargs):
        if meter_id == "ALL":
            meter_id = None

        return ofctl.get_meter_desc(dp, self.waiters, meter_id)

    @stats_method
    def get_meter_stats(self, req, dp, ofctl, meter_id=None, **kwargs):
        if meter_id == "ALL":
            meter_id = None

        return ofctl.get_meter_stats(dp, self.waiters, meter_id)

    @stats_method
    def get_group_features(self, req, dp, ofctl, **kwargs):
        return ofctl.get_group_features(dp, self.waiters)

    @stats_method
    def get_group_desc(self, req, dp, ofctl, group_id=None, **kwargs):
        if dp.ofproto.OFP_VERSION < ofproto_v1_5.OFP_VERSION:
            return ofctl.get_group_desc(dp, self.waiters)
        else:
            return ofctl.get_group_desc(dp, self.waiters, group_id)

    @stats_method
    def get_group_stats(self, req, dp, ofctl, group_id=None, **kwargs):
        if group_id == "ALL":
            group_id = None

        return ofctl.get_group_stats(dp, self.waiters, group_id)

    @stats_method
    def get_port_desc(self, req, dp, ofctl, port_no=None, **kwargs):
        if dp.ofproto.OFP_VERSION < ofproto_v1_5.OFP_VERSION:
            return ofctl.get_port_desc(dp, self.waiters)
        else:
            return ofctl.get_port_desc(dp, self.waiters, port_no)

    @stats_method
    def get_role(self, req, dp, ofctl, **kwargs):
        return ofctl.get_role(dp, self.waiters)

    @command_method
    def mod_flow_entry(self, req, dp, ofctl, flow, cmd, **kwargs):
        cmd_convert = {
            'add': dp.ofproto.OFPFC_ADD,
            'modify': dp.ofproto.OFPFC_MODIFY,
            'modify_strict': dp.ofproto.OFPFC_MODIFY_STRICT,
            'delete': dp.ofproto.OFPFC_DELETE,
            'delete_strict': dp.ofproto.OFPFC_DELETE_STRICT,
        }
        mod_cmd = cmd_convert.get(cmd, None)
        if mod_cmd is None:
            raise CommandNotFoundError(cmd=cmd)

        ofctl.mod_flow_entry(dp, flow, mod_cmd)

    @command_method
    def delete_flow_entry(self, req, dp, ofctl, flow, **kwargs):
        if ofproto_v1_0.OFP_VERSION == dp.ofproto.OFP_VERSION:
            flow = {}
        else:
            flow = {'table_id': dp.ofproto.OFPTT_ALL}

        ofctl.mod_flow_entry(dp, flow, dp.ofproto.OFPFC_DELETE)

    @command_method
    def mod_meter_entry(self, req, dp, ofctl, meter, cmd, **kwargs):
        cmd_convert = {
            'add': dp.ofproto.OFPMC_ADD,
            'modify': dp.ofproto.OFPMC_MODIFY,
            'delete': dp.ofproto.OFPMC_DELETE,
        }
        mod_cmd = cmd_convert.get(cmd, None)
        if mod_cmd is None:
            raise CommandNotFoundError(cmd=cmd)

        ofctl.mod_meter_entry(dp, meter, mod_cmd)

    @command_method
    def mod_group_entry(self, req, dp, ofctl, group, cmd, **kwargs):
        cmd_convert = {
            'add': dp.ofproto.OFPGC_ADD,
            'modify': dp.ofproto.OFPGC_MODIFY,
            'delete': dp.ofproto.OFPGC_DELETE,
        }
        mod_cmd = cmd_convert.get(cmd, None)
        if mod_cmd is None:
            raise CommandNotFoundError(cmd=cmd)

        ofctl.mod_group_entry(dp, group, mod_cmd)

    @command_method
    def mod_port_behavior(self, req, dp, ofctl, port_config, cmd, **kwargs):
        port_no = port_config.get('port_no', None)
        port_no = int(str(port_no), 0)

        port_info = self.dpset.port_state[int(dp.id)].get(port_no)
        if port_info:
            port_config.setdefault('hw_addr', port_info.hw_addr)
            if dp.ofproto.OFP_VERSION < ofproto_v1_4.OFP_VERSION:
                port_config.setdefault('advertise', port_info.advertised)
            else:
                port_config.setdefault('properties', port_info.properties)
        else:
            raise PortNotFoundError(port_no=port_no)

        if cmd != 'modify':
            raise CommandNotFoundError(cmd=cmd)

        ofctl.mod_port_behavior(dp, port_config)

    @command_method
    def send_experimenter(self, req, dp, ofctl, exp, **kwargs):
        ofctl.send_experimenter(dp, exp)

    @command_method
    def set_role(self, req, dp, ofctl, role, **kwargs):
        ofctl.set_role(dp, role)

    def send_packet(self, req, dp, ofctl, body, *args, **kwargs):
        #TODO ofctl.send_packet(dp, body)

        start = datetime.datetime.now()
        print('OFCTL_REST send_packet start timestamp ', start)

        buffer_id = ofctl.UTIL.ofp_buffer_from_user(
            body.get('buffer_id', dp.ofproto.OFP_NO_BUFFER))
        actions = ofctl.to_actions(dp, body.get('actions', []))
        in_port = ofctl.UTIL.ofp_port_from_user(body.get('in_port', None))

        out = dp.ofproto_parser.OFPPacketOut(
            datapath=dp, buffer_id=buffer_id, in_port=in_port,
            actions=actions, data=base64.b64decode(body.get('data')))

        dp.send_msg(out)
        stop = datetime.datetime.now()
        time_diff = (stop - start)
        ex_time = time_diff.total_seconds() * 1000
        print('OFCTL_REST send_packet ex_time ', ex_time)
        print('OFCTL_REST send_packet stop timestamp ', stop)

class WsStatsApi(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION,
                    ofproto_v1_2.OFP_VERSION,
                    ofproto_v1_3.OFP_VERSION,
                    ofproto_v1_4.OFP_VERSION,
                    ofproto_v1_5.OFP_VERSION]
    _CONTEXTS = {
        'wsgi': WSGIApplication,
        'dpset': dpset.DPSet,
    }

    def __init__(self, *args, **kwargs):
        super(WsStatsApi, self).__init__(*args, **kwargs)
        self.app = StatsController.__name__
        wsgi = kwargs['wsgi']
        self.waiters = {}
        self.data = {}
        self.dpset = kwargs['dpset']
        self.data['waiters'] = self.waiters
        wsgi.register(StatsController, {'app': self, 'dpset': dpset})

    @set_ev_cls([ofp_event.EventOFPStatsReply,
                 ofp_event.EventOFPDescStatsReply,
                 ofp_event.EventOFPFlowStatsReply,
                 ofp_event.EventOFPAggregateStatsReply,
                 ofp_event.EventOFPTableStatsReply,
                 ofp_event.EventOFPTableFeaturesStatsReply,
                 ofp_event.EventOFPPortStatsReply,
                 ofp_event.EventOFPQueueStatsReply,
                 ofp_event.EventOFPQueueDescStatsReply,
                 ofp_event.EventOFPMeterStatsReply,
                 ofp_event.EventOFPMeterFeaturesStatsReply,
                 ofp_event.EventOFPMeterConfigStatsReply,
                 ofp_event.EventOFPGroupStatsReply,
                 ofp_event.EventOFPGroupFeaturesStatsReply,
                 ofp_event.EventOFPGroupDescStatsReply,
                 ofp_event.EventOFPPortDescStatsReply
                 ], MAIN_DISPATCHER)
    def stats_reply_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath

        if dp.id not in self.waiters:
            return
        if msg.xid not in self.waiters[dp.id]:
            return
        lock, msgs = self.waiters[dp.id][msg.xid]
        msgs.append(msg)

        flags = 0
        if dp.ofproto.OFP_VERSION == ofproto_v1_0.OFP_VERSION:
            flags = dp.ofproto.OFPSF_REPLY_MORE
        elif dp.ofproto.OFP_VERSION == ofproto_v1_2.OFP_VERSION:
            flags = dp.ofproto.OFPSF_REPLY_MORE
        elif dp.ofproto.OFP_VERSION >= ofproto_v1_3.OFP_VERSION:
            flags = dp.ofproto.OFPMPF_REPLY_MORE

        if msg.flags & flags:
            return
        del self.waiters[dp.id][msg.xid]
        lock.set()

    @set_ev_cls([ofp_event.EventOFPSwitchFeatures,
                 ofp_event.EventOFPQueueGetConfigReply,
                 ofp_event.EventOFPRoleReply,
                 ], MAIN_DISPATCHER)
    def features_reply_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath

        if dp.id not in self.waiters:
            return
        if msg.xid not in self.waiters[dp.id]:
            return
        lock, msgs = self.waiters[dp.id][msg.xid]
        msgs.append(msg)

        del self.waiters[dp.id][msg.xid]
        lock.set()

app_manager.require_app('ryu.app.ofctl_rest')