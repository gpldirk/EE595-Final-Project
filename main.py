import Env
import numpy as np
from ddqn_keras import DDQNAgent

class DQN(object):
  def __init__(self, episodes, T, layer):
    self.episodes = episodes
    self.T = T
    self.layer = layer

    self.decisions = []
    self.rejects = []
    self.env = Env.Environment()
    self.ddqn_agent = DDQNAgent(alpha = 0.1, gamma = 0.9, n_actions = 4, epsilon = 0.9, batch_size = 64, input_dims = 8)
  
  # allocate the task into the cluster (clusterIndex)
  def process(self, tasks):
    for _ in range(self.episodes): # E
      state = env.reset(self.layer)
      for task in range(tasks): # T is the number of tasks
        action = ddqn_agent.choose_action(task, state)
        new_state, reward, reject, option = env.step(action)
        while reject == 1 and option > 1:
          for new_action in option:
            if new_action != action:
              action = new_action
              new_state, reward, reject, option = env.step(action)

        ddqn_agent.remember(state, action, reward, new_state)
        decisions.append(action)
        rejects.append(reject)
        ddqn_agent.learn()
    return decisions, rejects



if __name__ == '__main__':
  env = Env.Environment()
  tasks = []
  with open("tasks-1.txt") as f:
    for line in f.readlines():
      temestamp, requested_cpu, request_memory = line.strip().split(" ")
      tasks.append(int(temestamp), float(requested_cpu), float(request_memory))
  
  dpn = DQN(10000, len(tasks), 1)
  dqn.process(tasks)


  # for state in states:
  #   dqn = DQN(1)
  #   clusters, rejectc = dqn.DQN(state)

  #   dqn = DQN(2)
  #   for cluster in clusters:
  #     servers, rejects = dqn.DQN(state, cluster)
    
  #   dqn = DQN(3)
  #   for server in servers:
  #     hours, rejectt = dqn.DQN(state, cluster, server)
    
  #   dqn = DQN(4)
  #   for hour in hours:
  #       minutes, rejectm = dqn.DQN(state, cluster, server, hour)
