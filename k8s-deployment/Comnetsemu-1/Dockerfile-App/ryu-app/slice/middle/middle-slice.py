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

from flask import Flask, request, abort
from lib.packet import packet
from lib.packet import ethernet
from lib.packet import ether_types
import requests
import base64
import datetime
import os

api = Flask(__name__)

#TODO import from ofp
OFPP_FLOOD = 0xfffb
OFPFF_SEND_FLOW_REM = 1 << 0
OFP_NO_BUFFER = 0xffffffff

#RYU_BASE_URL = "http://192.168.2.1:8080"
RYU_BASE_URL = "http://" + str(os.environ['MIDDLE_MIDDLEWARE']) + ":8080"
middle_ryu_app = os.environ['MIDDLE_RYU_APP']

# out_port = slice_to_port[dpid][in_port]
slice_to_port = {
    2: {3: 1, 1: 3},
    4: {2: 4, 4: 2},
    7: {1: 3, 3: 1},
}

def build_flow(dpid, priority, match, actions):
    "Build and return a flow entry based on https://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#add-a-flow-entry"

    flow = {
        'dpid' : dpid,
        'match' : match,
        'cookie' : 0,
        'idle_timeout' : 20,
        'hard_timeout' : 120,
        'priority' : priority,
        'flags' : 1,
        'actions': actions,
    }

    return flow

def add_flow(flow):
    "Add a flow entry through REST"
    rest_uri = RYU_BASE_URL + "/stats/flowentry/add"

    #TODO verbose mode
    print("sending {}".format(flow))

    r = requests.post(rest_uri, json=flow)

    if r.status_code == 200:
        return True
    else:
        return False

def build_packet(data, dpid, in_port, actions, buffer_id):
    "Build and return a packet"
    pkt = {
        'dpid' : dpid,
        'buffer_id': buffer_id,
        'in_port' : in_port,
        'actions': actions,
        'data' : data
    }

    return pkt

def send_packet(pkt):
    "Send a packet to a switch through REST"
    rest_uri = RYU_BASE_URL + "/stats/sendpacket"

    start1 = datetime.datetime.now()
    print('send_packet start timestamp', start1)
    
    r = requests.post(rest_uri, json=pkt)

    if r.status_code == 200:
        return True
    else:
        return False

def extract_data(msg, event_name):
    data = msg[event_name]

    data['dpid'] = msg['dpid']

    if event_name is 'OFPPacketIn':
        data['encoded_data'] = data['data']
        data['data'] = base64.b64decode(data['encoded_data'])

        packet_data = packet.Packet(data['data'])
        eth = packet_data.get_protocol(ethernet.ethernet)

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            data['is_lldp'] = True
        else:
            data['is_lldp'] = False

            data['dst'] = eth.dst
            data['src'] = eth.src

    return data

@api.route('/')
def index():
    return 'Middle Slice Rest Server'

@api.route('/packetin', methods=['POST'])
def post_packetin():
    start1 = datetime.datetime.now()
    print('post_packetin start timestamp', start1)
    
    if not request.json:
        abort(400)

    start2 = datetime.datetime.now()
    data = extract_data(request.json, "OFPPacketIn")
    stop2 = datetime.datetime.now()
    time_diff = (stop2 - start2)
    ex_time = time_diff.total_seconds() * 1000
    print('extract_data: ', ex_time)

    if data['is_lldp']:
        # ignore lldp packet
        #TODO maybe server side
        return

    dpid = data['dpid']
    in_port = data['in_port']
    buffer_id = data['buffer_id']
    encoded_data = data['encoded_data']

    pkt = packet.Packet(data['data'])

    out_port = slice_to_port[dpid][in_port]

    # match = {'in_port': in_port}
    actions = [{"type":"OUTPUT", "port": out_port}]

    # start3 = datetime.datetime.now()
    # flow = build_flow(dpid, 2, match, actions)
    # add_flow(flow) # add flow
    # stop3 = datetime.datetime.now()
    # time_diff = (stop3 - start3)
    # ex_time = time_diff.total_seconds() * 1000
    # print('build_flow: ', ex_time)

    msg = None
    if buffer_id == OFP_NO_BUFFER:
        msg = encoded_data

    start4 = datetime.datetime.now()
    pkt = build_packet(msg, dpid, in_port, actions, buffer_id) # build packet
    stop4 = datetime.datetime.now()
    time_diff = (stop4 - start4)
    ex_time = time_diff.total_seconds() * 1000
    print('build_packet: ', ex_time)

    start5 = datetime.datetime.now()
    send_packet(pkt) # send packet
    stop5 = datetime.datetime.now()
    time_diff = (stop5 - start5)
    ex_time = time_diff.total_seconds() * 1000
    print('send_packet: ', ex_time)

    stop1 = datetime.datetime.now()
    time_diff = (stop1 - start1)
    ex_time = time_diff.total_seconds() * 1000
    print('post_packetin: ', ex_time)
    print('post_packetin stop timestamp', stop1)

    return "ACK"

# @api.route('/switch-features', methods=['POST'])
# def post_switch_features():
#     start1 = datetime.datetime.now()
#     print('post_switch_features start timestamp', start1)
    
#     if not request.json:
#         abort(400)

#     start2 = datetime.datetime.now()
#     data = extract_data(request.json, "OFPSwitchFeatures")
#     stop2 = datetime.datetime.now()
#     time_diff = (stop2 - start2)
#     ex_time = time_diff.total_seconds() * 1000
#     print('extract_data: ', ex_time)

#     dpid = data['dpid']

#     for key in slice_to_port[dpid]:
#         in_port = key
#         out_port = slice_to_port[dpid][key]

#         match = {'in_port': in_port}
#         actions = [{"type":"OUTPUT", "port": out_port}]

#         start3 = datetime.datetime.now()
#         flow = build_flow(dpid, 2, match, actions)
#         add_flow(flow) # add flow
#         stop3 = datetime.datetime.now()
#         time_diff = (stop3 - start3)
#         ex_time = time_diff.total_seconds() * 1000
#         print('build_flow: ', ex_time)

#     stop1 = datetime.datetime.now()
#     time_diff = (stop1 - start1)
#     ex_time = time_diff.total_seconds() * 1000
#     print('post_switch_features: ', ex_time)
#     print('post_switch_features stop timestamp', stop1)

#     return "ACK"

if __name__ == "__main__":
    api.run(host=middle_ryu_app, port=8090)