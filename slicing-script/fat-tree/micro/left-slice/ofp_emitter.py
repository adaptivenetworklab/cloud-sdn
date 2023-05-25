# Copyright (C) 2020 Daniel Barattini.
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

import websockets
import asyncio
import datetime
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.controller.controller import Datapath
from ryu.ofproto import ofproto_v1_0
import json

left_ryu_app = "ws://192.168.1.2:8090"

class OfpEmitter(app_manager.RyuApp):
    """Propagate events to interested microservices.

        packet format:

        {
            'OFPXXX' : {    //XXX = event name  (ex. OFPPacketIn)
                'buffer_id'     :   int
                'data'          :   str (base64 encoded)
                'in_port'       :   int
                'reason'        :   int
                'total_len'     :   int
            },
            'dpid' :    int
        }
    """

    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(OfpEmitter, self).__init__(*args, **kwargs)
        self.datapath_dict = {}

    def get_datapath_by_dpid(self, dpid):
        if dpid in self.datapath_dict:
            return self.datapath_dict[dpid]
        else:
            return None

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        start = datetime.datetime.now()
        print('_packet_in_handler start timestamp ', start)
        msg = ev.msg
        datapath = msg.datapath
        dpid = datapath.id
        self.datapath_dict[dpid] = datapath

        packet = msg.to_jsondict()
        packet['dpid'] = dpid
        print('Packet ', packet)

        stop = datetime.datetime.now()
        time_diff = (stop - start)
        ex_time = time_diff.total_seconds() * 1000
        print('_packet_in_handler time ', ex_time)
        timestp = datetime.datetime.now()
        print('_packet_in_handler start requests.post ', timestp)
        json_data = json.dumps(packet)

        async def send_ofp_msg_to_ryuapp(json_data):
            async with websockets.connect(left_ryu_app) as ws:
                await ws.send(json_data)

                while True:
                    try:
                        message = await ws.recv()
                    except websockets.ConnectionClosedOk:
                        break
                    print(message)
                    msg = json.loads(message)
                    datapath = self.get_datapath_by_dpid(msg['dpid'])

                    if msg['type'] is 'PacketOut':
                        actions = []
                        for act in msg['actions']:
                            actions.append(datapath.ofproto_parser.OFPActionOutput(act['port']))
                        ofproto = datapath.ofproto
                        data = None
                        if msg['buffer_id'] == ofproto.OFP_NO_BUFFER:
                            data = msg['data']

                        out = datapath.ofproto_parser.OFPPacketOut(
                            datapath=datapath,
                            buffer_id=msg['buffer_id'],
                            in_port=msg['in_port'],
                            actions=actions,
                            data=data,
                        )
                        datapath.send_msg(out)

                    elif msg['type'] is 'FlowMod':
                        actions = []
                        for act in msg['actions']:
                            actions.append(datapath.ofproto_parser.OFPActionOutput(act['port']))
                        ofproto = datapath.ofproto
                        parser = datapath.ofproto_parser

                        # construct flow_mod message and send it.
                        mod = parser.OFPFlowMod(
                            datapath=datapath,
                            match=msg['match'],
                            cookie=0,
                            command=ofproto.OFPFC_ADD,
                            idle_timeout=20,
                            hard_timeout=120,
                            priority=msg['priority'],
                            flags=ofproto.OFPFF_SEND_FLOW_REM,
                            actions=actions,
                        )
                        datapath.send_msg(mod)

        asyncio.run(send_ofp_msg_to_ryuapp(json_data))        

        timestp = datetime.datetime.now()
        print('_packet_in_handler end timestamp ', timestp)