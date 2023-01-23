from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import udp


class LeftSlice(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(LeftSlice, self).__init__(*args, **kwargs)

        # outport = self.mac_to_port[dpid][mac_address]
        self.mac_to_port = {
            10: {"00:00:00:00:00:01": 3, "00:00:00:00:00:02": 4}, # in s10 [out port 3 if mac 00::01, out port 4 if mac 00:02] 
            11: {"00:00:00:00:00:03": 4, "00:00:00:00:00:04": 5},
        }
        self.slice_TCport = 8888

        # outport = self.slice_ports[dpid][slicenumber]
        self.slice_ports = {10: {1: 1, 2: 2}, 11: {1: 1, 2: 2}}
        self.end_switches = [10, 11]

        # port mapping untuk non-edge switch
        # outport = self.slice_ports[dpid][in_port]
        self.non_edge_sw_port = {
            1: {1: 2, 2: 1},
            4: {4: 1, 5: 1},
            5: {4: 1, 5: 1},
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
                    "INFO sending packet from s%s (out_port=%s) w/ mac-to-port rule",
                    dpid,
                    out_port,
                )
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                match = datapath.ofproto_parser.OFPMatch(dl_dst=dst)
                self.add_flow(datapath, 10, match, actions)
                self._send_package(msg, datapath, in_port, actions)

            elif ( # jika dst mac bukan mengarah ke end device dan protokol dari paketnya adalah udp dengan dst atau src port-nya 8888
                pkt.get_protocol(udp.udp)
                and (pkt.get_protocol(udp.udp).dst_port == self.slice_TCport or pkt.get_protocol(udp.udp).src_port == self.slice_TCport)
            ):
                slice_number = 1
                out_port = self.slice_ports[dpid][slice_number]
                self.logger.info(
                    "INFO sending packet from s%s (out_port=%s) w/ UDP 8888 rule",
                    dpid,
                    out_port,
                )
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    dl_dst=dst,
                    dl_type=ether_types.ETH_TYPE_IP,
                    nw_proto=0x11,  # udp
                    tp_dst=pkt.get_protocol(udp.udp).dst_port,
                )

                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                self.add_flow(datapath, 2, match, actions)
                self._send_package(msg, datapath, in_port, actions)

            elif ( # jika dst mac bukan mengarah ke end device dan protokol dari paketnya adalah udp dengan src atau dst port-nya selain 8888
                pkt.get_protocol(udp.udp)
                and pkt.get_protocol(udp.udp).dst_port != self.slice_TCport and pkt.get_protocol(udp.udp).src_port != self.slice_TCport
            ):
                slice_number = 2
                out_port = self.slice_ports[dpid][slice_number]
                self.logger.info(
                    "INFO sending packet from s%s (out_port=%s) w/ UDP general rule",
                    dpid,
                    out_port,
                )
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    dl_dst=dst,
                    dl_src=src,
                    dl_type=ether_types.ETH_TYPE_IP,
                    nw_proto=0x11,  # udp
                    tp_dst=pkt.get_protocol(udp.udp).dst_port,
                )
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                self.add_flow(datapath, 1, match, actions)
                self._send_package(msg, datapath, in_port, actions)

            elif not pkt.get_protocol(udp.udp): # jika protocolnya bukan udp, discard packet-nya
                self.logger.info("packet in s%s in_port=%s discarded, because it's not udp and not going to end device.", dpid, in_port)
                return # packet di-drop jika protokolnya bukan udp

        elif dpid not in self.end_switches: # jika bukan s10 atau s11, maka lakukan simple forwarding
            self.logger.info("INFO packet arrived in s%s (in_port=%s)", dpid, in_port)
            if (dpid == 4 or dpid == 5) and in_port == 1: # special case
                # arahkan flow dengan in_port 1 pada s4 atau s5 ke edge switch sesuai dst mac
                if dst in self.mac_to_port[10]:
                    out_port = 4
                elif dst in self.mac_to_port[11]:
                    out_port = 5
                else:
                    self.logger.info("packet in s%s in_port=%s discarded.", dpid, in_port)
                    return # packet di-drop jika dst mac tidak ada di dalam self.mac_to_port
            else:
                out_port = self.non_edge_sw_port[dpid][in_port]
            
            actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
            match = datapath.ofproto_parser.OFPMatch(in_port=in_port)
            self.logger.info("INFO sending packet from s%s (out_port=%s)", dpid, out_port)

            self.add_flow(datapath, 1, match, actions)
            self._send_package(msg, datapath, in_port, actions)
