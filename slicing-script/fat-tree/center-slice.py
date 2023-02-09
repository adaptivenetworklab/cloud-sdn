from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import udp
from ryu.lib.packet import icmp


class CenterSlice(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(CenterSlice, self).__init__(*args, **kwargs)

        # outport = self.mac_to_port[dpid][mac_address]
        self.mac_to_port = {
            12: {"00:00:00:00:00:05": 4, "00:00:00:00:00:06": 5},
            13: {"00:00:00:00:00:07": 4, "00:00:00:00:00:08": 5},
        }

        # port mapping untuk non-edge switch
        # outport = self.non_edge_sw_port[dpid][in_port]
        self.non_edge_sw_port = {
            2: {1: 6, 6: 1},
            6: {5: 2, 2: 5},
            7: {5: 2, 2: 5},
        }

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

        # self.logger.info("packet in s%s in_port=%s eth_src=%s eth_dst=%s pkt=%s udp=%s", dpid, in_port, src, dst, pkt, pkt.get_protocol(udp.udp))
        self.logger.info("INFO packet arrived in s%s (in_port=%s)", dpid, in_port)

        if dpid in self.mac_to_port: # jika switch 10 atau 11
            if dst in self.mac_to_port[dpid]: # jika dst mac ada di dictionary mac_to_port[dpid] atau dst mac menuju end device  
                out_port = self.mac_to_port[dpid][dst]
                self.logger.info(
                    "INFO sending packet from s%s (out_port=%s)",
                    dpid,
                    out_port,
                )
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                match = datapath.ofproto_parser.OFPMatch(dl_dst=dst)
                self.add_flow(datapath, 1, match, actions)
                self._send_package(msg, datapath, in_port, actions)

            else:
                out_port = 2
                self.logger.info(
                    "INFO sending packet from s%s (out_port=%s)",
                    dpid,
                    out_port,
                )
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    dl_dst=dst,
                    dl_type=ether_types.ETH_TYPE_IP,
                )

                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                self.add_flow(datapath, 1, match, actions)
                self._send_package(msg, datapath, in_port, actions)

        else: # jika bukan s10 atau s11, maka lakukan simple forwarding
            self.logger.info("INFO packet arrived in s%s (in_port=%s)", dpid, in_port)
            out_port = self.non_edge_sw_port[dpid][in_port]
            
            actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
            match = datapath.ofproto_parser.OFPMatch(in_port=in_port)
            self.logger.info("INFO sending packet from s%s (out_port=%s)", dpid, out_port)

            self.add_flow(datapath, 1, match, actions)
            self._send_package(msg, datapath, in_port, actions)
