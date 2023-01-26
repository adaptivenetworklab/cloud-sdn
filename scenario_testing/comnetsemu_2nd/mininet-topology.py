#! /usr/bin/env python3
# -*- coding: utf-8 -*-

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
        host_link_config = {}

        for i in range(8):
            self.addHost("h%d" % (i + 1), ip="10.0.0.%d" % (i + 1), **hconfig) 

        for i in range(7):
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), protocols="OpenFlow10", **sconfig)

        # s1 = net.addSwitch("s1")
        # s2 = net.addSwitch("s2")
        # s3 = net.addSwitch("s3")
        # s4 = net.addSwitch("s4")
        # s5 = net.addSwitch("s5")
        # s6 = net.addSwitch("s6")
        # s7 = net.addSwitch("s7")

        # Add switch links
        self.addLink("s1", "s3", **http_link_config)
        self.addLink("s1", "s4", **http_link_config)
        self.addLink("s2", "s4", **http_link_config)
        self.addLink("s2", "s5", **http_link_config)
        self.addLink("s3", "s6", **http_link_config)
        self.addLink("s4", "s6", **http_link_config)
        self.addLink("s4", "s7", **http_link_config)
        self.addLink("s5", "s7", **http_link_config)

        # Add host links
        self.addLink("h1", "s1", **host_link_config)
        self.addLink("h2", "s1", **host_link_config)
        self.addLink("h3", "s2", **host_link_config)
        self.addLink("h4", "s2", **host_link_config)
        self.addLink("h5", "s6", **host_link_config)
        self.addLink("h6", "s6", **host_link_config)
        self.addLink("h7", "s7", **host_link_config)
        self.addLink("h8", "s7", **host_link_config)

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
    controller = RemoteController("c1", ip="10.244.2.26", port=6633)
    net.addController(controller)
    net.build()
    net.start()
    CLI(net)
    net.stop()