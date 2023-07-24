from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import TCLink

def create_topology():
    net = Mininet(controller=RemoteController, link=TCLink)

    # Adicionando o controlador Ryu
    c0 = net.addController('c0', controller=RemoteController, ip='172.28.121.175', port=6633)

    # Criando switches
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')

    # Criando hosts
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

    # Criando links entre switches e hosts
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s2, h3)
    net.addLink(s2, h4)
    net.addLink(s3, h5)
    net.addLink(s3, h6)
    net.addLink(s4, h7)
    net.addLink(s4, h8)

    # Criando links entre switches
    net.addLink(s1, s2)
    net.addLink(s1, s3)
    net.addLink(s2, s4)
    net.addLink(s3, s4)

    # Iniciando a rede
    net.start()

    # Configurando o controlador para os switches
    for switch in net.switches:
        switch.start([c0])

    # Adicionando uma rota padrão para cada host
    for host in net.hosts:
        host.cmd('route add default gw 10.0.0.1')

    # Iniciando a interface de linha de comando do Mininet
    CLI(net)

    # Parando a rede
    net.stop()

if __name__ == '__main__':
    create_topology()
