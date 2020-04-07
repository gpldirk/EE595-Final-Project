import env
import numpy as np
from ddqn_keras import DDQN
# from utils import plotLearning
if __name__ == '__main__':
  env = env.make_environment()
  f = open("tasks-1.txt")
  # the meaning of the 3 variables ?
  # the task.txt ?

  for line in f.readlines():
    line.strip().split(" ")

  task = (request_Memory, request_vm, priority, ddl)

  # initialize DQN == build_dqn
  cluster_control = DDQN(alpha = 0.0005, gamma = 0.99, n_actions = 4, epsilon = 1.0, batch_size = 64, input_dims = 8, layer = 1)

  clusters, rejectc = cluster_control.choose_action(task)

  server_control = DDQN(alpha = 0.0005, gamma = 0.99, n_actions = 4, epsilon = 1.0, batch_size = 64, input_dims = 8, layer = 2)
  for cluster in clusters:
    servers, rejects = server_control.choose_action(cluster)
  
  hour_control = DDQN(alpha = 0.0005, gamma = 0.99, n_actions = 4, epsilon = 1.0, batch_size = 64, input_dims = 8, layer = 3)
  for server in servers:
    hours, rejectt = hour_control.choose_action(cluster, server)
  
  minute_control = DDQN(alpha = 0.0005, gamma = 0.99, n_actions = 4, epsilon = 1.0, batch_size = 64, input_dims = 8, layer = 4)
  for hour in hours:
      minutes, rejectm = minute_control.choose_action(cluster, server, hour)

  # Calculate final user request allocation matrix, i.e., Ur for every server in every
  # minute according to Ac, As, At, Am, Rejectc, Rejects, Rejectt and Rejectm

  # Calculate final energy consumption Energy, electric bill Cost, energy
  # efficiency and cost efficiency