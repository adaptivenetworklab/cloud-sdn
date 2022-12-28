from mininet.cli import CLI
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch

# Create a Mininet object and add the controllers
net = Mininet()
c0 = net.addController()

# Create the switches
s1 = net.addSwitch('s1', cls=OVSSwitch)
s2 = net.addSwitch('s2', cls=OVSSwitch)
s3 = net.addSwitch('s3', cls=OVSSwitch)
s4 = net.addSwitch('s4', cls=OVSSwitch)
s5 = net.addSwitch('s5', cls=OVSSwitch)
s6 = net.addSwitch('s6', cls=OVSSwitch)
s7 = net.addSwitch('s7', cls=OVSSwitch)
s8 = net.addSwitch('s8', cls=OVSSwitch)
s9 = net.addSwitch('s9', cls=OVSSwitch)
s10 = net.addSwitch('s10', cls=OVSSwitch)
s11 = net.addSwitch('s11', cls=OVSSwitch)
s12 = net.addSwitch('s12', cls=OVSSwitch)
s13 = net.addSwitch('s13', cls=OVSSwitch)
s14 = net.addSwitch('s14', cls=OVSSwitch)
s15 = net.addSwitch('s15', cls=OVSSwitch)

# Create the hosts
h1 = net.addHost('h1')
h2 = net.addHost('h2')
h3 = net.addHost('h3')
h4 = net.addHost('h4')
h5 = net.addHost('h5')
h6 = net.addHost('h6')
h7 = net.addHost('h7')
h8 = net.addHost('h8')
h9 = net.addHost('h9')
h10 = net.addHost('h10')
h11 = net.addHost('h11')
h12 = net.addHost('h12')

# Connect the switches to the controllers
net.addLink(s1, c0)
net.addLink(s2, c0)
net.addLink(s3, c0)

# Connect the aggregation switches to the core switches
net.addLink(s4, s1)
net.addLink(s5, s1)
net.addLink(s6, s1)
net.addLink(s7, s2)
net.addLink(s8, s2)
net.addLink(s9, s2)
net.addLink(s10, s3)
net.addLink(s11, s3)
net.addLink(s12, s3)

# Connect the hosts to the aggregation switches
net.addLink(h1, s4)
net.addLink(h2, s4)
net.addLink(h3, s5)
net.addLink(h4, s5)
net.addLink(h5, s5)
net.addLink(h6, s6)
net.addLink(h7, s6)
net.addLink(h8, s7)
net.addLink(h9, s7)
net.addLink(h10, s8)
net.addLink(h11, s8)
net.addLink(h12, s8)

# Set the link parameters
net.configLinkStatus('s1', 's4', 'down')
net.configLinkStatus('s1', 's5', 'down')
net.configLinkStatus('s1', 's6', 'down')
net.configLinkStatus('s2', 's7', 'down')
net.configLinkStatus('s2', 's8', 'down')
net.configLinkStatus('s2', 's9', 'down')
net.configLinkStatus('s3', 's10', 'down')
net.configLinkStatus('s3', 's11', 'down')
net.configLinkStatus('s3', 's12', 'down')

# Start the Mininet network
net.start()

# Enter the Mininet CLI
CLI(net)

# Stop the Mininet network
net.stop()