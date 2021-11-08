#!/usr/bin/env python
# Copyright 2021
# Georgia Tech
# All rights reserved
# Do not post or publish in any public or forbidden forums or websites


from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import lg, info, setLogLevel
from mininet.util import dumpNodeConnections, quietRun, moveIntf
from mininet.cli import CLI
from mininet.node import Switch, OVSKernelSwitch

from subprocess import Popen, PIPE, check_output
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser

import sys
import os
import termcolor as T
import time

setLogLevel('info')

parser = ArgumentParser("Configure simple BGP network in Mininet.")
parser.add_argument('--rogue', action="store_true", default=False)
parser.add_argument('--scriptfile', default=None)
parser.add_argument('--sleep', default=3, type=int)
args = parser.parse_args()

FLAGS_rogue_as = args.rogue
ROGUE_AS_NAME = 'R6'

def log(s, col="green"):
    print(T.colored(s, col))


class Router(Switch):
    """Defines a new router that is inside a network namespace so that the
    individual routing entries don't collide.

    """
    ID = 0
    def __init__(self, name, **kwargs):
        kwargs['inNamespace'] = True
        Switch.__init__(self, name, **kwargs)
        Router.ID += 1
        self.switch_id = Router.ID

    @staticmethod
    def setup():
        return

    def start(self, controllers):
        pass

    def stop(self):
        self.deleteIntfs()

    def log(self, s, col="magenta"):
        print(T.colored(s, col))


class SimpleTopo(Topo):
    """The Autonomous System topology is a simple straight-line topology
    between AS1 -- AS2 -- AS3.  The rogue AS (AS4) connects to AS1 directly.

    """
    def __init__(self):
        # Add default members to class.
        super(SimpleTopo, self ).__init__()
        num_hosts_per_as = 2
        num_ases = 5
        num_hosts = num_hosts_per_as * num_ases
        # The topology has one router per AS
        routers = []
        for i in range(num_ases):
            router = self.addSwitch('R%d' % (i+1))
        routers.append(router)
        hosts = []
        for i in range(num_ases):
            router = 'R%d' % (i+1)
            for j in range(num_hosts_per_as):
                hostname = 'h%d-%d' % (i+1, j+1)
                host = self.addNode(hostname)
                hosts.append(host)
                self.addLink(router, host)

        self.addLink('R1', 'R2')
        self.addLink('R1', 'R3')
        self.addLink('R2', 'R3')
        self.addLink('R2', 'R4')
        self.addLink('R2', 'R5')
        self.addLink('R3', 'R4')
        self.addLink('R3', 'R5')
        self.addLink('R4', 'R5')
        routers.append(self.addSwitch('R6'))
        for j in range(num_hosts_per_as):
            hostname = 'h%d-%d' % (6, j+1)
            host = self.addNode(hostname)
            hosts.append(host)
            self.addLink('R6', hostname)
        # This MUST be added at the end
        self.addLink('R6', 'R5')
        return


def getIP(hostname):
    AS, idx = hostname.replace('h', '').split('-')
    AS = int(AS)
    if AS == 6:
        AS = 1
    ip = '%s.0.%s.1/24' % (10+AS, idx)
    return ip


def getGateway(hostname):
    AS, idx = hostname.replace('h', '').split('-')
    AS = int(AS)
    # This condition gives AS4 the same IP range as AS3 so it can be an
    # attacker.
    if AS == 6:
        AS = 1
    gw = '%s.0.%s.254' % (10+AS, idx)
    return gw


def startWebserver(net, hostname, text="Default web server 2.1.1"):
    host = net.getNodeByName(hostname)
    return host.popen("python webserver.py --text '%s'" % text, shell=True)


def main():
    os.system("rm -f /tmp/R*.log /tmp/R*.pid logs/*")
    os.system("mn -c >/dev/null 2>&1")
    os.system("pkill -9 bgpd > /dev/null 2>&1")
    os.system("pkill -9 zebra > /dev/null 2>&1")
    os.system('pkill -9 -f webserver.py')

    import pdb
    pdb.set_trace()
    pdb.set_trace()
    net = Mininet(topo=SimpleTopo(), switch=Router)
    net.start()
    for router in net.switches:
        router.cmd("sysctl -w net.ipv4.ip_forward=1")
        router.waitOutput()

    log("Waiting %d seconds for sysctl changes to take effect..."
        % args.sleep)
    sleep(args.sleep)

    for router in net.switches:
        if router.name == ROGUE_AS_NAME and not FLAGS_rogue_as:
            continue
        router.cmd("ip link set dev lo up ")
        router.waitOutput()
        router.cmd("/usr/lib/frr/zebra -f conf/zebra-%s.conf -d -i /tmp/zebra-%s.pid > logs/%s-zebra-stdout 2>&1" % (router.name, router.name, router.name))
        router.waitOutput()
        router.cmd("/usr/lib/frr/bgpd -f conf/bgpd-%s.conf -d -i /tmp/bgp-%s.pid > logs/%s-bgpd-stdout 2>&1" % (router.name, router.name, router.name), shell=True)
        router.waitOutput()
        log("Starting zebra and bgpd on %s" % router.name)

    for host in net.hosts:
        host.cmd("ifconfig %s-eth0 %s" % (host.name, getIP(host.name)))
        host.cmd("route add default gw %s" % (getGateway(host.name)))

    log("Starting web servers", 'yellow')
    startWebserver(net, 'h1-1', "Default web server 2.1.1")
    startWebserver(net, 'h6-1', "*** Attacker web server 2.1.1***")

    CLI(net, script=args.scriptfile)
    net.stop()
    os.system("pkill -9 bgpd")
    os.system("pkill -9 zebra")
    os.system('pkill -9 -f webserver.py')


if __name__ == "__main__":
    main()
