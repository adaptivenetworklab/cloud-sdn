from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0

from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import udp


class RightSlice(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(RightSlice, self).__init__(*args, **kwargs)

        # outport = self.mac_to_port[dpid][mac_address]
        self.mac_to_port = {
            14: {"00:00:00:00:00:09": 4, "00:00:00:00:00:10": 5},
            15: {"00:00:00:00:00:11": 3, "00:00:00:00:00:12": 4},
        }

        # port mapping untuk non-edge switch (long & short)

        # outport = self.short_path[dpid][in_port]
        self.short_path = {
            3: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0},
            8: {1: 0, 2: 0, 3: 0, 4: 0, 5: 6, 6: 5},
            9: {1: 0, 2: 0, 3: 0, 4: 5, 5: 4, 6: 0},
        }

        # outport = self.long_path[dpid][in_port]
        self.long_path = {
            3: {1: 0, 2: 0, 3: 0, 4: 0, 5: 6, 6: 5},
            8: {1: 0, 2: 0, 3: 5, 4: 0, 5: 3, 6: 0},
            9: {1: 0, 2: 0, 3: 5, 4: 0, 5: 3, 6: 0},
        }

        # outport = self.edge_sw_port[dpid][short(1)/long(2)]
        self.edge_sw_port = {
            14: {1: 3, 2: 2},
            15: {1: 1, 2: 2},
        }

        self.rtp_dst_port = range(10000, 20001) # range of rtp port for VoIP
        self.sip_dst_port = 5060 # default sip port for VoIP

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        mod = parser.OFPFlowMod(
            datapath=datapath,
            match=match,
            cookie=0,
            command=ofproto.OFPFC_ADD,
            idle_timeout=20,
            hard_timeout=120,
            priority=priority,
            flags=ofproto.OFPFF_SEND_FLOW_REM,
            actions=actions,
        )
        datapath.send_msg(mod)

    def _send_package(self, msg, datapath, in_port, actions):
        data = None
        ofproto = datapath.ofproto
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data,
        )
        datapath.send_msg(out)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        in_port = msg.in_port
        dpid = datapath.id
        out_port = 0

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            # self.logger.info("LLDP packet discarded.")
            return
        dst = eth.dst
        src = eth.src

        is_src_match_port = False
        is_dst_match_port = False

        if pkt.get_protocol(udp.udp):
            is_src_match_port = (
                pkt.get_protocol(udp.udp).src_port == self.sip_dst_port or
                pkt.get_protocol(udp.udp).src_port in self.rtp_dst_port
            ) 
            is_dst_match_port = (
                pkt.get_protocol(udp.udp).dst_port == self.sip_dst_port or
                pkt.get_protocol(udp.udp).dst_port in self.rtp_dst_port
            ) 

        # self.logger.info("packet in s%s in_port=%s eth_src=%s eth_dst=%s pkt=%s udp=%s", dpid, in_port, src, dst, pkt, pkt.get_protocol(udp.udp))
        self.logger.info("INFO packet arrived in s%s (in_port=%s)", dpid, in_port)

        if dpid in self.mac_to_port: # if the datapath is edge switch
            if dst in self.mac_to_port[dpid]: # traffic to end device
                out_port = self.mac_to_port[dpid][dst]
                self.logger.info(
                    "INFO sending packet from s%s (out_port=%s)",
                    dpid,
                    out_port,
                )
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                match = datapath.ofproto_parser.OFPMatch(dl_dst=dst)
                self.add_flow(datapath, 2, match, actions)
                self._send_package(msg, datapath, in_port, actions)
            
            elif ( # voip traffic is using short path (considered by src_port)
                pkt.get_protocol(udp.udp) and is_src_match_port
            ):
                out_port = self.edge_sw_port[dpid][1]

                if out_port == 0:
                    return
                
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    dl_src=src,
                    dl_dst=dst,
                    dl_type=ether_types.ETH_TYPE_IP,
                    nw_proto=0x11,  # udp
                    tp_src=pkt.get_protocol(udp.udp).src_port
                )
                self.logger.info("INFO sending packet from s%s (out_port=%s)", dpid, out_port)

                self.add_flow(datapath, 3, match, actions)
                self._send_package(msg, datapath, in_port, actions)

            elif ( # voip traffic is using short path (considered by dst_port)
                pkt.get_protocol(udp.udp) and is_dst_match_port
            ):
                out_port = self.edge_sw_port[dpid][1]

                if out_port == 0:
                    return
                
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    dl_src=src,
                    dl_dst=dst,
                    dl_type=ether_types.ETH_TYPE_IP,
                    nw_proto=0x11,  # udp
                    tp_dst=pkt.get_protocol(udp.udp).dst_port
                )
                self.logger.info("INFO sending packet from s%s (out_port=%s)", dpid, out_port)

                self.add_flow(datapath, 3, match, actions)
                self._send_package(msg, datapath, in_port, actions)

            else: # non-voip traffic is using long path
                out_port = self.edge_sw_port[dpid][2]

                if out_port == 0:
                    return
                
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    dl_dst=dst,
                    dl_type=ether_types.ETH_TYPE_IP,
                )
                self.logger.info("INFO sending packet from s%s (out_port=%s)", dpid, out_port)

                self.add_flow(datapath, 1, match, actions)
                self._send_package(msg, datapath, in_port, actions)

        else: # if the datapath is non-edge switch
            if ( # voip traffic is using short path (considered by src_port)
                pkt.get_protocol(udp.udp) and is_src_match_port
            ):
                out_port = self.short_path[dpid][in_port]

                if out_port == 0:
                    return
                
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    dl_src=src,
                    dl_dst=dst,
                    dl_type=ether_types.ETH_TYPE_IP,
                    nw_proto=0x11,  # udp
                    tp_src=pkt.get_protocol(udp.udp).src_port
                )
                self.logger.info("INFO sending packet from s%s (out_port=%s)", dpid, out_port)

                self.add_flow(datapath, 3, match, actions)
                self._send_package(msg, datapath, in_port, actions)

            elif ( # voip traffic is using short path (considered by dst_port)
                pkt.get_protocol(udp.udp) and is_dst_match_port
            ):
                out_port = self.short_path[dpid][in_port]

                if out_port == 0:
                    return
                
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    dl_src=src,
                    dl_dst=dst,
                    dl_type=ether_types.ETH_TYPE_IP,
                    nw_proto=0x11,  # udp
                    tp_dst=pkt.get_protocol(udp.udp).dst_port
                )
                self.logger.info("INFO sending packet from s%s (out_port=%s)", dpid, out_port)

                self.add_flow(datapath, 3, match, actions)
                self._send_package(msg, datapath, in_port, actions)
            
            else: # non-voip traffic is using long path
                out_port = self.long_path[dpid][in_port]

                if out_port == 0:
                    return
                
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    dl_dst=dst,
                    dl_type=ether_types.ETH_TYPE_IP,
                )
                self.logger.info("INFO sending packet from s%s (out_port=%s)", dpid, out_port)

                self.add_flow(datapath, 1, match, actions)
                self._send_package(msg, datapath, in_port, actions)
                

