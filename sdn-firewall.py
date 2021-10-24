#!/usr/bin/python

# CS 6250 Fall 2021 - SDN Firewall Project with POX
# build habit-v23

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from pox.lib.revent import *
from pox.lib.addresses import IPAddr, EthAddr

# You may use this space before the firewall_policy_processing function to add any extra function that you 
# may need to complete your firewall implementation.  No additional functions "should" be required to complete
# this assignment.


def firewall_policy_processing(policies):
    '''
    This is where you are to implement your code that will build POX/Openflow Match and Action operations to
    create a dynamic firewall meeting the requirements specified in your configure.pol file.  Do NOT hardcode
    the IP/MAC Addresses/Protocols/Ports that are specified in the project description - this code should use
    the values provided in the configure.pol to implement the firewall.

    The policies passed to this function is a list of dictionary objects that contain the data imported from the
    configure.pol file.  The policy variable in the "for policy in policies" represents a single line from the
    configure.pol file.  Each of the configuration values are then accessed using the policy['field'] command. 
    The fields are:  'rulenum','action','mac-src','mac-dst','ip-src','ip-dst','ipprotocol','port-src','port-dst',
    'comment'.

    Your return from this function is a list of flow_mods that represent the different rules in your configure.pol file.

    Implementation Hints:
    The documentation for the POX controller is available at https://noxrepo.github.io/pox-doc/html .  This project
    is using the gar-experimental branch of POX in order to properly support Python 3.  To complete this project, you
    need to use the OpenFlow match and flow_modification routines (https://noxrepo.github.io/pox-doc/html/#openflow-messages
    for flow_mod and https://noxrepo.github.io/pox-doc/html/#match-structure for match.)  Also, do NOT wrap IP Addresses with
    IPAddr() unless you reformat the CIDR notation.  Look at the https://github.com/att/pox/blob/master/pox/lib/addresses.py
    for what POX is expecting as an IP Address.
    '''

    rules = []
    import pdb

    for policy in policies:
        # Enter your code here to implement matching and block/allow rules.  See the links
        # in Implementation Hints on how to do this. 
        # HINT:  Think about how to use the priority in your flow modification.

        
        rule = None # Please note that you need to redefine this variable below to create a valid POX Flow Modification Object
        print("this is a test")
        rule = of.ofp_flow_mod()
        if policy['action'] == "Allow":
            rule.priority = 3000
            action_port = of.OFPP_NORMAL
        else:
            rule.priority = 1
            action_port = 4
        rule.match.dl_type=0X800

        if policy['ip-src'] != "-":
            rule.match.nw_src = policy['ip-src']
        if policy['ip-dst'] != "-":
            rule.match.nw_dst = policy['ip-dst']
        if policy['ipprotocol'] != "-":
            rule.match.nw_proto = int(policy['ipprotocol'])
        if policy['port-src'] != "-":
            rule.match.tp_src = int(policy['port-src'])
        if policy['port-dst'] != "-":
            rule.match.tp_dst = int(policy['port-dst'])



        #rule.match.nw_src = IPAddr('10.0.0.2')
        #rule.match.nw_dst = IPAddr('10.0.1.1')
        #rule.match.tp_dst = 80
        rule.actions.append(of.ofp_action_output(port=action_port))


        # End Code Here
        print('Added Rule ',policy['rulenum'],': ',policy['comment'])
        #print(rule)   #Uncomment this to debug your "rule"
        rules.append(rule)
    #from pprint import pprint
    #for rule in rules:
    #    pprint(vars(rule))
    #    pprint(vars(rule.match))
    #pdb.set_trace()
    return rules
