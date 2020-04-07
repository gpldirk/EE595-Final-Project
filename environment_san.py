class Environment(object):
	# Specify how many clusters, servers per cluster, VMs per server, CPU and Mem for each server
	def __init__(self, num_clus, serv_per_clus, cpu_per_serv, mem_per_serv):
		# Parameters
		self.num_clus = num_clus	
		self.serv_per_clus = serv_per_clus
		self.cpu_per_serv = cpu_per_serv # Virtual cores (2* phys = virt)
		self.mem_per_serv = mem_per_serv # Memory should always be cores * 2
		
		# Additional variables calculated with parameters
		self.serv_total = num_clus*serv_per_clus
		
		# VMs, sm = 1 vcore, 2 GB; md = 2 vcore, 4GB; lg = 4 vcore, 8GB
		self.sm = round(self.cpu_per_serv*.5) # 50% of the server are small VMs
		self.md = round(self.cpu_per_serv*.3) # 30% of the server are medium VMs
		self.lg = self.cpu_per_serv - (self.sm+self.md) # 20% of the server are large VMs

		# Dictionary initializing the VMs within the server
		self.vm_ind = {
			'sm': sm,
			'md': md,
			'lg': lg
		}

		# The vm dictionary is nested within the server dictionary
		self.servers = {}
		self.servlist = []
		for i in range(0,self.serv_total):
			self.servers.update({i: self.vm_ind}) 
			self.servlist.append(i)

		# The clusters are saved within a list. 
		# Example, if I want to access the third server in the second cluster: servers[clusters[1][2]]
		self.clusters = []
		for i in range(0,self.num_clus):
			self.begin = i*self.serv_per_clus
			self.end = self.begin+self.serv_per_clus
			self.clusters.append(self.servlist[self.begin:self.end])
		
		# State Space
		"""
		self.stateSpace = # All states except for the terminal one
		self.stateSpace.remove() # Need to remove the terminal state
		self.stateSpacePlus = # All the states
		"""
		
		# Action Space
		# self.actionSpace = # Is this the clusters list?
		self.possibleActions = [i for i range (0, self.num_clus)] # The possible actions for Layer 1 is the list of available clusters

		# Agent position
		#self.agentPosition = 
	
	def isTerminalState(self, state):
		return state in self.stateSpacePlus and not in self.stateSpace
		
	#def currentState(self):
		
	#def setState(self, state):
		
	def notValidMove(self, newState, oldState):
		if newState not in self.stateSpacePlus:
			return True
			
		else:
			return False
			
	#def step(self, action):
		
	#def reset(self):		
