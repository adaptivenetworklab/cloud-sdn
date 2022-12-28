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
        voip_link_config = {"bw": 5}
        video_link_config = {"bw": 10}
        host_link_config = {}

        # Create switch nodes
        for i in range(15):
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), protocols="OpenFlow10", **sconfig)

        # Create host nodes
        for i in range(12):
            self.addHost("h%d" % (i + 1), **hconfig)

        # Add switch links
        self.addLink("s4", "s1", **http_link_config)
        self.addLink("s5", "s1", **http_link_config)
        self.addLink("s6", "s1", **http_link_config)
        self.addLink("s7", "s2", **http_link_config)
        self.addLink("s8", "s2", **http_link_config)
        self.addLink("s9", "s2", **http_link_config)
        self.addLink("s10", "s3", **http_link_config)
        self.addLink("s11", "s3", **http_link_config)
        self.addLink("s12", "s3", **http_link_config)

        # Add host links
        self.addLink("h1", "s4", **host_link_config)
        self.addLink("h2", "s4", **host_link_config)
        self.addLink("h3", "s5", **host_link_config)
        self.addLink("h4", "s5", **host_link_config)
        self.addLink("h5", "s5", **host_link_config)
        self.addLink("h6", "s6", **host_link_config)
        self.addLink("h7", "s6", **host_link_config)
        self.addLink("h8", "s7", **host_link_config)
        self.addLink("h9", "s7", **host_link_config)
        self.addLink("h10", "s8", **host_link_config)
        self.addLink("h11", "s8", **host_link_config)
        self.addLink("h12", "s8", **host_link_config)


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
    controller = RemoteController("c1", ip="localhost", port=6633)
    net.addController(controller)
    net.build()
    net.start()
    CLI(net)
    net.stop()