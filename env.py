import numpy as np

#           small  medium  large
# vCPU        1      2       4
# memory(GB)  1      4       8
# Timestamp, cpu requested, memory requested
# type: [cpu, memory]
virtual_machine_repository = {
  'small': [1, 1],
  'medium': [2, 4],
  'large': [4, 8]
}

an = 1
bn = 1
optimal_utilization = 1
server_cpu = 4
server_memory = 8
serversOfCluster = 1000
numOfClusters = 10

class Task(object):
  def __init__(self, timestamp, requested_cpu, requested_memory):
    self.timestamp = timestamp
    self.requested_cpu = requested_cpu
    self.requested_memory = requested_memory

class VirtualMachine(object):
  def __init__(self, vm_type, required_cpu = 0, required_memory = 0):
    self.vm_type = vm_type
    self.cpu = virtual_machine_repository[vm_type][0]
    self.memory = virtual_machine_repository[vm_type][1]
    self.required_cpu = required_cpu
    self.required_memory = required_memory
  
  # check constraints (9, 10)
  def violated(self, task):
    if task.requested_cpu + self.required_cpu > self.cpu or \
        task.requested_memory + self.required_memory > self.memory:
      return True
    else:
      return False

class Server(object):
  def __init__(self, cpu, memory, vm_type):
    self.cpu = cpu
    self.memory = memory
    self.vm_type = vm_type
    self.numOfVM = min(self.cpu // virtual_machine_repository[vm_type][0], 
                       self.memory // virtual_machine_repository[vm_type][1])
    self.vm_list = []
    for i in range(self.numOfVM):
      self.vm_list.append(VirtualMachine(vm_type))
  
  # check constraints (11, 12)
  def violated(self, task):
    total_required_cpu = 0
    total_required_memory = 0
    for i in range(self.numOfVM):
      total_required_cpu += self.vm_list[i].required_cpu
      total_required_memory += self.vm_list[i].requested_memory

    if total_required_cpu + task.requested_cpu > self.cpu or \
        total_required_memory + task.requested_memory > self.memory:
      return True
    return False

  def CPU_Utilization_Rate(self):
    utilize_cpu = 0
    for vm in self.vm_list:
      utilize_cpu += vm.required_cpu
    utilization_rate = utilize_cpu / self.cpu
    return utilization_rate * an if utilization_rate < optimal_utilization \
      else utilization_rate * an + ((utilization_rate - optimal_utilization) ** 2) * bn

class Cluster(object):
  def __init__(self):
    self.cpu = serversOfCluster * server_cpu
    self.memory = serversOfCluster * server_memory
    self.left_cpu = self.cpu
    self.left_memory = self.memory
    self.servers = []
    for _ in range(serversOfCluster):
      # randomly choose the vm_type for current server or small:medium:large = 5:3:2
      vm_type = np.random.choice(virtual_machine_repository.keys())
      self.servers.append(Server(server_cpu, server_memory, vm_type))

# action space: available clusters, servers, hours and minutes
# the observation of task is a tuple {CPU, MEM}

class Environment(object):
  def __init__(self):
    self.clusters = []
    for _ in range(numOfClusters):
      self.clusters.append(Cluster())

  def reset(self, layer):
    self.__init__()
    self.layer = layer

  def choose_clusters(self, task):
    new_state = []
    reject = 1
    option = 0
    for index, cluster in enumerate(self.clusters):
      # ???
    return new_state, reject, option

  def choose_clusters(self, task, clusters):
    new_state = []
    reject = 1
    option = 0
    for index, cluster in enumerate(self.clusters):
      # ???
    return new_state, reject, option
  
  def choose_clusters(self, task, clusters, servers):
    new_state = []
    reject = 1
    option = 0
    for index, cluster in enumerate(self.clusters):
      # ???
    return new_state, reject, option
  
  def choose_clusters(self, task, clusters, servers, hours):
    new_state = []
    reject = 1
    option = 0
    for index, cluster in enumerate(self.clusters):
      # ???
    return new_state, reject, option

  # new_observation, reward, reject, option = env.step(action)
  def step(self, *action):
    if len(action) == 1:
      new_state, reject, option = self.choose_clusters(action)
    elif len(action) == 2:
      new_state, reject, option = self.choose_servers(action)
    elif len(action) == 3:
      new_state, reject, option = self.choose_hours(action)
    elif len(action) == 4:
      new_state, reject, option = self.choose_minutes(action)

    reward = get_reward(self.layer)
    return new_state, reward, reject, option

  
  def get_utilization_rate(self): #???
    return 0


  def get_reward(self, layer, action): # (take current task on cluster i, server j and vm k)
    if layer == 1:
      if 0 <= self.get_utilization_rate() < 0.45:
        return 1
      elif self.get_utilization_rate() > 0.5:
        return -2
      else:
        return -1


    

