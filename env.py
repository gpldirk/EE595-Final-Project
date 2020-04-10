import numpy as np

#           small  medium  large
# vCPU        1      2       4
# memory(GB)  1      4       8
# task = (Timestamp, cpu requested, memory requested)
# type: [cpu, memory]

virtual_machine_repository = {
  'small': (1, 1),
  'medium': (2, 4),
  'large': (4, 8)
}

server_repository = {
  0: ['large'],
  1: ['medium', 'medium'],
  2: ['medium', 'small', 'small'],
  3: ['small', 'small', 'small', 'small']
}

an = 0.2
bn = 0.5
server_cpu = 4
server_memory = 8
serversOfCluster = 10000
numOfClusters = 10
optimal_utilization_rate = 0.7


class Task(object):
  def __init__(self, timestamp, requested_cpu, requested_memory):
    self.timestamp = timestamp
    self.requested_cpu = requested_cpu
    self.requested_memory = requested_memory

class VirtualMachine(object):
  def __init__(self, vm_type, required_cpu = 0, required_memory = 0):
    self.vm_type = vm_type
    self.required_cpu = required_cpu
    self.required_memory = required_memory
    self.demand_cpu = 0
    self.demand_memory = 0
  
  # check constraints (9, 10)
  def violated(self, task):
    if task.requested_cpu + self.demand_cpu > self.required_cpu or \
        task.demand_memory + self.demand_memory > self.required_memory:
      return True
    else:
      return False
  
  def CPU_Utilization_Rate(self):
    return self.demand_cpu / self.required_cpu

class Server(object):
  def __init__(self, server_cpu, server_memory):
    self.left_cpu = server_cpu
    self.left_memory = server_memory
    self.vm_list = []
    key = np.random.randint(0, 4)
    for vm_type in server_repository[key]:
      self.vm_list.append(VirtualMachine(vm_type, \
        virtual_machine_repository[vm_type][0], virtual_machine_repository[vm_type][1]))
  
  # check constraints (11, 12)
  def violated(self, task):
    if task.requested_cpu > self.left_cpu or task.requested_memory > self.left_memory:
      return True
    else:
      return False

  def CPU_Utilization_Rate(self):
    utilize_cpu = 0
    total_cpu = 0
    for vm in self.vm_list:
      utilize_cpu += vm.demand_cpu
      total_cpu += vm.required_cpu
    utilization_rate = utilize_cpu / total_cpu
    return utilization_rate * an if utilization_rate < optimal_utilization_rate \
      else utilization_rate * an + ((utilization_rate - optimal_utilization_rate) ** 2) * bn

class Cluster(object):
  def __init__(self):
    self.cpu = serversOfCluster * server_cpu
    self.memory = serversOfCluster * server_memory
    self.left_cpu = self.cpu
    self.left_memory = self.memory
    self.servers = []
    for _ in range(serversOfCluster):
      self.servers.append(Server(server_cpu, server_memory))
  
  def violated(self, task):
    if task.requested_cpu > self.left_cpu or \
      task.requested_memory > self.left_memory:
      return True
    else:
      return False

  def CPU_Utilization_Rate(self):
    return (self.cpu - self.left_cpu) / self.cpu
  

# action space: available clusters, servers, hours and minutes
# observation or state: 
# cluster observation: (CPU and memory of that cluster) + task observation (DCPU, DMEM)

class Environment(object):
  def __init__(self):
    self.clusters = []
    for _ in range(numOfClusters):
      self.clusters.append(Cluster())

  def reset(self, layer):
    self.__init__()
    self.layer = layer
    return [[self.clusters[0].left_cpu, self.clusters[0].left_memory] * len(self.clusters)]

  # new_state, reject, option, the new new_observation = [left_cpu, left_memory] in every cluster
  def choose_cluster(self, task, clusterIndex):
    new_state = [] * len(self.clusters)

    option = []
    for i in range(len(self.clusters)):
      new_state[i] = [self.clusters[i].left_cpu, self.clusters[i].left_memory]
      if not self.clusters[i].violated(task):
        option.append[i]

    if self.clusters[clusterIndex].violated(task):
      return new_state, 1, option

    self.clusters[clusterIndex].left_cpu -= task.requested_cpu
    self.clusters[clusterIndex].left_memory += task.requested_memory
    new_state[clusterIndex][0] -= task.requested_cpu
    new_state[clusterIndex][1] -= task.requested_memory
    return self.clusters, 0, option
      

  def get_reward(self, clusterIndex): 
    if 0 <= self.clusters[clusterIndex].CPU_Utilization_Rate() < 0.45:
      return 1
    elif self.clusters[clusterIndex].CPU_Utilization_Rate() > 0.5:
      return -2
    else:
      return -1

  # new_state, reward, reject, option = env.step(action), action = (task, clusterIndex)
  def step(self, *action):
    new_state, reject, option = self.choose_cluster(action[0], action[1])
    reward = self.get_reward(action[1])
    return new_state, reward, reject, option



    

