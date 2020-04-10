import numpy as np
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
		self.vm_ind = {'sm': self.sm, 'md': self.md, 'lg': self.lg }

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
		self.stateSpace =  []# All states except for the terminal one
		#self.stateSpace.remove() # Need to remove the terminal state
		#self.stateSpacePlus = # All the states
		#(DCPU,DMEM)X(Numero de clusters)
		#(tarea1, asignacion1,tarea2, asignacion2,) 
		# ss1 = x1 => (Dcpu, Dmem)
		#updateStateSpace(x1)
		# self.stateSpace.append(x1)
		
		# Action Space
		#self.actionSpace = # Clusters
		self.actionSpace = [i for i in range(0, self.num_clus)] # The possible actions for Layer 1 is the list of available clusters

		# Agent position
		#self.agentPosition = 

		#Current Job
		self.currentJob = {}

		#Resources requested
		self.reqcpu_per_cluster = np.zeros(num_clus)
		self.reqmem_per_cluster = np.zeros(num_clus)

		#Reject flag
		self.reject = 0	

		#Options
		self.options = 0
	
	#def isTerminalState(self, state):
		#return state in self.stateSpacePlus and not in self.stateSpace
		
	def currentState(self):
		observation  = 	np.array([self.num_clus*self.cpu_per_serv*self.serv_per_clus, \
						self.num_clus*self.mem_per_serv*self.serv_per_clus])
		return observation

	def setState(self):
	#observation +1 
	#Restale el recurso que asignaste
		observation_ = np.array([self.num_clus*self.cpu_per_serv*self.serv_per_clus - sum(self.reqcpu_per_cluster), \
						    self.num_clus*self.mem_per_serv*self.serv_per_clus - sum(self.reqmem_per_cluster)])
		return observation_

	'''	
	def notValidMove(self, newState, oldState):
		if newState not in self.stateSpacePlus:
			return True
			
		else:
			return False
	'''

	def prepareActionSpace(self, jobNumber, action):
		#Check if already exists if not add a new 
		newAS = self.currentJob.get(str(jobNumber),"")
		if newAS == '' :
			self.currentJob[str(jobNumber)] = action
			self.actionSpace = action
		else:
			self.actionSpace = newAS 
			
	
	def get_ur(self, action):
		if self.layer == 1 :
			ut=(self.reqcpu_per_cluster[action]/ (self.cpu_per_serv*self.serv_per_clus))*100
		if ut > 0 and ut < 45:
			return 1
		elif ut > 50 : 
			return -2
		else:
			return -1

	def isLegal(self,action, request):
		flag=True
                #Restriction 1: Limits in CPU
		if (self.reqcpu_per_cluster[action] + request[0]) >= (self.cpu_per_serv*self.serv_per_clus):
			flag= False
		#Restriction 2: Limits in Memory
		if (self.reqmem_per_cluster[action] + request[1]) >= (self.mem_per_serv*self.serv_per_clus):
			flag= False

		if (self.layer == 1):
			#Restriction 3: Same job in same cluster
			if self.actionSpace != action:
				flag= False
		return flag
		
	def step(self, action, request):
		reward = self.get_ur(action)
		if self.isLegal(action,request):	
			self.reqcpu_per_cluster[action] = self.reqcpu_per_cluster[action] + request[0]
			self.reqmem_per_cluster[action] = self.reqmem_per_cluster[action] + request[1]
			self.stateSpace.append(request)
			self.stateSpace.append(action)
			self.reject = 0
			observation_ = self.setState()
		else:
			self.reject = 1
			self.options = self.actionSpace
			observation_ = self.currentState()

		return observation_, reward, self.reject, self.options

	'''			
	#def step(self, action):
	#Layer 1: All the tasks in the same job are located in the same cluster
	#Input: cluster 
	#Output: observation_ (resources available after the t+1, todo --cuantos clusters, cuantas maquinas, cuantas vm), reward (from utilization function), done(no more tasks), reject (flag), info = env.step(action)
	#Escribir esto en function del setState(), currentState()
	#Revisar si estoy en el mismo trabajo, si no actualizo variables: current_job, current_cluster
	#Calcular la utilizacion (antes de la accion, de aqui obtengo la recompensa)
	#Es legal o no? Si segun el job al que perteces le tocaba ese cluster
	#Si la opcion es legal , actualiza el estado, regresar observation_ y la recompensa
	#Si no es legal mando reject, no actualizo estado y reward 0, reject=1, opciones 
								#las opciones van a ser el cluster del current job		
	'''
	
	def reset(self, layer):	
		self.layer=layer

		#Inicializar los estados ()	
