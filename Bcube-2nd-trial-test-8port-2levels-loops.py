#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call


def myNetwork():
    net = Mininet(topo=None,
                  build=False,
                  ipBase='10.0.0.0/8')

    info('*** Adding controller\n')
    c0 = net.addController(name='c0', controller=RemoteController, ip='107.170.56.111', protocol='tcp', port=6633)

    info('*** Add switches\n')
    s = []
    h = []
    l = []

#    host_num = num_port**(num_level) = 64
#    switch_num_edge = num_port**(num_level) = 64
#    switch_num_level_1 = num_port**(num_level-1) = 16

    host_num = 64
    switch_num_edge = 64
    switch_num_level_1 = 8
    switch_num_level_2 = 8
    all_switch_count = switch_num_level_1 + switch_num_level_2 + switch_num_edge
    
    for i in xrange(all_switch_count):
        sw = net.addSwitch('s{}'.format(i + 1), cls=OVSKernelSwitch)
        s.append(sw.name)
    print s

    info('*** Add hosts\n')
    for i in xrange(host_num):
        host = net.addHost('h{}'.format(i + 1), cls=Host, defaultRoute=None)
        h.append(host.name)
    print h

    info('*** Add links\n')
    y = 0
    for j in xrange(64, 72):
        print 'y =', y
        for x in xrange(8):
            print 'x=', x
            net.addLink(s[j], s[x + y])
            print s[j], '-->', s[x + y]
            l.append('(s{}'.format(j + 1) + ',s{})'.format(y + x + 1))
        y += 8

    y = 0
    for j in xrange(72, 80):
        for x in xrange(0, 64, 8):
            net.addLink(s[j], s[y + x])
            l.append('(s{}'.format(j + 1) + ',s{})'.format(y + x + 1))
        y += 1

    for i in xrange(64):
        Link = net.addLink(s[i], h[i])
        l.append('(s{}'.format(i + 1) + ',h{})'.format(i + 1))
    print l

    info('*** Starting network\n')
    net.build()
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    for i in xrange(80):
        net.get(s[i]).start([c0])

    info('*** Post configure switches and hosts\n')

#    net.pingAll()

    loghost = "h"
    y = 2
    loghost += str(y)
    loghost = net.get(loghost)
    loghost.sendCmd('./ITGLog')
    print loghost

    hosts = net.hosts
    print hosts
    popens = {}
    print popens
    for h in hosts:
        print '1'
        print h
        popens[h] = h.popen('./ITGRecv')

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
