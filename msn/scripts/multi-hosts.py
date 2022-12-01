from mininet.topo import Topo
class MyTopo( Topo ):
    "Simple topology example."
    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        Host1 = self.addHost('h1')
        Host2 = self.addHost('h2')
        Host3 = self.addHost('h3')
        Host4 = self.addHost('h4')
        Host5 = self.addHost('h5')
        Host6 = self.addHost('h6')
        Host7 = self.addHost('h7')
        Host8 = self.addHost('h8')
        Host9 = self.addHost('h9')
        Host10 = self.addHost('h10')
        Switch1 = self.addSwitch('s1')
        Switch2 = self.addSwitch('s2')
        Switch3 = self.addSwitch('s3')
        Switch4 = self.addSwitch('s4')
        Switch5 = self.addSwitch('s5')
        # Add links
        self.addLink( Host1, Switch1 )
        self.addLink( Host2, Switch1 )
        self.addLink( Host3, Switch2 )
        self.addLink( Host4, Switch2 )
        self.addLink( Host5, Switch3 )
        self.addLink( Host6, Switch3 )
        self.addLink( Host7, Switch4 )
        self.addLink( Host8, Switch4 )
        self.addLink( Host9, Switch5 )
        self.addLink( Host10, Switch5 )
        self.addLink( Switch1, Switch2 )
        self.addLink( Switch2, Switch3 )
        self.addLink( Switch3, Switch4 )
        self.addLink( Switch4, Switch5 )
topos = { 'mytopo': ( lambda: MyTopo() ) }

