from simple_dqn_tf2 import Agent
import numpy as np
#import gym
#from utils import plotLearning
import tensorflow as tf

#Layer 1 DQN

if __name__ == '__main__':

    
    #Learning rate
    lr = 0.001
    eps = 500

    #Agent initialization
    #input_dims=env.observation_space.shape. Sera la s?, Sera x2?
    agent = Agent(gamma=0.99, epsilon=1.0, lr=lr, 
                input_dims=env.observation_space.shape,
                n_actions=env.action_space.n, mem_size=1000000, batch_size=64,
                epsilon_end=0.01)

    #Read the input
    f=open("tasks-1.txt", "r")

    clusters = []
    eps_history = []

    for i in range(eps):
        done = False
        cl = 0
        env.reset(layer) #environment reset

        #Data handling
        line=f.readline().split(",")
        jobID = int(line[0])
        dcpu = float(line[1])
        dmem = float(line[2].strip())

        request = [dcpu, dmem]
        observation = env.currentState()

        while not done:
            action = agent.choose_action(observation)
            env.prepareActionSpace(jobID, action)
            observation_, reward, reject, options = env.step(action,request) #environment function
            #Do the reject stuff and valid action number option
            #while (keep running until no rejection)  
            
            while reject == 1 and len(option)>1:
                action_ = round_robin(options) 
                if action != action_ :
                    action = action_
                    observation_, reward, reject, options = env.step(action,request)
                
            agent.store_transition(observation, action, reward, observation_, done)
            observation = observation_  
            clusters.apped(cluster)
            #store decision and reject signal
            agent.learn()
        eps_history.append(agent.epsilon)

    f.close()
       
    def round_robin(options):
        return options[0]
