from mininet.topo import Topo

class MyTopo(Topo):
	def __init__(self):
		Topo.__init__(self)

		switches = []
		hosts = []

		# Creacion de switches y hosts
		for i in range(4):
			switches.append(self.addSwitch(f's{i + 1}', dpid = f'00:00:00:00:00:00:00:{i + 1:02x}'))
			hosts.append(self.addHost(f'h{i + 1}', mac = f'10:00:00:00:00:0{i + 1}'))

			#Conexion entre el host y el switch
			self.addLink(self.addLink(hosts[i], switches[i], 1, 1))

		# Conexiones entre los switches
		for i in range(4):
			self.addLink(switches[i], switches[i - 1], 2, 3)
		# Conexion adicional
		self.addLink(switches[0], switches[2], 4, 5)

topos = {'MyTopo': (lambda: MyTopo())}