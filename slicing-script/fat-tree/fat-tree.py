#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI

class FatTreeTopo(Topo):
    "Fat Tree Topology"

    def __init__(self, k=4, **opts):
        # Initialize topology and default option
        Topo.__init__(self, **opts)

        # Create k-ary tree
        self.createFatTree(k)

    def createFatTree(self, k):
        # Create core layer
        coreSwitches = []
        for i in range(int(k**2 / 4)):
            coreSwitches.append(self.addSwitch('c%d' % (i + 1)))

        # Create aggregation layer
        aggSwitches = []
        for i in range(int(k**2 / 2)):
            aggSwitches.append(self.addSwitch('a%d' % (i + 1)))

        # Create edge layer
        edgeSwitches = []
        for i in range(int(k**2 / 2)):
            edgeSwitches.append(self.addSwitch('e%d' % (i + 1)))

        # Connect core switches to aggregation switches
        for i in range(int(k**2 / 4)):
            for j in range(int(k**2 / 2)):
                self.addLink(coreSwitches[i], aggSwitches[j])

        # Connect aggregation switches to edge switches
        for i in range(int(k**2 / 2)):
            for j in range(int(k**2 / 2)):
                self.addLink(aggSwitches[i], edgeSwitches[j])

        # Create hosts and connect them to edge switches
        for i in range(int(k**3 / 4)):
            host = self.addHost('h%d' % (i + 1))
            self.addLink(edgeSwitches[int(i / (k / 2))], host)

# def testFatTree():
#     "Create and test a fat tree topology"
#     topo = FatTreeTopo(k=4)
#     net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
#     net.start()
#     print ("Dumping host connections")
#     dumpNodeConnections(net.hosts)
#     print ("Testing network connectivity")
#     net.pingAll()
#     net.stop()

# if __name__ == '__main__':
#     setLogLevel('info')
#     testFatTree()

if __name__ == "__main__":
    topo = FatTreeTopo(k=4)
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