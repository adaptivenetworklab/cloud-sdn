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

import datetime
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0
import json
import websocket

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

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        start = datetime.datetime.now()
        print('_packet_in_handler start timestamp ', start)
        msg = ev.msg
        datapath = msg.datapath
        dpid = datapath.id

        packet = msg.to_jsondict()
        packet['dpid'] = dpid
        print('Packet ', packet)

        stop = datetime.datetime.now()
        time_diff = (stop - start)
        ex_time = time_diff.total_seconds() * 1000
        print('_packet_in_handler time ', ex_time)
        timestp = datetime.datetime.now()
        print('_packet_in_handler start requests.post ', timestp)
        ws = websocket.create_connection(left_ryu_app)
        json_data = json.dumps(packet)
        ws.send(json_data)
        ws.close()
        timestp = datetime.datetime.now()
        print('_packet_in_handler end timestamp ', timestp)