"""Example Topology Manager Template
CSCI1680

This class is meant to serve as an example for how you can track the
network's topology from netwokr events.

**You are not required to use this file**: feel free to extend it,
change its structure, or replace it entirely.

"""

from ryu.topology.switches import Port, Switch, Link
import queue

class Device():
    """Base class to represent an device in the network.

    Any device (switch or host) has a name (used for debugging only)
    and a set of neighbors.
    """
    def __init__(self, name):
        self.name = name
        self.neighbors = []

    def add_neighbor(self, dev):
        self.neighbors.append(dev)
    
    def remove_neighbor(self,dev):
        self.neighbors.remove(dev)

    def get_neighbor(self,dev):
        return self.neighbors
    # . . .
    def get_neighbors(self):
        return self.neighbors
    def __str__(self):
        return "{}({})".format(self.__class__.__name__,
                               self.name)


class TMSwitch(Device):
    """Representation of a switch, extends Device

    This class is a wrapper around the Ryu Switch object,
    which contains information about the switch's ports
    """

    def __init__(self, name,dpid, switch):
        super(TMSwitch, self).__init__(name)
        self.switch = switch
        self.dpid=dpid
        self.host=set()
        # TODO:  Add more attributes as necessary
    def BFS_2(self,switches):
        print("BFS2 begin")
        switches_list=[]
        switch_queue=queue.Queue()
        switches_port = []
        willreturn = []
        for i in switches:
            #print(type(i)) 
            switches_list.append(i)
        for i in self.neighbors:
            if type(i[0]) == type(self):
                switch_queue.put(i)
                switches_list.remove(i[0])
        switches_list.remove(self)
        while switch_queue.empty() is False:
            head = switch_queue.get()
            #print(head[0].name)
            #print(type(head[0]))
            #switches_list.remove(head[0])    
            switches_port.append(head)     
            port=head[1]
            #print("outer {}".format(head[0].name))
            for j in head[0].neighbors:
                #print(j[0].name)
                if j[0] in switches_list:
                    switch_queue.put((j[0],port))
                    switches_list.remove(j[0])
        #return switches_port
        for i in self.host:
            port=i.host.port.port_no
            willreturn.append((i,port))
        for i in switches_port:
            port=i[1]
            for j in i[0].host:
                willreturn.append((j,port))
        print("BFS2 end")
        return willreturn
    def add_host(self,h):
        host=TMHost("host",h.mac,h)
        self.host.add(host)
        return host
    def get_dpid(self):
        """Return switch DPID"""
        return self.dpid

    def get_ports(self):
        """Return list of Ryu port objects for this switch
        """
        return self.switch.ports

    def get_dp(self):
        """Return switch datapath object"""
        return self.switch.dp
            
    # . . . 

class TMHost(Device):
    """Representation of a host, extends Device

    This class is a wrapper around the Ryu Host object,
    which contains information about the switch port to which
    the host is connected
    """

    def __init__(self, name,mac, host):
        super(TMHost, self).__init__(host)
        self.mac=mac
        self.host = host
        # TODO:  Add more attributes as necessary

    def get_mac(self):
        return self.mac

    def get_ips(self):
        return self.host.ipv4

    def get_port(self):
        """Return Ryu port object for this host"""
        return self.host.port

    # . . .


class TopoManager():
    """
    Example class for keeping track of the network topology

    """
    def __init__(self):
        # TODO:  Initialize some data structures
        #self.all_devices = []
        self.switches = set()
        self.hostes = set()
        pass
    
    def add_switch(self, sw):
        name = "switch_{}".format(sw.dp.id)
        switch = TMSwitch(name,sw.dp.id, sw)
        
        #self.all_devices.append(switch)
        self.switches.add(switch)
        # TODO:  Add switch to some data structure(s)

    def add_host(self, h):
        name = "host_{}".format(h.mac)
        host = TMHost(name, h.mac,h)
        self.hostes.add(host)
        #self.all_devices.append(host)
        return host

    def remove_switch (self,sw):
        switch_temp= self.get_switches_dpid(sw)
        if self.get_switches_dpid(sw) is None:
            return
        else:
            self.switches.remove(self.get_switches_dpid(sw))
            remove_switch = None
            for i in self.switches:
                for j in i.get_neighbors():
                    # if j[0].name[0:6] != "switch":
                    if type(j[0]) != type(switch_temp):
                        continue
                    else:
                        if j[0].get_dpid()== sw:
                          remove_switch = j
                          break
                if remove_switch in i.neighbors:
                    i.neighbors.remove
                    (remove_switch)
        # TODO:  Add host to some data structure(s)
    
    def remove_host (self,sw):
        if self.get_switches_dpid(sw) is None:
            return
        else:
            self.switches.remove(self.get_switches_dpid(sw))
            remove_switch = None
            for i in self.switches:
                for j in i.get_neighbors():
                    if j[0].name[0:6] != "switch":
                        continue
                    else:
                        if j[0].get_dpid()== sw:
                          remove_switch = j
                          break
                i.neighbors.remove(remove_switch)
        # TODO:  Add host to some data structure(s)    
    def get_switches_dpid(self,switch_in):
        for i in self.switches:
            if i.get_dpid() == switch_in:
                return i
        return None
           

    # . . .
