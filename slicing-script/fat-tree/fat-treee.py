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
        http_link_config = {"bw": 1}
        email_link_config = {"bw": 0.5}
        video_link_config = {"bw": 3}
        host_link_config = {}

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
        self.addLink("s4", "s1", **http_link_config)
        self.addLink("s5", "s1", **http_link_config)
        self.addLink("s6", "s1", **http_link_config)
        self.addLink("s7", "s1", **http_link_config)
        self.addLink("s8", "s1", **http_link_config)
        self.addLink("s9", "s1", **http_link_config)
        self.addLink("s7", "s2", **http_link_config)
        self.addLink("s8", "s2", **http_link_config)
        self.addLink("s9", "s2", **http_link_config)
        self.addLink("s4", "s2", **http_link_config)
        self.addLink("s5", "s2", **http_link_config)
        self.addLink("s6", "s2", **http_link_config)
        self.addLink("s4", "s3", **http_link_config)
        self.addLink("s5", "s3", **http_link_config)
        self.addLink("s6", "s3", **http_link_config)
        self.addLink("s7", "s3", **http_link_config)
        self.addLink("s8", "s3", **http_link_config)
        self.addLink("s9", "s3", **http_link_config)
        self.addLink("s10", "s4", **http_link_config)
        self.addLink("s11", "s4", **http_link_config)
        self.addLink("s10", "s5", **http_link_config)
        self.addLink("s11", "s5", **http_link_config)
        self.addLink("s12", "s5", **http_link_config)
        self.addLink("s11", "s6", **http_link_config)
        self.addLink("s12", "s6", **http_link_config)
        self.addLink("s13", "s6", **http_link_config)
        self.addLink("s12", "s7", **http_link_config)
        self.addLink("s13", "s7", **http_link_config)
        self.addLink("s14", "s7", **http_link_config)
        self.addLink("s13", "s8", **http_link_config)
        self.addLink("s14", "s8", **http_link_config)
        self.addLink("s15", "s8", **http_link_config)
        self.addLink("s14", "s9", **http_link_config)
        self.addLink("s15", "s9", **http_link_config)

        # Add host links
        self.addLink("h1", "s10", **host_link_config)
        self.addLink("h2", "s10", **host_link_config)
        self.addLink("h3", "s11", **host_link_config)
        self.addLink("h4", "s11", **host_link_config)
        self.addLink("h5", "s12", **host_link_config)
        self.addLink("h6", "s12", **host_link_config)
        self.addLink("h7", "s13", **host_link_config)
        self.addLink("h8", "s13", **host_link_config)
        self.addLink("h9", "s14", **host_link_config)
        self.addLink("h10", "s14", **host_link_config)
        self.addLink("h11", "s15", **host_link_config)
        self.addLink("h12", "s15", **host_link_config)


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
    controller = RemoteController("c1", ip="10.0.2.207", port=6633)
    net.addController(controller)
    net.build()
    net.start()
    CLI(net)
    net.stop()
