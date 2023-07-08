# Copyright (C) 2014 Nippon Telegraph and Telephone Corporation.
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

"""
Usage example

Run this application:
$ PYTHONPATH=. ./bin/ryu run --verbose ryu.app.simple_switch_websocket_13

Install and run websocket client(in other terminal):
$ pip install websocket-client
$ wsdump.py ws://192.168.56.10/packetin

Send packet to dataplane:
> {"jsonrpc": "2.0", "id": 1, "method": "sendpacket", "params" : {"msg": "msg"}}
"""

from websocket import WebSocketApp
from ryu.base import app_manager
from ryu.app.wsgi import ControllerBase
from ryu.app.wsgi import rpc_public
from ryu.app.wsgi import websocket
from ryu.app.wsgi import WebSocketRPCServer
from ryu.app.wsgi import WSGIApplication
from ryu.controller import ofp_event
from ryu.controller.handler import set_ev_cls
from ryu.lib.packet import packet
from ryu.lib import ofctl_v1_0
import json
import time
import base64

simple_switch_instance_name = 'simple_switch_api_app'
url = '/packetin'


class MiddlewareWebSocket(app_manager.RyuApp):
    _CONTEXTS = {
        'wsgi': WSGIApplication,
    }

    def __init__(self, *args, **kwargs):
        super(MiddlewareWebSocket, self).__init__(*args, **kwargs)
        self.datapath_dict = {}
        self.ofctl = ofctl_v1_0
        wsgi = kwargs['wsgi']
        wsgi.register(
            MiddlewareWebSocketController,
            data={simple_switch_instance_name: self},
        )
        self._ws_manager = wsgi.websocketmanager

    def get_datapath_by_dpid(self, dpid):
        if dpid in self.datapath_dict:
            return self.datapath_dict[dpid]
        else:
            return None

    @set_ev_cls(ofp_event.EventOFPPacketIn)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        dpid = datapath.id
        self.datapath_dict[dpid] = datapath

        packet = msg.to_jsondict()
        packet['dpid'] = dpid
        print('Packet ', packet)
        json_data = json.dumps(packet)
        self._ws_manager.broadcast(str(json_data))

    @rpc_public
    def sendpacket(self, dpid, buffer_id, in_port, actions, data):
        # Parse the received JSON message
        datapath = self.get_datapath_by_dpid(dpid)
        processed_actions = None

        if actions[0]["type"] == "OUTPUT":
            out_port = actions[0]["port"]
            processed_actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]

        if (datapath is not None) and (processed_actions is not None):
            out = datapath.ofproto_parser.OFPPacketOut(
                datapath=datapath,
                buffer_id=buffer_id,
                in_port=in_port,
                actions=processed_actions,
                data=base64.b64decode(data),
            )
            datapath.send_msg(out)
            print("a packet was sent to dataplane")

        else:
            return "datapath or action undefined"
        
    @rpc_public
    def addflow(self, dpid, match, priority, actions):
        # Parse the received JSON message
        datapath = self.get_datapath_by_dpid(dpid)
        processed_actions = None

        if actions[0]["type"] == "OUTPUT":
            out_port = actions[0]["port"]
            processed_actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]

        if (datapath is not None) and (processed_actions is not None):
        # construct flow_mod message and send it.
            flow = datapath.ofproto_parser.OFPFlowMod(
                datapath=datapath,
                match=datapath.ofproto_parser.OFPMatch(**match),
                cookie=0,
                command=datapath.ofproto.OFPFC_ADD,
                idle_timeout=20,
                hard_timeout=120,
                priority=priority,
                flags=datapath.ofproto.OFPFF_SEND_FLOW_REM,
                actions=actions,
            )
            datapath.send_msg(flow)
            print("a flow was sent to dataplane")

        else:
            return "datapath or action undefined"
        
    def on_message(self, ws, message):
        self.sendpacket(message)

    def on_error(ws, error):
        print("Error:", error)

    def on_close(ws):
        print("Connection closed")

class MiddlewareWebSocketController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(MiddlewareWebSocketController, self).__init__(
            req, link, data, **config)
        self.simple_switch_app = data[simple_switch_instance_name]

    @websocket('packetin', url)
    def _websocket_handler(self, ws):
        simple_switch = self.simple_switch_app
        simple_switch.logger.debug('WebSocket connected: %s', ws)
        rpc_server = WebSocketRPCServer(ws, simple_switch)
        rpc_server.serve_forever()
        simple_switch.logger.debug('WebSocket disconnected: %s', ws)
