from ddqn import Agent
import numpy as np
from cloud_environment import Environment
import tensorflow as tf

# Layer 1 DQN
def round_robin(options):
    return options

if __name__ == '__main__':

    # Learning rate
    lr = 0.001
    eps = 500

    # layer = 1
    # env = Environment(300, 150, 2000, 3000, layer)
    # # Initialize agent
    # agent = Agent(alpha = lr, gamma = 0.99, n_actions = len(env.actionSpace), epsilon = 1.0, 
    # batch_size = 64, input_dims = env.setState().shape, epsilon_decay_rate = 0.95, epsilon_end = 0.01, 
    # mem_size = 1000000, fname = 'dqn_model.h5', replace_target = 300, Y = 20)

    # print(len(env.actionSpace))

    # # Read the input
    # clusters = []
    # for i in range(eps):
    #     clusters = []
    #     env.reset(layer)

    #     # fileName = ../C++/tasks-(1, 6, 9).txt
    #     f = open("../C++/tasks-1.txt", "r", encoding = 'utf-8-sig')
    #     line = f.readline().strip("\n").split(" ")
    #     while line:
    #         # Data handling
    #         jobID = int(line[0])
    #         dcpu = float(line[1])
    #         dmem = float(line[2].strip())

    #         request = [dcpu, dmem]
    #         observation = env.currentState()

    #         action = agent.choose_action(observation)
    #         # put all tasks within one job into the same cluster
    #         env.prepareActionSpace(jobID, action)
    #         # environment function
    #         observation_, reward, reject, options = env.step(action, request) 
            
    #         # Keep running until no rejection      
    #         while reject == 1 and options > 1:
    #             action_ = round_robin(options) 
    #             if action != action_ :
    #                 action = action_
    #                 observation_, reward, reject, options = env.step(action,request)
                
    #         agent.store_transition(observation, action, reward, observation_)
    #         observation = observation_  
    #         request.append(action)
    #         clusters.append(request) 
    #         agent.learn()

    #         with open('clusters.txt', 'w') as fi: 
    #             for cluster in clusters:
    #                 fi.write("{} {} {}\n".format(cluster[0], cluster[1], cluster[2]))

    #         line = f.readline().strip("\n").split(" ")
    #     f.close()


    
    layer = 2
    env = Environment(300, 150, 2000, 3000, layer)
    agent = Agent(alpha = lr, gamma = 0.99, n_actions = len(env.actionSpace), epsilon = 1.0, 
    batch_size = 64, input_dims = env.setState().shape, epsilon_decay_rate = 0.95, epsilon_end = 0.01, 
    mem_size = 1000000, fname = 'dqn_model.h5', replace_target = 300, Y = 20)

    print(len(env.actionSpace))

    servers = []
    for i in range(eps):
        servers = []
        env.reset(layer)
        f = open("clusters.txt", "r")
        line = f.readline().strip("\n").split(" ")

        while line:
            # how to fix the current parsing error ???
            if len(line) != 3:
                line = f.readline().strip("\n").split(" ")
                continue
            # Data handling
            dcpu = float(line[0])
            dmem = float(line[1])
            clusterIndex = int(line[2])
            # --- Ranges (CPU based) ---
            # First experiment:
            # lg: 0.033 - 0.4062
            # md: 0.016 - 0.033
            # sm: 0.0006247 - 0.016
            if dcpu >= 0.033:
                dVM = 'lg'
            elif 0.033 > dcpu > 0.016:
                dVM = 'md'
            else:
                dVM = 'sm'

            request = [dcpu, dmem, clusterIndex, dVM]

            # [total_available_cpu, total_available_mem] for the selected cluster
            observation = env.currentState(clusterIndex) 
            action = agent.choose_action(observation) 

            # new [total_available_cpu, total_available_mem] for the selected cluster 
            observation_, reward, reject, options = env.step(action, request) 
            
            # while (keep running until no rejection)      
            while reject == 1 and options > 1:
                action_ = round_robin(options)
                if action != action_:
                    action = action_
                    observation_, reward, reject, options = env.step(action,request)
                    
            # def store_transition(self, state, action, reward, new_state):    
            agent.store_transition(observation, action, reward, observation_)
            observation = observation_  
            request.append(action)
            servers.append(request)
            agent.learn()

            with open('servers.txt', 'w') as fi: 
                for server in servers:
                    fi.write("{} {} {} {} {}\n".format(server[0], server[1], server[2], server[3], server[4]))

            line = f.readline().strip("\n").split(" ")

        f.close()