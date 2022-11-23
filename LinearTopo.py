#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange, dumpNodeConnections
from mininet.log import setLogLevel


class LinearTopo(Topo):
    """Linear topology of k switches, with one host per switch."""

    def __init__(self, k=2, **opts):
        """
        Init.
        k: number of switches (and hosts)
        hconf: host configuration options
        lconf: link configuration options
        """
    
        super(LinearTopo, self).__init__(**opts)
    
        self.k = k
    
        lastSwitch = None
        for i in irange(1, k):
            host = self.addHost('h%s' % i, cpu=.5/k)
            switch = self.addSwitch('s%s' % i)
            self.addLink(host, switch)
            
            if lastSwitch:
                self.addLink(switch, lastSwitch, bw=10, delay='5ms', loss=1,max_queue_size=1000, use_htb=True)
            lastSwitch = switch


def perfTest():
    """Create network and run simple performance test"""

    topo = LinearTopo(k=4)
    net = Mininet(topo=topo)
    net.start()

    print("Dumping host connections")
    dumpNodeConnections(net.hosts)

    print("Testing network connectivity")
    net.pingAll()
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    perfTest()
