from dqn import Agent
import numpy as np
from env_san_sha import Environment
#from utils import plotLearning
import tensorflow as tf

#Layer 1 DQN

if __name__ == '__main__':

    
    #Learning rate
    lr = 0.001
    eps = 500

    env = Environment(20,40,2000,3000)

    #Agent initialization
    #input_dims=env.observation_space.shape. Sera la s?, Sera x2?
    agent = Agent(gamma=0.99, epsilon=1.0, lr=lr, 
                input_dims=env.currentState().shape,
                n_actions=len(env.actionSpace), mem_size=1000000, batch_size=64,
                epsilon_end=0.01)

    #Read the input
    f=open("tasks-1-2.txt", "r")
    layer=1
    clusters = []
    eps_history = []
    
    for i in range(eps):
        done = False
        cl = 0
        env.reset(layer) #environment reset
        line=f.readline().split(",")

        while line:
            #Data handling
            jobID = int(line[0])
            dcpu = float(line[1])
            dmem = float(line[2].strip())

            request = [dcpu, dmem]
            observation = env.currentState()

            print(request)
            print(observation)

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
            clusters.apped(action)
            #store decision and reject signal
            agent.learn()
        eps_history.append(agent.epsilon)

    f.close()
       
    def round_robin(options):
        return options[0]
