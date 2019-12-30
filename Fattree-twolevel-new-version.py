from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import OVSSwitch, OVSKernelSwitch, Controller, RemoteController
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink

class FatTreeTopo(Topo):
    """
	A fat-tree normally consist of k-pods, each pod has two layers of k/2 k-port switches and (k/2)^2 servers.
	A fat tree build with k-port switches can support up to (k^3)/4 host.
	Each k-port edge switch in the lower layer is directly connected to (k/2) server and (k/2) k-port aggregation switches.
	Each k-port aggregation switch is further connected with (k/2) k-port core switches.
	There are (k/2)^2 k-port core switch, each core switch has one port connected to each k-pods. 
	The i-th port of any core switch is connected to pod i such that, the consecutive port of aggregation layer of each pod is connected to core switch on (k/2) stride. 
	fat tree with four hierarchical layers, including, from the bottom, hosts, edge switches, aggregation switches, and core switches.
    k : int The number of ports of the switches
    r : int The oversubscription ratio of blocking Fat-Tree
    """

    def __init__(self, k=6, r=1):
        "Create fat_tree topo."

        core = []  # core
        aggregation = []  # aggravate
        edge = []  # edge
        all_switch = []  # switch
        all_hosts = []  # hosts

        # Initialize topology
        Topo.__init__(self)

        # Create core nodes
        Core_SW = ((k // 2) ** 2) // r
        for i in xrange(Core_SW):
            sw = self.addSwitch('c{}'.format(i + 1),cls=OVSKernelSwitch)
            core.append(sw)
            all_switch.append(sw)

        # Create aggregation and edge nodes and connect them
        for pod in xrange(k):
            aggr_start_node = len(all_switch) + 1
            aggr_end_node = aggr_start_node + k // 2
            edge_start_node = aggr_end_node
            edge_end_node = edge_start_node + k // 2
            aggr_nodes = xrange(aggr_start_node, aggr_end_node)
            edge_nodes = xrange(edge_start_node, edge_end_node)
            for i in aggr_nodes:
                sw = self.addSwitch('a{}'.format(i),cls=OVSKernelSwitch)
                aggregation.append(sw)
                all_switch.append(sw)
	    for j in edge_nodes:
            	sw = self.addSwitch('e{}'.format(j),cls=OVSKernelSwitch)
             	edge.append(sw)
               	all_switch.append(sw)
            for aa in aggr_nodes:
                for ee in edge_nodes:
                    self.addLink( all_switch[aa - 1],  all_switch[ee - 1])

        # Connect core switches to aggregation switches
        for core_node in xrange(Core_SW):
            for pod in xrange(k):
                aggr_node = Core_SW + (core_node // ((k // 2) // r)) + (k * pod)
                self.addLink( all_switch[core_node],  all_switch[aggr_node])

        # Create hosts and connect them to edge switches
	count = 1
	host = []
        for sw in edge:
            for i in xrange(k / 2):
                host = self.addHost('h{}'.format(count))
                self.addLink(sw, host)
                count += 1

	hostNumber=(count-1)
	nodeslist = self.nodes()
	LengthOfNodeslist = len(nodeslist)

	print nodeslist
	print LengthOfNodeslist
	print hostNumber
	print nodeslist [LengthOfNodeslist - hostNumber] 
	print (LengthOfNodeslist - hostNumber) 

#topos = {'fattree': FatTreeTopo}


def simpleTest():
        "Create and test a simple network"
#       CONTROLLER_IP = ""
#        CONTROLLER_PORT = 6633
        
        topo = FatTreeTopo()
        net = Mininet(topo=topo, controller=None, host=CPULimitedHost, link=TCLink)
        net.addController( 'controller',controller=RemoteController,ip='107.170.38.22')
        net.start()
        net.pingAll()
#        net.pingAll()

#        cliout = client.cmd( 'iperf -c ' + server.IP() + ' -n %d' % nbytes )
#        server.sendInt()
        

#        loghost = "h"
#        y=2
#        loghost+=str(y)
#        loghost = net.get(loghost)
#        loghost.sendCmd('./ITGLog')
#        print loghost

        hosts = net.hosts
        print hosts

        popens = {}
        print popens
        for h in hosts:
            print '1'
            print h
            popens[ h ] = h.popen('./ITGRecv')

        

#        for h in hosts[:4]:
#            print '2'
#            print h
#            h.cmd('./ITGSend singleflow-1000-script_file -l send_log_file -L 10.0.0.2 UDP -X 10.0.0.2 UDP -x recv_log_file')
#            result = h.waitOutput()
#            print result


# reciever hosts

#        recvhostnumber = 3
#        for i in range(3,recvhostnumber+1):
#            print i
#            rhost = "h"
#            rhost+=str(i)
#            print rhost
#            rhost = net.get(rhost)
#            rhost.sendCmd('./ITGRecv')
#            recvhost.append(rhost)
#            print rhost
#            print recvhost

#            if i== (recvhostnumber-2):
#                senderhost = "h"
#                x=1
#                senderhost+=str(x)
#                senderhost = net.get(senderhost)
#                print senderhost
#                senderhost.sendCmd('./ITGSend -a 10.0.0.3 -rp 9501 -C 1000 -u 500 1000 -l send_log_file -L 10.0.0.2 UDP -X 10.0.0.2 UDP -x recv_log_file')
#                result1=senderhost.waitOutput()
#                print result1
#                CLI(net)
 # log hosts       
 # send hosts               

#        print IntrResult
#        commandAnalys = './ITGDec recv_log_file >> reciverLog1'
#        result1=senderhost.cmd('ifconfig')
#        resultO = recieverhost.waitOutput()
#        print result1
#        recieverhost.waitOutput()

        CLI(net)
        net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
