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

api = Flask(__name__)

#TODO import from ofp
OFPP_FLOOD = 0xfffb
OFP_DEFAULT_PRIORITY = 32768
OFPFF_SEND_FLOW_REM = 1 << 0
OFP_NO_BUFFER = 0xffffffff

SEND_OUT = None

RYU_BASE_URL = "http://10.0.2.207:8080"
#RYU_BASE_URL = "http://172.17.0.2:8080"
#RYU_BASE_URL = "http://ryu_middleware:8080"

mac_to_port = {}

def build_flow(dpid, src, dst, in_port, out_port, buffer_id, cookie = 0, idle_timeout = 0, hard_timeout = 0, priority = OFP_DEFAULT_PRIORITY, flags = 1, actions = SEND_OUT):
    "Build and return a flow entry based on https://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#add-a-flow-entry"

    match = {'in_port': in_port, 'dl_src': src, 'dl_dst': dst}

    if actions == SEND_OUT:
        actions = [{"type":"OUTPUT", "port": out_port}]

    flow = {
        'dpid' : dpid,
        'match' : match,
        'cookie' : cookie,
        'idle_timeout' : idle_timeout,
        'hard_timeout' : hard_timeout,
        'priority' : priority,
        'flags' : flags,
        'actions': actions,
        'buffer_id': buffer_id
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

def build_packet(dpid, in_port, out_port, data, buffer_id):
    "Build and return a packet"
    pkt = {
        'dpid' : dpid,
        'buffer_id': buffer_id,
        'in_port' : in_port,
        'actions': [{"type":"OUTPUT", "port": out_port}],
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

    data['encoded_data'] = data['data']
    data['data'] = base64.b64decode(data['encoded_data'])
    data['dpid'] = msg['dpid']

    packet_data = packet.Packet(data['data'])
    eth = packet_data.get_protocol(ethernet.ethernet)

    if eth.ethertype == ether_types.ETH_TYPE_LLDP:
        data['is_lldp'] = True
    else:
        data['is_lldp'] = False

        data['dst'] = eth.dst
        data['src'] = eth.src

    return data

def update_mac_to_port(dpid, src, in_port):
    mac_to_port.setdefault(dpid, {})

    # learn a mac address to avoid FLOOD next time.
    mac_to_port[dpid][src] = in_port


def out_port_lookup(dpid, dst):
    if dst in mac_to_port[dpid]:
        return mac_to_port[dpid][dst]
    else:
        return OFPP_FLOOD

@api.route('/')
def index():
    return 'Simple Switch Rest Server'

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
    src = data['src']
    dst = data['dst']
    in_port = data['in_port']
    buffer_id = data['buffer_id']
    encoded_data = data['encoded_data']

    update_mac_to_port(dpid, src, in_port)
    out_port = out_port_lookup(dpid, dst)

    start3 = datetime.datetime.now()
    if out_port != OFPP_FLOOD:
        # flow = build_flow(dpid, src, dst, in_port, out_port, buffer_id)
        flow = build_flow(dpid, src, dst, in_port, out_port, buffer_id, hard_timeout=5, idle_timeout=5)
        add_flow(flow)
    stop3 = datetime.datetime.now()
    time_diff = (stop3 - start3)
    ex_time = time_diff.total_seconds() * 1000
    print('build_flow: ', ex_time)

    msg = None
    if buffer_id == OFP_NO_BUFFER:
        msg = encoded_data

    start4 = datetime.datetime.now()
    pkt = build_packet(dpid, in_port, out_port, msg, buffer_id)
    stop4 = datetime.datetime.now()
    time_diff = (stop4 - start4)
    ex_time = time_diff.total_seconds() * 1000
    print('build_packet: ', ex_time)

    start5 = datetime.datetime.now()
    send_packet(pkt)
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

if __name__ == "__main__":
    api.run(host='0.0.0.0', port=8090)
