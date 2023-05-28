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
from lib.packet import packet
from lib.packet import ethernet
from lib.packet import ether_types
from lib.packet import udp
import requests
import base64
import datetime
import json

PORT = 8090

print("Server is listenning on port " + str(PORT))

#TODO import from ofp
OFPP_FLOOD = 0xfffb
OFPFF_SEND_FLOW_REM = 1 << 0
OFP_NO_BUFFER = 0xffffffff

RYU_BASE_URL = "ws://192.168.1.1:8080"

# outport = mac_to_port[dpid][mac_address]
mac_to_port = {
    10: {"00:00:00:00:00:01": 3, "00:00:00:00:00:02": 4},
    11: {"00:00:00:00:00:03": 4, "00:00:00:00:00:04": 5},
}

# port mapping untuk non-edge switch (long & short)

# outport = short_path[dpid][in_port]
short_path = {
    1: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0},
    4: {1: 0, 2: 0, 3: 0, 4: 5, 5: 4, 6: 0},
    5: {1: 0, 2: 0, 3: 0, 4: 5, 5: 4, 6: 0},
}

# outport = long_path[dpid][in_port]
long_path = {
    1: {1: 2, 2: 1, 3: 0, 4: 0, 5: 0, 6: 0},
    4: {1: 4, 2: 0, 3: 0, 4: 1, 5: 0, 6: 0},
    5: {1: 5, 2: 0, 3: 0, 4: 0, 5: 1, 6: 0},
}

# outport = edge_sw_port[dpid][short(1)/long(2)]
edge_sw_port = {
    10: {1: 2, 2: 1},
    11: {1: 1, 2: 2},
}

rtp_dst_port = 5004 # default rtp port for vlc

def build_flow(dpid, priority, match, actions):
    "Build and return a flow entry based on https://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#add-a-flow-entry"

    flow = {
        'type' : 'FlowMod',
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
        'type' : 'PacketOut',
        'dpid' : dpid,
        'buffer_id': buffer_id,
        'in_port' : in_port,
        'actions': actions,
        'data' : data
    }

    return pkt

def send_packet(pkt):
    "Send a packet to a switch through Websocket"
    mapper_path = "/stats/sendpacket"
    asyncio.get_event_loop().run_until_complete(send_packet_helper(f"{mapper_path}:{pkt}"))
        
async def send_packet_helper(data):
    async with websockets.connect(RYU_BASE_URL) as websocket:
        start1 = datetime.datetime.now()
        print('send_packet start timestamp', start1)
        await websocket.send(data)

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

