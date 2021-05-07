import numpy as np

class Environment(object):
	# Specify how many clusters, servers per cluster, CPU and Mem for each server
	def __init__(self, num_clus, serv_per_clus, cpu_per_serv, mem_per_serv, layer):
		# Parameters
		self.num_clus = num_clus	
		self.serv_per_clus = serv_per_clus
		self.cpu_per_serv = cpu_per_serv # Virtual cores (2* phys = virt)
		self.mem_per_serv = mem_per_serv # Memory should always be cores * 2
		self.layer = layer
		
		# VMs, 3 different CPU sizes (small, medium, large) on one server
		self.sm = round(self.cpu_per_serv * .5) # 50% CPU of the server are small VMs
		self.md = round(self.cpu_per_serv * .3) # 30% CPU of the server are medium VMs
		self.lg = self.cpu_per_serv - (self.sm + self.md) # 20% CPU of the server are large VMs
		
		# State Space
		self.stateSpace =  []

		# Action Space
		if self.layer == 1:
			# The possible actions for Layer 1 is the list of available clusters index
			self.actionSpace = [i for i in range(self.num_clus)] 
			# The possible actions for Layer 2 is the list of available servers index within one cluster
		elif self.layer == 2:
			self.actionSpace = [i for i in range(self.serv_per_clus)]

		# Current Job
		self.currentJob = {}

		self.reqcpu_per_cluster = np.zeros(num_clus)
		self.reqmem_per_cluster = np.zeros(num_clus)
		self.reqcpu_per_server = np.zeros(num_clus * serv_per_clus)
		self.reqmem_per_server = np.zeros(num_clus * serv_per_clus)

		# Resources requested
		# --- Ranges (CPU based) ---
		# First experiment:
		# lg: 0.033 - 0.4062
		# md: 0.016 - 0.033
		# sm: 0.0006247 - 0.016
		self.reqcpu_lg_per_server = np.zeros(num_clus * serv_per_clus)
		self.reqcpu_md_per_server = np.zeros(num_clus * serv_per_clus)
		self.reqcpu_sm_per_server = np.zeros(num_clus * serv_per_clus)
	
	# initialize the state for environment
	def setState(self):
		# for layer 1, it is [total_CPU, total_memory] for all clusters
		if self.layer == 1:
			observation = np.array([self.num_clus * self.serv_per_clus * self.cpu_per_serv, \
							self.num_clus * self.serv_per_clus * self.mem_per_serv])
			return observation
		# for layer 2, it is [total_CPU, total_memory] for all servers within one cluster
		elif self.layer == 2:
			observation = np.array([self.cpu_per_serv * self.serv_per_clus, \
							self.mem_per_serv * self.serv_per_clus])
			return observation
	
	# get current state for environment
	def currentState(self, clusterIndex = 0):
		# for layer 1, it is [total_avaliable_CPU, total_available_memory] for all clusters
		if self.layer == 1:
			observation_ = np.array([self.num_clus * self.serv_per_clus * self.cpu_per_serv - sum(self.reqcpu_per_cluster), \
									self.num_clus * self.serv_per_clus * self.mem_per_serv - sum(self.reqmem_per_cluster)])
			return observation_
		
		# for layer 2, it is [total_available_cpu, total_available_mem] for current cluster
		elif self.layer == 2:
			observation_ = np.array(
				[self.cpu_per_serv * self.serv_per_clus - sum(self.reqcpu_per_server
				[clusterIndex * self.serv_per_clus : (clusterIndex + 1) * self.serv_per_clus]), \
				 self.mem_per_serv * self.serv_per_clus - sum(self.reqmem_per_server
			  [clusterIndex * self.serv_per_clus : (clusterIndex + 1) * self.serv_per_clus])]
				)
			return observation_

	def prepareActionSpace(self, jobNumber, action):
		# check if already exists if not add a new 
		newAS = self.currentJob.get(str(jobNumber),"")
		if newAS == '' :
			self.currentJob[str(jobNumber)] = action
			self.actionSpace = action
		else:
			self.actionSpace = newAS 
			
	
	def get_ur(self, action, clusterIndex = 0):
		if self.layer == 1 :
			# cpu utilization rate for current cluster
			ut = (self.reqcpu_per_cluster[action] / (self.cpu_per_serv * self.serv_per_clus)) * 100
			if ut > 0 and ut < 45:
				return 1
			elif ut > 50 : 
				return -2
			else:
				return -1
		
		elif self.layer == 2:
			# cpu utilization rate for current server ???
			ut = (self.reqcpu_per_server[clusterIndex * self.serv_per_clus + action] / (self.cpu_per_serv))*100
			if ut >= 20 and ut < 80:
				return 1
			elif ut > 100 : 
				return -2
			else:
				return -1

	def isLegal(self, action, request):
		if (self.layer == 1):
			# Restriction 1: Limits in CPU for selected cluster
			if (self.reqcpu_per_cluster[action] + request[0]) >= (self.cpu_per_serv * self.serv_per_clus):
				return False
			# Restriction 2: Limits in Memory for selected cluster
			if (self.reqmem_per_cluster[action] + request[1]) >= (self.mem_per_serv * self.serv_per_clus):
				return False
			# Restriction 3: Same job in same cluster
			if self.actionSpace != action:
				return False

		
		if (self.layer == 2):
			# Restriction 1: Limits in CPU for selected server
			index = request[2] * self.serv_per_clus + action
			if (self.reqcpu_per_server[index] + request[0]) >= (self.cpu_per_serv):
				return False
			# Restriction 2: Limits in Memory for selected server
			if (self.reqmem_per_server[index] + request[1]) >= (self.mem_per_serv):
				return False
			
			# Restriction 3: Limits in CPU for selected VM
			if (request[3] == 'lg'):
				if (self.reqcpu_lg_per_server[index] + request[0] >= self.lg):
					return False
			if (request[3] == 'md'):
				if (self.reqcpu_md_per_server[index] + request[0] >= self.md):
					return False
			if (request[3] == 'sm'):
				if (self.reqcpu_sm_per_server[index] + request[0] >= self.sm):
					return False
		return True
	
	def step(self, action, request):
		if self.isLegal(action, request):	
			# Q1: if the request is legal, then the CPU utilization rate will
			# always < 100% -> no meaning for reward?

			# update the available CPU and memory for selected cluster
			if self.layer == 1:
				self.reqcpu_per_cluster[action] = self.reqcpu_per_cluster[action] + request[0]
				self.reqmem_per_cluster[action] = self.reqmem_per_cluster[action] + request[1]
				self.stateSpace.append(request)
				self.stateSpace.append(action)
				reject = 0
				options = 0
				observation_ = self.currentState()
			# update the available CPU and memory for selected server
			elif self.layer == 2:
				index = request[2] * self.serv_per_clus + action
				self.reqcpu_per_server[index] += request[0]
				self.reqmem_per_server[index] += request[1]
				if (request[3] == 'lg'):
					self.reqcpu_lg_per_server[index] += request[0]
				elif (request[3] == 'md'):
					self.reqcpu_md_per_server[index] += request[0]
				elif (request[3] == 'sm'):
					self.reqcpu_sm_per_server[index] += request[0]
				
				self.stateSpace.append(request)
				self.stateSpace.append(action)
				reject = 0
				options = 0
				observation_ = self.currentState(request[2])

		else:
			reject = 1
			options = self.actionSpace
			observation_ = self.currentState(request[2])

		reward = self.get_ur(action, request[2])
		return observation_, reward, reject, options

	# reset the environment, including important variables
	def reset(self, layer):	
		# Q2: no need to define the stateSpace ??? because we do not use it
		# State Space
		self.stateSpace =  []

		# Action Space
		if self.layer == 1:
			# The possible actions for Layer 1 is the list of available clusters index
			self.actionSpace = [i for i in range(self.num_clus)] 
			# The possible actions for Layer 2 is the list of available servers index within one cluster
		elif self.layer == 2:
			self.actionSpace = [i for i in range(self.serv_per_clus)]

		# Current Job
		self.currentJob = {}

		self.reqcpu_per_cluster = np.zeros(self.num_clus)
		self.reqmem_per_cluster = np.zeros(self.num_clus)
		self.reqcpu_per_server = np.zeros(self.num_clus * self.serv_per_clus)
		self.reqmem_per_server = np.zeros(self.num_clus * self.serv_per_clus)

		# Resources requested
		# --- Ranges (CPU based) ---
		# First experiment:
		# lg: 0.033 - 0.4062
		# md: 0.016 - 0.033
		# sm: 0.0006247 - 0.016
		self.reqcpu_lg_per_server = np.zeros(self.num_clus * self.serv_per_clus)
		self.reqcpu_md_per_server = np.zeros(self.num_clus * self.serv_per_clus)
		self.reqcpu_sm_per_server = np.zeros(self.num_clus * self.serv_per_clus)



