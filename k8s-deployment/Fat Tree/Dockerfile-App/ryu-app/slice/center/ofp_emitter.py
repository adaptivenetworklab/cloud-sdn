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
import os
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0
import json

<<<<<<< HEAD:slicing-script/fat-tree/micro/right-slice/ofp_emitter.py
right_ryu_app = "ws://192.168.3.2:8090/packetin"
=======
#center_ryu_app = "http://172.17.0.3:8090/packetin"
center_ryu_app = "http://" + str(os.environ['CENTER_RYU_APP']) + ":8090/packetin"
>>>>>>> fbec69869ed959e0936020ebb1b7d55e27bbe4ee:k8s-deployment/Fat Tree/Dockerfile-App/ryu-app/slice/center/ofp_emitter.py

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
<<<<<<< HEAD:slicing-script/fat-tree/micro/right-slice/ofp_emitter.py
        json_data = json.dumps(packet)

        async def send_ofp_msg_to_ryuapp(json_data):
            async with websockets.connect(right_ryu_app) as ws:
                await ws.send(json_data)
                print(json_data)

        asyncio.run(send_ofp_msg_to_ryuapp(json_data))      

=======
        x = requests.post(center_ryu_app,json=packet)
>>>>>>> fbec69869ed959e0936020ebb1b7d55e27bbe4ee:k8s-deployment/Fat Tree/Dockerfile-App/ryu-app/slice/center/ofp_emitter.py
        timestp = datetime.datetime.now()
        print('_packet_in_handler end timestamp ', timestp)
