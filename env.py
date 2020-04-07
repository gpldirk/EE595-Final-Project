
#           small  medium  large
# vCPU        1      2       4
# memory(GB)  1      4       8
# tasks under the same job should be on the same sevrer ?

class VirtualMachine(object):
  def __init__(self, vm_Type, required_Cpu = 0, required_Memory = 0):
    self.vm_Type = vm_Type
    self.required_Cpu = required_Cpu
    self.required_Memory = required_Memory


class Task(object):
  def __init__(self, request_Cpu, request_Memory, int timestamp): # ???
    self.jobId = jobId
    self.taskId = taskId
    self.request_Cpu = request_Cpu
    self.request_Memory = request_Memory
    self.request_vm = request_vm
    self.priority = priority
    self.ddl = ddl 
    
class Server(object):
  def __init__(self, Cpu, Memory, numOfVM, vm):
    self.Cpu = Cpu
    self.Memory = Memory
    self.numOfVM = numOfVM
    self.vm_Type = vm.vm_Type
    self.vm_list = list() # 
    for i in range(numOfVM):
      self.vm_list.append(VirtualMachine(vm.vm_Type))
  
  # a, b and optimal_utilization
  def UtilizationOfCPU(self):
    utilize_cpu = 0
    for vm in self.vm_list:
      utilize_cpu += vm.required_Cpu
    utilization_rate = utilize_cpu / self.Cpu
    return a * utilization_rate if utilization_rate < optimal_utilization 
      else a * utilization_rate + ((utilization_rate - optimal_utilization) ** 2) * b

class Cluster(object):
  def __init__(self):
    self.servers = []
    self.Cpu = 0
    self.Memory = 0
    for i in range(n):

      self.servers.append(Server())



cluster c1 = Cluster()
class Environment(object):
  def __init__(self):
 
  
  def reset(self, layer):
    self.__init__(layer)

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
    

