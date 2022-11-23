#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange, dumpNodeConnections
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel


class CustomTopo(Topo):
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        Topo.__init__(self, **opts)

        core = self.addSwitch('core_ty1')

        for a in range(fanout):
            aggr = self.addSwitch('a%s' % (a + 1))
            self.addLink(aggr, core, **linkopts1)

            for e in range(fanout):
                edge = self.addSwitch('e%s' % ((a * fanout + e) + 1))
                self.addLink(edge, aggr, **linkopts2)

                for h in range(fanout):
                    host = self.addHost('h%s' % (((a * fanout + e) * fanout + h) + 1))
                    self.addLink(host, edge, **linkopts3)


def simple_test():
    print("1. --Set parameters")
    linkopts1 = {'bw': 50, 'delay': '5ms'}
    linkopts2 = {'bw': 30, 'delay': '10ms'}
    linkopts3 = {'bw': 10, 'delay': '15ms'}

    print("2. --Realising our topology with parameters")
    topo = CustomTopo(linkopts1, linkopts2, linkopts3, fanout=2)

    print("3. --Creating a network from our topology")
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    dumpNodeConnections(net.hosts)

    print("4. --Testing the network")
    net.pingAll()

    print("5. --Stopping")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    simple_test()
