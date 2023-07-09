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

import websocket
import json
import base64
import datetime
import json

import sys
sys.path.append('../')
from lib.packet import packet
from lib.packet import ethernet
from lib.packet import ether_types
from lib.packet import udp
from env import RIGHT_MIDDLEWARE
from env import RIGHT_FLOWMOD_ACTIVE

#TODO import from ofp
OFPP_FLOOD = 0xfffb
OFPFF_SEND_FLOW_REM = 1 << 0
OFP_NO_BUFFER = 0xffffffff

# outport = mac_to_port[dpid][mac_address]
mac_to_port = {
    14: {"00:00:00:00:00:09": 4, "00:00:00:00:00:10": 5},
    15: {"00:00:00:00:00:11": 3, "00:00:00:00:00:12": 4},
}

# port mapping untuk non-edge switch (long & short)

# outport = short_path[dpid][in_port]
short_path = {
    3: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0},
    8: {1: 0, 2: 0, 3: 0, 4: 0, 5: 6, 6: 5},
    9: {1: 0, 2: 0, 3: 0, 4: 5, 5: 4, 6: 0},
}

# outport = long_path[dpid][in_port]
long_path = {
    3: {1: 0, 2: 0, 3: 0, 4: 0, 5: 6, 6: 5},
    8: {1: 0, 2: 0, 3: 5, 4: 0, 5: 3, 6: 0},
    9: {1: 0, 2: 0, 3: 5, 4: 0, 5: 3, 6: 0},
}

# outport = edge_sw_port[dpid][short(1)/long(2)]
edge_sw_port = {
    14: {1: 3, 2: 2},
    15: {1: 1, 2: 2},
}

rtp_dst_port = range(10000, 20001) # range of rtp port for VoIP
sip_dst_port = 5060 # default sip port for VoIP

def build_flow(dpid, priority, match, actions):
    "Build and return a flow entry based on https://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#add-a-flow-entry"

    flow = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "addflow",
        "params": {
            'dpid' : dpid,
            'match' : match,
            'priority' : priority,
            'actions': actions,
        }
    }

    return flow

def add_flow(ws, flow):
    flow = json.dumps(flow)

    #TODO verbose mode
    print("sending {}".format(flow))

    ws.send(data=flow)

def build_packet(data, dpid, in_port, actions, buffer_id):
    "Build and return a packet"
    pkt = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "sendpacket",
        "params": {
            'dpid' : dpid,
            'buffer_id': buffer_id,
            'in_port' : in_port,
            'actions': actions,
            'data' : data
        }
    }

    return pkt

def send_packet(ws, pkt):
    pkt = json.dumps(pkt)

    start1 = datetime.datetime.now()
    print('send_packet start timestamp', start1)
    print('send_packet msg:', pkt)

    ws.send(data=pkt)

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

