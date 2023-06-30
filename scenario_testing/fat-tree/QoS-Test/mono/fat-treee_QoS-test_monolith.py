#!/usr/bin/python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink


class FVTopo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        # Create template host, switch, and link
        hconfig = {"inNamespace": True}
        # http_link_config = {"bw": 1}
        # voip_link_config = {"bw": 0.5}
        # video_link_config = {"bw": 3}

        # Create switch nodes
        for i in range(15):
            sconfig = {"dpid": "%010x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), protocols="OpenFlow10", **sconfig)

        # Create host nodes
        for i in range(12):
            if (i + 1) < 10:
                self.addHost("h%d" % (i + 1), mac="00:00:00:00:00:0%d" % (i + 1), **hconfig)
            else:
                self.addHost("h%d" % (i + 1), mac="00:00:00:00:00:%d" % (i + 1), **hconfig)

        # Add switch links
        self.addLink("s4", "s1")
        self.addLink("s5", "s1")
        self.addLink("s6", "s1")
        self.addLink("s7", "s1")
        self.addLink("s8", "s1")
        self.addLink("s9", "s1")
        self.addLink("s7", "s2")
        self.addLink("s8", "s2")
        self.addLink("s9", "s2")
        self.addLink("s4", "s2")
        self.addLink("s5", "s2")
        self.addLink("s6", "s2")
        self.addLink("s4", "s3")
        self.addLink("s5", "s3")
        self.addLink("s6", "s3")
        self.addLink("s7", "s3")
        self.addLink("s8", "s3")
        self.addLink("s9", "s3")
        self.addLink("s10", "s4")
        self.addLink("s11", "s4")
        self.addLink("s10", "s5")
        self.addLink("s11", "s5")
        self.addLink("s12", "s5")
        self.addLink("s11", "s6")
        self.addLink("s12", "s6")
        self.addLink("s13", "s6")
        self.addLink("s12", "s7")
        self.addLink("s13", "s7")
        self.addLink("s14", "s7")
        self.addLink("s13", "s8")
        self.addLink("s14", "s8")
        self.addLink("s15", "s8")
        self.addLink("s14", "s9")
        self.addLink("s15", "s9")

        # Add host links
        self.addLink("h1", "s10")
        self.addLink("h2", "s10")
        self.addLink("h3", "s11")
        self.addLink("h4", "s11")
        self.addLink("h5", "s12")
        self.addLink("h6", "s12")
        self.addLink("h7", "s13")
        self.addLink("h8", "s13")
        self.addLink("h9", "s14")
        self.addLink("h10", "s14")
        self.addLink("h11", "s15")
        self.addLink("h12", "s15")


topos = {"fvtopo": (lambda: FVTopo())}

if __name__ == "__main__":
    topo = FVTopo()
    net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )
    controller = RemoteController("c1", ip="10.0.1.242", port=6633)
    net.addController(controller)
    net.build()
    net.start()

    # h2, h4 = net.get('h2', 'h4')
    # h6, h8 = net.get('h6', 'h8')
    # h10, h12 = net.get('h10', 'h12')
    # net.iperf( hosts = (h2, h4), l4Type='UDP', udpBw='1000M', seconds=100000, port = 5999 )
    # net.iperf( hosts = (h6, h8), l4Type='UDP', udpBw='1000M', seconds=100000, port = 5999 )
    # net.iperf( hosts = (h10, h12), l4Type='UDP', udpBw='1000M', seconds=100000, port = 5999 )
    
    CLI.do_sh(net, 'sleep 30')

    #Batch command execution for video streaming
    video_test = "/home/ubuntu/cloud-sdn/scenario_testing/fat-tree/QoS-Test/mono/QoS-test_monolith-video.sh"
    CLI(net, script=video_test)

    #Batch command execution for Web
    web_test = "/home/ubuntu/cloud-sdn/scenario_testing/fat-tree/QoS-Test/mono/QoS-test_monolith-web.sh"
    CLI(net, script=web_test)

    #Batch command execution for VoIP
    voip_test = "/home/ubuntu/cloud-sdn/scenario_testing/fat-tree/QoS-Test/mono/QoS-test_monolith-voip.sh"
    CLI(net, script=voip_test)

    #Manual CLI
    CLI(net)
    net.stop()