from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topo import Topo
from mininet.topo.topolib import FatTree

# Create a FatTree topology with 3 core switches, 6 aggregate switches, and 6 edge switches
topo = FatTree(k=3, speed=1, bw=10, delay='1ms', loss=0, max_queue_size=None, cores=3, aggrs=6, edges=6)

# Create a Mininet network with the topology and a remote controller
net = Mininet(topo=topo, controller=RemoteController)

# Start the Mininet network
net.start()

# Get the list of hosts in the network
hosts = net.hosts

# Connect each host to a separate edge switch
for i in range(12):
    hosts[i].linkTo(net.switches[6+i])

# Test connectivity between all hosts
net.pingAll()

# Measure network performance
net.iperf()

# Stop the Mininet network
net.stop()

