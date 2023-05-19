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

import requests
import datetime
import os
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0

#middle_ryu_app = "http://192.168.2.2:8090"
middle_ryu_app = "http://" + str(os.environ['MIDDLE_RYU_APP']) + ":8090"
middle_ryu_app_packetin = middle_ryu_app + "/packetin"
#middle_ryu_app_sf = middle_ryu_app + "/switch-features"

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

    # @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    # def switch_features_handler(self, ev):
    #     start = datetime.datetime.now()
    #     print('_packet_in_handler start timestamp ', start)
    #     msg = ev.msg
    #     datapath = msg.datapath
    #     dpid = datapath.id

    #     packet = msg.to_jsondict()
    #     packet['dpid'] = dpid
    #     print('Packet ', packet)

    #     stop = datetime.datetime.now()
    #     time_diff = (stop - start)
    #     ex_time = time_diff.total_seconds() * 1000
    #     print('_switch_features_handler time ', ex_time)
    #     timestp = datetime.datetime.now()
    #     print('_switch_features_handler start requests.post ', timestp)
    #     x = requests.post(middle_ryu_app_sf,json=packet)
    #     timestp = datetime.datetime.now()
    #     print('_switch_features_handler end timestamp ', timestp)

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
        x = requests.post(middle_ryu_app_packetin,json=packet)
        timestp = datetime.datetime.now()
        print('_packet_in_handler end timestamp ', timestp)
