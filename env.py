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
    
class Server(object):
  def __init__(self, cpu, memory, vm_type):
    self.cpu = cpu
    self.memory = memory
    self.vm_type = vm_type
    self.numOfVM = min(self.cpu // virtual_machine_repository[vm_type][0], 
                       self.memory // virtual_machine_repository[vm_type][1])
    self.vm_list = []
    for i in range(numOfVM):
      self.vm_list.append(VirtualMachine(vm_type))
  
  def CPU_Utilization_Rate(self):
    utilize_cpu = 0
    for vm in self.vm_list:
      utilize_cpu += vm.required_cpu
    utilization_rate = utilize_cpu / self.cpu
    return utilization_rate * an if utilization_rate < optimal_utilization \
      else utilization_rate * an + ((utilization_rate - optimal_utilization) ** 2) * bn

class Cluster(object):
  def __init__(self):
    self.cpu = 0
    self.memory = 0
    self.servers = []
    for i in range(serversOfCluster):
      # randomly choose the vm_type for current server
      vm_type = np.random.choice(virtual_machine_repository.keys())
      self.servers.append(Server(server_cpu, server_memory, vm_type))


class Environment(object):
  def __init__(self):
    self.clusters = []
    for i in range(numOfClusters):
      self.clusters.append(Cluster())
    
  def reset(self, layer):
    self.layer = layer
    self.__init__()

  def Reward(layer, action):
    if layer == 1:
      if 0 <= total_utilization_rate < 0.45:
        return 1
      elif total_utilization_rate > 0.5:
        return -2
      else:
        return -1

  # new_observation, reward, reject, option = env.step(action)
  def step(self, action):
    reward = Reward(self.layer, action)


    

