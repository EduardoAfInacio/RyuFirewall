from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, set_ev_cls
from ryu.lib.packet import packet, ethernet, ipv4, tcp, udp, ether_types
from ryu.ofproto import ofproto_v1_3


class SecurityApp(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SecurityApp, self).__init__(*args, **kwargs)
        self.firewall_rules = [
            {'src_ip': '10.0.0.1', 'dst_ip': '10.0.0.2', 'dst_port': 80},
            # Regras
        ]

    def apply_firewall_rules(self, datapath, pkt_ethernet, pkt_ipv4, pkt_tcp_udp):
        src_ip = pkt_ipv4.src
        dst_ip = pkt_ipv4.dst
        dst_port = None

        if pkt_tcp_udp.protocol == ipv4.inet.IPPROTO_TCP:
            dst_port = pkt_tcp_udp.dst_port
        elif pkt_tcp_udp.protocol == ipv4.inet.IPPROTO_UDP:
            dst_port = pkt_tcp_udp.dst_port

        for rule in self.firewall_rules:
            if (src_ip == rule['src_ip'] and dst_ip == rule['dst_ip'] and
                    (dst_port is None or dst_port == rule['dst_port'])):
                self.logger.info('Firewall: Dropping packet from %s to %s:%s',
                                 src_ip, dst_ip, dst_port)
                match = datapath.ofproto_parser.OFPMatch(
                    eth_type=ether_types.ETH_TYPE_IP,
                    ipv4_src=src_ip,
                    ipv4_dst=dst_ip,
                    ip_proto=pkt_tcp_udp.protocol,
                    tcp_dst=dst_port if pkt_tcp_udp.protocol == ipv4.inet.IPPROTO_TCP else None,
                    udp_dst=dst_port if pkt_tcp_udp.protocol == ipv4.inet.IPPROTO_UDP else None
                )
                self.add_flow(datapath, match, priority=1, actions=[])
                return True

        return False

    def add_flow(self, datapath, match, priority, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, match=match, cookie=0,
                                command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                priority=priority, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        pkt = packet.Packet(msg.data)
        pkt_ethernet = pkt.get_protocol(ethernet.ethernet)
        pkt_ipv4 = pkt.get_protocol(ipv4.ipv4)
        pkt_tcp_udp = pkt.get_protocol(tcp.tcp) or pkt.get_protocol(udp.udp)

        if pkt_ethernet.ethertype == ether_types.ETH_TYPE_IP and pkt_ipv4:
            if self.apply_firewall_rules(datapath, pkt_ethernet, pkt_ipv4, pkt_tcp_udp):
                return

        # Caso não haja match de regras, segue:
        actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=msg.match['in_port'], actions=actions)
        datapath.send_msg(out)


if __name__ == '__main__':
    # Startando a aplicação:
    from ryu.cmd import manager
    manager.main()
