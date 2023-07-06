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
$ wsdump.py ws://127.0.0.1:8080/simpleswitch/ws
< "ethernet(dst='ff:ff:ff:ff:ff:ff',ethertype=2054,src='32:1a:51:fb:91:77'), a
rp(dst_ip='10.0.0.2',dst_mac='00:00:00:00:00:00',hlen=6,hwtype=1,opcode=1,plen
=4,proto=2048,src_ip='10.0.0.1',src_mac='32:1a:51:fb:91:77')"
< "ethernet(dst='32:1a:51:fb:91:77',ethertype=2054,src='26:8c:15:0c:de:49'), a
rp(dst_ip='10.0.0.1',dst_mac='32:1a:51:fb:91:77',hlen=6,hwtype=1,opcode=2,plen
=4,proto=2048,src_ip='10.0.0.2',src_mac='26:8c:15:0c:de:49')"
< "ethernet(dst='26:8c:15:0c:de:49',ethertype=2048,src='32:1a:51:fb:91:77'), i
pv4(csum=9895,dst='10.0.0.2',flags=2,header_length=5,identification=0,offset=0
,option=None,proto=1,src='10.0.0.1',tos=0,total_length=84,ttl=64,version=4), i
cmp(code=0,csum=43748,data=echo(data='`\\xb9uS\\x00\\x00\\x00\\x00\\x7f\\'\\x0
1\\x00\\x00\\x00\\x00\\x00\\x10\\x11\\x12\\x13\\x14\\x15\\x16\\x17\\x18\\x19\\
x1a\\x1b\\x1c\\x1d\\x1e\\x1f !\"#$%&\\'()*+,-./01234567',id=14355,seq=1),type=
8)"

Get arp table:
> {"jsonrpc": "2.0", "id": 1, "method": "get_arp_table", "params" : {}}
< {"jsonrpc": "2.0", "id": 1, "result": {"1": {"32:1a:51:fb:91:77": 1, "26:8c:
15:0c:de:49": 2}}}
"""

import websockets
import asyncio
from ryu.base import app_manager
from ryu.app.wsgi import ControllerBase
from ryu.app.wsgi import rpc_public
from ryu.app.wsgi import websocket
from ryu.app.wsgi import WebSocketRPCServer
from ryu.app.wsgi import WSGIApplication
from ryu.controller import ofp_event
from ryu.controller.handler import set_ev_cls
from ryu.lib.packet import packet
import json

simple_switch_instance_name = 'simple_switch_api_app'
url = '/packetin'


class MiddlewareWebSocket(app_manager.RyuApp):
    _CONTEXTS = {
        'wsgi': WSGIApplication,
    }

    def __init__(self, *args, **kwargs):
        super(MiddlewareWebSocket, self).__init__(*args, **kwargs)
        self.datapath_dict = {}
        wsgi = kwargs['wsgi']
        wsgi.register(
            MiddlewareWebSocketController,
            data={simple_switch_instance_name: self},
        )
        self._ws_manager = wsgi.websocketmanager
        # Start the WebSocket server
        asyncio.run(self.start_server())

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

    @websocket('sendpacket', '/sendpacket')
    def websocket_handler(self, ws):
        while True:
            msg = ws.wait()
            # Process the received message
            self.sendpacket(msg)

    def sendpacket(self, msg):
        # Parse the received JSON message
        pkt = json.loads(msg)

        datapath = self.get_datapath_by_dpid(pkt['dpid'])

        if datapath is not None:
            out = datapath.ofproto_parser.OFPPacketOut(
                datapath=datapath,
                buffer_id=pkt['buffer_id'],
                in_port=pkt['in_port'],
                actions=pkt['actions'],
                data=pkt['data'],
            )
            datapath.send_msg(out)

    # async def start_server(self):
    #     # Define the WebSocket server URL
    #     ws_host = '192.168.56.10'
    #     ws_port = 8090
        
    #     # Start the WebSocket server
    #     server = await websockets.serve(self.sendpacket, ws_host, ws_port)
    #     print(f"WebSocket server started at ws://{ws_host}:{ws_port}")
        
    #     # Keep the server running until interrupted
    #     await server.wait_closed()


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
