#!/usr/bin/env python3

"""Shortest Path Switching template
CSCI1680

This example creates a simple controller application that watches for
topology events.  You can use this framework to collect information
about the network topology and install rules to implement shortest
path switching.

"""

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0

from ryu.topology import event, switches
import ryu.topology.api as topo

from ryu.lib.packet import packet, ether_types
from ryu.lib.packet import ethernet, arp, icmp

from ofctl_utils import OfCtl, VLANID_NONE

from topo_manager_example import TopoManager


class ShortestPathSwitching(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(ShortestPathSwitching, self).__init__(*args, **kwargs)

        self.tm = TopoManager()
    def add_forwarding_rule(self, datapath, dl_dst, port):
        ofctl = OfCtl.factory(datapath, self.logger)
        actions = [datapath.ofproto_parser.OFPActionOutput(port)] 
        ofctl.set_flow(cookie=0, priority=0,
                dl_type=ether_types.ETH_TYPE_IP,
                dl_vlan=VLANID_NONE,
                dl_dst=dl_dst,
                actions=actions)
      
    def BFS_1(self):
        mac_infos = []
        for i in self.tm.switches:
            tables = i.BFS_2(self.tm.switches)
            self.logger.warn("switches {} length is {}".format(i.dpid,len(tables)))
            for j in tables:
                self.add_forwarding_rule(i.switch.dp,j[0].mac,j[1])
                self.logger.warn("switch:{} ,Mac:{} port:{}".format(i.dpid,j[0].mac,j[1]))
                mac_infos.append((i.dpid,j[0].mac,j[1]))
        self.logger.warn("BFS 1 finish")
        
        begin = []
        end = []
        for i in self.tm.hostes:
            begin.append(i)
            end.append(i)
        for i in begin:
            for j in end:
                if i.mac == j.mac:
                    continue
                else:
                    print("1 {}".format(i.name))
                    begin_switch=i.get_neighbors()[0][0]
                    next_switch =i.get_neighbors()[0][0]
                    print(begin_switch.name)
                    while type(begin_switch) == type(next_switch):
                        begin_switch = next_switch
                        next_switch_port = None
                        for k in mac_infos:
                            if begin_switch.dpid == k[0] and j.mac == k[1]:
                                next_switch_port=k[2]
                                break
                        for k in begin_switch.get_neighbors():
                            if k[1] == next_switch_port:
                                print(k[0].name)
                                next_switch = k[0]
                                break
        print("shortest finish")                        
    
    
    def show_shortest_path(self):
        begin = []
        end = []
        for i in self.tm.hostes:
            begin.append(i)
            end.append(i)
        # for i in begin:
        #    for j in end:

        pass    
    @set_ev_cls(event.EventSwitchEnter)
    def handle_switch_add(self, ev):
        """
        switch加入,没有链接其他的
        Event handler indicating a switch has come online.
        """
        switch = ev.switch
        
        self.logger.warn("Added Switch switch%d with ports:", switch.dp.id)
        for port in switch.ports:
            self.logger.warn("\t%d:  %s", port.port_no, port.hw_addr)
        
        # TODO:  Update network topology and flow rules
        self.tm.add_switch(switch)
        self.BFS_1()
    @set_ev_cls(event.EventSwitchLeave)
    def handle_switch_delete(self, ev):
        """
        switch关闭,需要删除其本身和所有邻居
        Event handler indicating a switch has been removed
        """
        switch = ev.switch

        self.logger.warn("Removed Switch switch%d with ports:", switch.dp.id)
        for port in switch.ports:
            self.logger.warn("\t%d:  %s", port.port_no, port.hw_addr)
        self.tm.remove_switch(switch.dp.id)
        # TODO:  Update network topology and flow rules
        self.BFS_1()
    @set_ev_cls(event.EventHostAdd)
    def handle_host_add(self, ev):
        """
        host开启,加入列表
        Event handler indiciating a host has joined the network
        This handler is automatically triggered when a host sends an ARP response.
        """
        host = ev.host
        self.logger.warn("Host Added:  %s (IPs:  %s) on switch%s/%s (%s)",
                          host.mac, host.ipv4,
                         host.port.dpid, host.port.port_no, host.port.hw_addr)
        h = self.tm.add_host(host)
        self.logger.warn("host type is {}".format(type(h)))
        self.tm.get_switches_dpid(host.port.dpid).add_neighbor((h,host.port.port_no))
        self.tm.get_switches_dpid(host.port.dpid).add_host(host)
        # TODO:  Update network topology and flow rules
        h.add_neighbor((self.tm.get_switches_dpid(host.port.dpid),None))
        self.BFS_1()
        

    @set_ev_cls(event.EventLinkAdd) 
    def handle_link_add(self, ev):
        """
        switch1-switch2 连接上 
        Event handler indicating a link between two switches has been added
        """
        link = ev.link
        src_port = ev.link.src
        dst_port = ev.link.dst
        self.logger.warn("Added Link:  switch%s/%s (%s) -> switch%s/%s (%s)",
                         src_port.dpid, src_port.port_no, src_port.hw_addr,
                         dst_port.dpid, dst_port.port_no, dst_port.hw_addr)
        src_switch = self.tm.get_switches_dpid(src_port.dpid)
        dst_switch = self.tm.get_switches_dpid(dst_port.dpid)
        src_switch.add_neighbor((dst_switch,src_port.port_no))
        # TODO:  Update network topology and flow rules
        self.BFS_1()
    @set_ev_cls(event.EventLinkDelete)
    def handle_link_delete(self, ev):
        """
        switch1-switch2 连接关闭
        Event handler indicating when a link between two switches has been deleted
        """
        link = ev.link
        src_port = link.src
        dst_port = link.dst

        self.logger.warn("Deleted Link:  switch%s/%s (%s) -> switch%s/%s (%s)",
                          src_port.dpid, src_port.port_no, src_port.hw_addr,
                          dst_port.dpid, dst_port.port_no, dst_port.hw_addr)
        src_switch = self.tm.get_switches_dpid(src_port.dpid)
        dst_switch = self.tm.get_switches_dpid(dst_port.dpid)
        print(src_switch is None, dst_switch is None)
        if src_switch is not None and dst_switch is not None and dst_switch in src_switch.get_neighbors():
            src_switch.remove_neighbor(dst_switch)
        # TODO:  Update network topology and flow rules
        self.BFS_1()
    @set_ev_cls(event.EventPortModify)
    def handle_port_modify(self, ev):
        """
        switch-host
        Event handler for when any switch port changes state.
        This includes links for hosts as well as links between switches.
        """
        port = ev.port
        self.logger.warn("Port Changed:  switch%s/%s (%s):  %s,device name is %s",
                         port.dpid, 
                         port.port_no,
                         port.hw_addr,
                         "UP" if port.is_live() else "DOWN",
                         port.name)
        if port.is_live():
            pass
        else:
            if (port.port_no) > 1000:
                return
            src_switch = self.tm.get_switches_dpid(port.dpid)
            dst_switch = None
            for i in src_switch.get_neighbors():
                if (i[1] == port.port_no):
                    dst_switch = i[0]
            if dst_switch is None:
                return
            print(src_switch.name,dst_switch.name)
            for i in src_switch.get_neighbors():
                if i[0] == dst_switch:
                    print("src removed")
                    src_switch.remove_neighbor(i)
            for i in dst_switch.get_neighbors():
                if i[0] == src_switch:
                    print("dst  remove")
                    dst_switch.remove_neighbor(i)
            # if dst_switch in src_switch.get_neighbors():
            #    print("src removed")
            #    src_switch.remove_neighbor(dst_switch)
            # if src_switch in dst_switch.get_neighbors():
            #    print("src removed")    
            #    dst_switch.remove_neighbor(  src_switch )
        # TODO:  Update network topology and flow rules
            self.BFS_1()
        print("Port change success")
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        """
       EventHandler for PacketIn messages
        """
        msg = ev.msg

        # In OpenFlow, switches are called "datapaths".  Each switch gets its own datapath ID.
        # In the controller, we pass around datapath objects with metadata about each switch.
        dp = msg.datapath

        # Use this object to create packets for the given datapath
        ofctl = OfCtl.factory(dp, self.logger)

        in_port = msg.in_port
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_ARP:
            arp_msg = pkt.get_protocols(arp.arp)[0]

            if arp_msg.opcode == arp.ARP_REQUEST:
                self.logger.warning("Received ARP REQUEST on switch%d/%d:  Who has %s?  Tell %s,ip:%s,opcode:%s",
                                     dp.id, 
                                    in_port, 
                                    arp_msg.dst_ip, 
                                    arp_msg.src_mac,
                                    arp_msg.src_ip,
                                    arp_msg.opcode)
                self.logger.warning(arp_msg)
                """
        Generate an ARP packet and send it
        Arguments:
        arp_opcode    -- Opcode for message
        vlan_id       -- VLAN identifier, or VLANID_NONE
        dst_mac       -- Destination to send the packet (not an ARP field)
        sender_mac    -- Sender hardware address
        sender_ip     -- Sender protocol address
        target_mac    -- Target hardware address
        target_ip     -- Target protocol address
        src_port      -- Source port number for sending message (can be OFPP_CONTROLLER)
        output_port   -- Outgoing port number to send message
                """# src 出发,dst收尾
                reply_mac = None  
                for i in self.tm.hostes:
                    print(i.host.ipv4)
                    if i.host.ipv4[0] == arp_msg.dst_ip:
                        reply_mac = i.mac
                        break
                print("reply is {}".format(reply_mac))
                if reply_mac is None:
                    return
                else:
                    ofctl.send_arp(
                arp_opcode=2,
                vlan_id=VLANID_NONE,
                dst_mac=arp_msg.src_mac,
                sender_mac=reply_mac,
                sender_ip=arp_msg.dst_ip,
                target_mac=arp_msg.src_mac,
                target_ip=arp_msg.src_ip,
                src_port=ofctl.dp.ofproto.OFPP_CONTROLLER,
                #src_port=in_port,
                output_port=in_port)
                print("send finish") 
                for i in self.tm.switches:
                    for j in i.neighbors:
                        print(i.name,j[0].name,j[1])
                    # for j in i.host:
                        # print(i.name,j.name,j.host.port.port_no)
                self.BFS_1()
                # TODO:  Generate a *REPLY* for this request based on your switch state
               
                # Here is an example way to send an ARP packet using the ofctl utilities
                #ofctl.send_arp(vlan_id=VLANID_NONE,
                #               src_port=ofctl.dp.ofproto.OFPP_CONTROLLER,
                #               . . .)