def on_message(ws, message):
    # Handle the received message from the server
    # In this example, we assume the server will send a JSON response
    start1 = datetime.datetime.now()
    print('post_packetin start timestamp', start1)
    
    json_data = json.loads(message)

    start2 = datetime.datetime.now()
    data = extract_data(json_data, "OFPPacketIn")
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

    pkt = packet.Packet(data['data'])
    eth = pkt.get_protocol(ethernet.ethernet)
    dst_mac = eth.dst
    src_mac = eth.src

    is_src_match_port = False
    is_dst_match_port = False

    if pkt.get_protocol(udp.udp):
        is_src_match_port = (
            pkt.get_protocol(udp.udp).src_port == sip_dst_port or
            pkt.get_protocol(udp.udp).src_port in rtp_dst_port
        ) 
        is_dst_match_port = (
            pkt.get_protocol(udp.udp).dst_port == sip_dst_port or
            pkt.get_protocol(udp.udp).dst_port in rtp_dst_port
        )
    

    if dpid in mac_to_port: # if the datapath is edge switch
        if dst in mac_to_port[dpid]: # traffic to end device
            out_port = mac_to_port[dpid][dst_mac]

            actions = [{"type":"OUTPUT", "port": out_port}]
            
            if RIGHT_FLOWMOD_ACTIVE:
                match = {'dl_dst': dst_mac}

                start3 = datetime.datetime.now()
                flow = build_flow(dpid, 2, match, actions)
                add_flow(ws, flow) # add flow
                stop3 = datetime.datetime.now()
                time_diff = (stop3 - start3)
                ex_time = time_diff.total_seconds() * 1000
                print('build_flow: ', ex_time)

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
            send_packet(ws, pkt) # send packet
            stop5 = datetime.datetime.now()
            time_diff = (stop5 - start5)
            ex_time = time_diff.total_seconds() * 1000
            print('send_packet: ', ex_time)
        
        elif ( # voip traffic is using short path (considered by src_port)
            pkt.get_protocol(udp.udp) and is_src_match_port
        ):
            out_port = edge_sw_port[dpid][1]

            if out_port == 0:
                return

            actions = [{"type":"OUTPUT", "port": out_port}]
            
            if RIGHT_FLOWMOD_ACTIVE:
                match = {
                    'in_port': in_port,
                    'dl_src': src_mac,
                    'dl_dst': dst_mac,
                    'dl_type': ether_types.ETH_TYPE_IP,
                    'nw_proto': 0x11, #udp
                    'tp_src': pkt.get_protocol(udp.udp).src_port
                }

                start3 = datetime.datetime.now()
                flow = build_flow(dpid, 3, match, actions)
                add_flow(ws, flow) # add flow
                stop3 = datetime.datetime.now()
                time_diff = (stop3 - start3)
                ex_time = time_diff.total_seconds() * 1000
                print('build_flow: ', ex_time)

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
            send_packet(ws, pkt) # send packet
            stop5 = datetime.datetime.now()
            time_diff = (stop5 - start5)
            ex_time = time_diff.total_seconds() * 1000
            print('send_packet: ', ex_time)
            
        elif ( # voip traffic is using short path (considered by dst_port)
            pkt.get_protocol(udp.udp) and is_dst_match_port
        ):
            out_port = edge_sw_port[dpid][1]

            if out_port == 0:
                return

            actions = [{"type":"OUTPUT", "port": out_port}]
            
            if RIGHT_FLOWMOD_ACTIVE:
                match = {
                    'in_port': in_port,
                    'dl_src': src_mac,
                    'dl_dst': dst_mac,
                    'dl_type': ether_types.ETH_TYPE_IP,
                    'nw_proto': 0x11, #udp
                    'tp_dst': pkt.get_protocol(udp.udp).dst_port
                }

                start3 = datetime.datetime.now()
                flow = build_flow(dpid, 3, match, actions)
                add_flow(ws, flow) # add flow
                stop3 = datetime.datetime.now()
                time_diff = (stop3 - start3)
                ex_time = time_diff.total_seconds() * 1000
                print('build_flow: ', ex_time)

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
            send_packet(ws, pkt) # send packet
            stop5 = datetime.datetime.now()
            time_diff = (stop5 - start5)
            ex_time = time_diff.total_seconds() * 1000
            print('send_packet: ', ex_time)
            
        else: # non-voip traffic is using long path
            out_port = edge_sw_port[dpid][2]

            if out_port == 0:
                return

            actions = [{"type":"OUTPUT", "port": out_port}]
            
            if RIGHT_FLOWMOD_ACTIVE:
                match = {
                    'in_port': in_port,
                    'dl_dst': dst_mac,
                    'dl_type': ether_types.ETH_TYPE_IP,
                }

                start3 = datetime.datetime.now()
                flow = build_flow(dpid, 1, match, actions)
                add_flow(ws, flow) # add flow
                stop3 = datetime.datetime.now()
                time_diff = (stop3 - start3)
                ex_time = time_diff.total_seconds() * 1000
                print('build_flow: ', ex_time)

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
            send_packet(ws, pkt) # send packet
            stop5 = datetime.datetime.now()
            time_diff = (stop5 - start5)
            ex_time = time_diff.total_seconds() * 1000
            print('send_packet: ', ex_time)

    else: # if the datapath is non-edge switch
        if ( # voip traffic is using short path (considered by src_port)
            pkt.get_protocol(udp.udp) and is_src_match_port
        ):
            out_port = short_path[dpid][in_port]

            if out_port == 0:
                return

            actions = [{"type":"OUTPUT", "port": out_port}]
            
            if RIGHT_FLOWMOD_ACTIVE:
                match = {
                    'in_port': in_port,
                    'dl_src': src_mac,
                    'dl_dst': dst_mac,
                    'dl_type': ether_types.ETH_TYPE_IP,
                    'nw_proto': 0x11, # udp
                    'tp_src': pkt.get_protocol(udp.udp).src_port
                }

                start3 = datetime.datetime.now()
                flow = build_flow(dpid, 3, match, actions)
                add_flow(ws, flow) # add flow
                stop3 = datetime.datetime.now()
                time_diff = (stop3 - start3)
                ex_time = time_diff.total_seconds() * 1000
                print('build_flow: ', ex_time)

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
            send_packet(ws, pkt) # send packet
            stop5 = datetime.datetime.now()
            time_diff = (stop5 - start5)
            ex_time = time_diff.total_seconds() * 1000
            print('send_packet: ', ex_time)

        elif ( # voip traffic is using short path (considered by dst_port)
            pkt.get_protocol(udp.udp) and is_dst_match_port
        ):
            out_port = short_path[dpid][in_port]

            if out_port == 0:
                return

            actions = [{"type":"OUTPUT", "port": out_port}]
            
            if RIGHT_FLOWMOD_ACTIVE:
                match = {
                    'in_port': in_port,
                    'dl_src': src_mac,
                    'dl_dst': dst_mac,
                    'dl_type': ether_types.ETH_TYPE_IP,
                    'nw_proto': 0x11, # udp
                    'tp_src': pkt.get_protocol(udp.udp).dst_port
                }

                start3 = datetime.datetime.now()
                flow = build_flow(dpid, 3, match, actions)
                add_flow(ws, flow) # add flow
                stop3 = datetime.datetime.now()
                time_diff = (stop3 - start3)
                ex_time = time_diff.total_seconds() * 1000
                print('build_flow: ', ex_time)

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
            send_packet(ws, pkt) # send packet
            stop5 = datetime.datetime.now()
            time_diff = (stop5 - start5)
            ex_time = time_diff.total_seconds() * 1000
            print('send_packet: ', ex_time)
            
        else: # non-voip traffic is using long path
            out_port = long_path[dpid][in_port]

            if out_port == 0:
                return

            actions = [{"type":"OUTPUT", "port": out_port}]
            
            if RIGHT_FLOWMOD_ACTIVE:
                match = {
                    'in_port': in_port,
                    'dl_dst': dst_mac,
                    'dl_type': ether_types.ETH_TYPE_IP,
                }

                start3 = datetime.datetime.now()
                flow = build_flow(dpid, 1, match, actions)
                add_flow(ws, flow) # add flow
                stop3 = datetime.datetime.now()
                time_diff = (stop3 - start3)
                ex_time = time_diff.total_seconds() * 1000
                print('build_flow: ', ex_time)

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
            send_packet(ws, pkt) # send packet
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

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("Connection closed")

if __name__ == '__main__':
    # establish connection to receive packetin from middleware
    ws_url = "ws://" + RIGHT_MIDDLEWARE + "/packetin"
    print("Accessing", ws_url)
    ws = websocket.WebSocketApp(ws_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()
