import Env
import ddqn_keras
import numpy as np

# from utils import plotLearning
if __name__ == '__main__':
  env = Env.Environment()
  f = open("tasks-1.txt")
  
  
  states = []
  for line in f.readlines():
    request_Cpu, request_Memory = line.strip().split(" ")
    states.append((request_Cpu, request_Memory))

  for state in states:
    dqn = DQN(1)
    clusters, rejectc = dqn.DQN(state)

    dqn = DQN(2)
    for cluster in clusters:
      servers, rejects = dqn.DQN(state, cluster)
    
    dqn = DQN(3)
    for server in servers:
      hours, rejectt = dqn.DQN(state, cluster, server)
    
    dqn = DQN(4)
    for hour in hours:
        minutes, rejectm = dqn.DQN(state, cluster, server, hour)

  # Calculate final user request allocation matrix, i.e., Ur for every server in every
  # minute according to Ac, As, At, Am, Rejectc, Rejects, Rejectt and Rejectm

  # Calculate final energy consumption Energy, electric bill Cost, energy
  # efficiency and cost efficiency