async def packetin(websocket, path):
    start1 = datetime.datetime.now()
    print('post_packetin start timestamp', start1)
    
    recv_data = await websocket.recv()
    json_data = json.loads(recv_data)

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
        is_src_match_port = pkt.get_protocol(udp.udp).src_port == rtp_dst_port
        is_dst_match_port = pkt.get_protocol(udp.udp).dst_port == rtp_dst_port

    if dpid in mac_to_port: # if the datapath is edge switch
        if dst in mac_to_port[dpid]: # traffic to end device
            out_port = mac_to_port[dpid][dst_mac]

            # match = {'dl_dst': dst_mac}
            actions = [{"type":"OUTPUT", "port": out_port}]

            # start3 = datetime.datetime.now()
            # flow = build_flow(datapath, 2, match, actions)
            # json_flow = json.dumps(flow)
            # await websocket.send(json_flow)
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
        
        elif ( # rtp traffic is using short path (considered by src_port)
            pkt.get_protocol(udp.udp) and is_src_match_port
        ):
            out_port = edge_sw_port[dpid][1]

            if out_port == 0:
                return

            # match = {
            #     'in_port': in_port,
            #     'dl_src': src_mac,
            #     'dl_dst': dst_mac,
            #     'dl_type': ether_types.ETH_TYPE_IP,
            #     'nw_proto': 0x11, #udp
            #     'tp_src': pkt.get_protocol(udp.udp).src_port
            # }
            actions = [{"type":"OUTPUT", "port": out_port}]

            # start3 = datetime.datetime.now()
            # flow = build_flow(dpid, 3, match, actions)
            # add_flow(flow) # add flow
            # json_flow = json.dumps(flow)
            # await websocket.send(json_flow)
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
            
        elif ( # rtp traffic is using short path (considered by dst_port)
            pkt.get_protocol(udp.udp) and is_dst_match_port
        ):
            out_port = edge_sw_port[dpid][1]

            if out_port == 0:
                return

            # match = {
            #     'in_port': in_port,
            #     'dl_src': src_mac,
            #     'dl_dst': dst_mac,
            #     'dl_type': ether_types.ETH_TYPE_IP,
            #     'nw_proto': 0x11, #udp
            #     'tp_dst': pkt.get_protocol(udp.udp).dst_port
            # }
            actions = [{"type":"OUTPUT", "port": out_port}]

            # start3 = datetime.datetime.now()
            # flow = build_flow(dpid, 3, match, actions)
            # add_flow(flow) # add flow
            # json_flow = json.dumps(flow)
            # await websocket.send(json_flow)
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
            
        else: # non-rtp traffic is using long path
            out_port = edge_sw_port[dpid][2]

            if out_port == 0:
                return

            # match = {
            #     'in_port': in_port,
            #     'dl_dst': dst_mac,
            #     'dl_type': ether_types.ETH_TYPE_IP,
            # }
            actions = [{"type":"OUTPUT", "port": out_port}]

            # start3 = datetime.datetime.now()
            # flow = build_flow(dpid, 1, match, actions)
            # add_flow(flow) # add flow
            # json_flow = json.dumps(flow)
            # await websocket.send(json_flow)
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

    else: # if the dpid is non-edge switch
        if ( # rtp traffic is using short path (considered by src_port)
            pkt.get_protocol(udp.udp) and is_src_match_port
        ):
            out_port = short_path[dpid][in_port]

            if out_port == 0:
                return

            # match = {
            #     'in_port': in_port,
            #     'dl_src': src_mac,
            #     'dl_dst': dst_mac,
            #     'dl_type': ether_types.ETH_TYPE_IP,
            #     'nw_proto': 0x11, # udp
            #     'tp_src': pkt.get_protocol(udp.udp).src_port
            # }
            actions = [{"type":"OUTPUT", "port": out_port}]

            # start3 = datetime.datetime.now()
            # flow = build_flow(dpid, 3, match, actions)
            # add_flow(flow) # add flow
            # json_flow = json.dumps(flow)
            # await websocket.send(json_flow)
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

        elif ( # rtp traffic is using short path (considered by dst_port)
            pkt.get_protocol(udp.udp) and is_dst_match_port
        ):
            out_port = short_path[dpid][in_port]

            if out_port == 0:
                return

            # match = {
            #     'in_port': in_port,
            #     'dl_src': src_mac,
            #     'dl_dst': dst_mac,
            #     'dl_type': ether_types.ETH_TYPE_IP,
            #     'nw_proto': 0x11, # udp
            #     'tp_src': pkt.get_protocol(udp.udp).dst_port
            # }
            actions = [{"type":"OUTPUT", "port": out_port}]

            # start3 = datetime.datetime.now()
            # flow = build_flow(dpid, 3, match, actions)
            # add_flow(flow) # add flow
            # json_flow = json.dumps(flow)
            # await websocket.send(json_flow)
            # stop3 = datetime.datetime.now()
            # time_diff = (stop3 - start3)
            # ex_time = time_diff.total_seconds() * 1000
            # print('build_flow: ', ex_time)

            msg = None
            if buffer_id == OFP_NO_BUFFER:
                msg = encoded_data

            start4 = datetime.datetime.now()
            pkt = build_packet(msg, dpid, dpid, actions, buffer_id) # build packet
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
            
        else: # non-rtp traffic is using long path
            out_port = long_path[dpid][in_port]

            if out_port == 0:
                return

            # match = {
            #     'in_port': in_port,
            #     'dl_dst': dst_mac,
            #     'dl_type': ether_types.ETH_TYPE_IP,
            # }
            actions = [{"type":"OUTPUT", "port": out_port}]

            # start3 = datetime.datetime.now()
            # flow = build_flow(dpid, 1, match, actions)
            # add_flow(flow) # add flow
            # json_flow = json.dumps(flow)
            # await websocket.send(json_flow)
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

if __name__ == "__main__":
    start_server = websockets.serve(packetin, "192.168.1.2", PORT)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()