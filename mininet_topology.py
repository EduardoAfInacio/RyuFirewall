from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
import os

def create_topology():
    net = Mininet(controller=Controller, switch=OVSSwitch, link=TCLink)
    net.addController('c0', controller=RemoteController, ip='IP DA MINHA REDE', port=6633)

    # Criação dos switches
    s1 = net.addSwitch('s1', protocols='OpenFlow13')
    s2 = net.addSwitch('s2', protocols='OpenFlow13')
    s3 = net.addSwitch('s3', protocols='OpenFlow13')
    s4 = net.addSwitch('s4', protocols='OpenFlow13')

    # Criação dos hosts
    h1 = net.addHost('h1', ip='10.0.0.1')
    h2 = net.addHost('h2', ip='10.0.0.2')
    h3 = net.addHost('h3', ip='10.0.0.3')
    h4 = net.addHost('h4', ip='10.0.0.4')
    h5 = net.addHost('h5', ip='10.0.0.5')
    h6 = net.addHost('h6', ip='10.0.0.6')
    h7 = net.addHost('h7', ip='10.0.0.7')
    h8 = net.addHost('h8', ip='10.0.0.8')
    h9 = net.addHost('h9', ip='10.0.0.9')
    h10 = net.addHost('h10', ip='10.0.0.10')

    # Criação das conexões
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s2, h3)
    net.addLink(s2, h4)
    net.addLink(s3, h5)
    net.addLink(s3, h6)
    net.addLink(s4, h7)
    net.addLink(s4, h8)
    net.addLink(s1, s2)
    net.addLink(s1, s3)
    net.addLink(s2, s4)
    net.addLink(s3, s4)
    net.addLink(s3, h9)
    net.addLink(s4, h10)
    
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    os.system('mn -c')
    create_topology()