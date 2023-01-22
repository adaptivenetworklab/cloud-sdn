from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0

from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import tcp


class CenterSlice(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(CenterSlice, self).__init__(*args, **kwargs)

        # out_port = non_edge_switch_short[dpid][in_port]
        self.non_edge_switch_short = {
            2: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0},
            6: {1: 0, 2: 0, 3: 0, 4: 0, 5: 6, 6: 5},
            7: {1: 0, 2: 0, 3: 0, 4: 5, 5: 4, 6: 0}
        }

        # out_port = non_edge_switch_long[dpid][in_port]
        self.non_edge_switch_long = {
            2: {1: 6, 2: 0, 3: 0, 4: 0, 5: 0, 6: 1},
            6: {1: 0, 2: 5, 3: 0, 4: 0, 5: 2, 6: 0},
            7: {1: 0, 2: 5, 3: 0, 4: 0, 5: 2, 6: 0}
        }

        # out_port = edge_switch_short[dpid][in_port]
        self.edge_switch_short = {
            13: {1: 0, 2: 0, 3: 0, 4: 3, 5: 3, 6: 3},
            14: {1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 1}
        }

        # out_port = edge_switch_long[dpid][in_port]
        self.edge_switch_long = {
            13: {1: 0, 2: 0, 3: 0, 4: 2, 5: 2, 6: 2},
            14: {1: 0, 2: 0, 3: 0, 4: 2, 5: 2, 6: 2}
        }

        # out_port = edge_switch_to_end[dpid][dst-mac]
        self.edge_switch_to_end = {
            13: {"00:00:00:00:00:05": 4, "00:00:00:00:00:06": 5},
            14: {"00:00:00:00:00:07": 4, "00:00:00:00:00:08": 5}
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
        # self.logger.info("send_msg %s", out)
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

        dst = eth.dst

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            # self.logger.info("LLDP packet discarded.")
            return

        if dpid in self.edge_switch_to_end:
            if dst in self.edge_switch_to_end[dpid]:
                out_port = self.edge_switch_to_end[dpid][dst]
                self.logger.info(
                    "INFO sending packet from s%s (out_port=%s) w/ mac-to-port rule",
                    dpid,
                    out_port,
                )
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                match = datapath.ofproto_parser.OFPMatch(dl_dst=dst)
                self.add_flow(datapath, 10, match, actions)
                self._send_package(msg, datapath, in_port, actions)

            elif (
                pkt.get_protocol(tcp.tcp) and 
                (pkt.get_protocol(tcp.tcp).dst_port == 80 or pkt.get_protocol(tcp.tcp).src_port == 80)
            ):
                # implement short direction with higher priority
                out_port = self.edge_switch_short[dpid][in_port]
                self.logger.info(
                    "INFO sending packet from s%s (out_port=%s) w/ TCP 80 rule (short path)",
                    dpid,
                    out_port,
                )
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    dl_dst=dst,
                    dl_type=ether_types.ETH_TYPE_IP,
                    tp_src=pkt.get_protocol(tcp.tcp).src_port,
                    tp_dst=pkt.get_protocol(tcp.tcp).dst_port,
                )

                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                self.add_flow(datapath, 2, match, actions)
                self._send_package(msg, datapath, in_port, actions)

            elif (
                pkt.get_protocol(tcp.tcp) and 
                pkt.get_protocol(tcp.tcp).dst_port != 80 and
                pkt.get_protocol(tcp.tcp).src_port != 80
            ):
                # implement long direction with normal priority
                out_port = self.edge_switch_long[dpid][in_port]
                self.logger.info(
                    "INFO sending packet from s%s (out_port=%s) w/ TCP not 80 rule (long path)",
                    dpid,
                    out_port,
                )
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    dl_dst=dst,
                    dl_type=ether_types.ETH_TYPE_IP,
                    tp_src=pkt.get_protocol(tcp.tcp).src_port,
                    tp_dst=pkt.get_protocol(tcp.tcp).dst_port,
                )

                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                self.add_flow(datapath, 1, match, actions)
                self._send_package(msg, datapath, in_port, actions)

            elif not pkt.get_protocol(tcp.tcp): # jika protocolnya bukan tcp, discard packet-nya
                self.logger.info("packet in s%s in_port=%s discarded, because it's not tcp and not going to end device.", dpid, in_port)
                return # packet di-drop jika protokolnya bukan tcp

        elif dpid in self.non_edge_switch_short:
            if (
                pkt.get_protocol(tcp.tcp) and 
                (pkt.get_protocol(tcp.tcp).dst_port == 80 or pkt.get_protocol(tcp.tcp).src_port == 80)
            ):
                # implement short direction with higher priority
                out_port = self.non_edge_switch_short[dpid][in_port]
                self.logger.info(
                    "INFO sending packet from s%s (out_port=%s) w/ TCP 80 rule (short path)",
                    dpid,
                    out_port,
                )
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    dl_dst=dst,
                    dl_type=ether_types.ETH_TYPE_IP,
                    tp_src=pkt.get_protocol(tcp.tcp).src_port,
                    tp_dst=pkt.get_protocol(tcp.tcp).dst_port,
                )

                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                self.add_flow(datapath, 2, match, actions)
                self._send_package(msg, datapath, in_port, actions)

            elif (
                pkt.get_protocol(tcp.tcp) and 
                pkt.get_protocol(tcp.tcp).dst_port != 80 and
                pkt.get_protocol(tcp.tcp).src_port != 80
            ):
                # implement long direction with normal priority
                out_port = self.non_edge_switch_long[dpid][in_port]
                self.logger.info(
                    "INFO sending packet from s%s (out_port=%s) w/ TCP not 80 rule (long path)",
                    dpid,
                    out_port,
                )
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    dl_dst=dst,
                    dl_type=ether_types.ETH_TYPE_IP,
                    tp_src=pkt.get_protocol(tcp.tcp).src_port,
                    tp_dst=pkt.get_protocol(tcp.tcp).dst_port,
                )

                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                self.add_flow(datapath, 1, match, actions)
                self._send_package(msg, datapath, in_port, actions)

            elif not pkt.get_protocol(tcp.tcp): # jika protocolnya bukan tcp, discard packet-nya
                self.logger.info("packet in s%s in_port=%s discarded, because it's not tcp and not going to end device.", dpid, in_port)
                return # packet di-drop jika protokolnya bukan tcp
        else:
            self.logger.info("packet in s%s in_port=%s discarded, switch is not available in this slice.", dpid, in_port)
            return # packet di-drop jika switch tidak terdaftar di slice ini