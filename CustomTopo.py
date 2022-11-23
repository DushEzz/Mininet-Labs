#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange, dumpNodeConnections
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel


class CustomTopo(Topo):
    """
    linkopts1 : параметр производительности для линков между коммутаторами
    core и aggregation
    linkopts2 : параметр производительности для линков между коммутаторами
    aggregation и edge
    linkopts3 : параметр производительности для линков между коммутаторами
    edge и хостом
    fanout : параметр fanout означающий число childs per node
    """

    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        Topo.__init__(self, **opts)

        core = self.addSwitch('core_ty1')

        # Вершина топологии
        for a in range(fanout):
            aggr = self.addSwitch('a%s' % (a + 1))

            # Добавляем свитч в топологию
            self.addLink(aggr, core, **linkopts1)

            # Связываем свитч этого уровня с кор-свичом, распаковываем настройки производительности
            for e in range(fanout):
                edge = self.addSwitch('e%s' % ((a * fanout + e) + 1))

                # Каждому а-свичу добавлем edge свитч
                self.addLink(edge, aggr, **linkopts2)

                for h in range(fanout):
                    host = self.addHost('h%s' % (((a * fanout + e) * fanout + h) + 1))
                    # Добавляем хосты
                    self.addLink(host, edge, **linkopts3)


def simple_test():
    print("1. --Задаем параметры")
    linkopts1 = {'bw': 50, 'delay': '5ms'}
    linkopts2 = {'bw': 30, 'delay': '10ms'}
    linkopts3 = {'bw': 10, 'delay': '15ms'}

    print("2. --Реализуем нашу топологию с праметрами")
    topo = CustomTopo(linkopts1, linkopts2, linkopts3, fanout=2)

    print("3. --Создаем сеть из нашей топологии ")
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    dumpNodeConnections(net.hosts)

    print("4. --Тестируем сеть ")
    net.pingAll()

    print("5. --Останавливаем")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
