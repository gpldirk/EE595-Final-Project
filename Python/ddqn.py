import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model

class ReplayBuffer():
    def __init__(self, max_size, input_dims):
        self.mem_size = max_size
        self.mem_cntr = 0

        self.state_memory = np.zeros((self.mem_size, *input_dims), 
                                    dtype = np.float32)
        self.new_state_memory = np.zeros((self.mem_size, *input_dims),
                                dtype = np.float32)
        self.action_memory = np.zeros(self.mem_size, dtype = np.int32)
        self.reward_memory = np.zeros(self.mem_size, dtype = np.float32)

    def store_transition(self, state, action, reward, state_):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = state_
        self.reward_memory[index] = reward
        self.action_memory[index] = action
        self.mem_cntr += 1

    def sample_buffer(self, batch_size):
        max_mem = min(self.mem_cntr, self.mem_size)
        batch = np.random.choice(max_mem, batch_size, replace = False)

        states = self.state_memory[batch]
        states_ = self.new_state_memory[batch]
        rewards = self.reward_memory[batch]
        actions = self.action_memory[batch]

        return states, actions, rewards, states_

def build_dqn(alpha, n_actions, input_dims, fc1_dims):
    
    # When adding a layer we are initializing weights 
    model = keras.Sequential([
        keras.layers.Dense(fc1_dims, activation = 'relu')
        ])
    model.compile(optimizer = Adam(learning_rate = alpha), loss = 'mean_squared_error')
   
    return model

class Agent():
    def __init__(self, alpha, gamma, n_actions, epsilon, batch_size,
                input_dims, epsilon_decay_rate = 0.95, epsilon_end=0.01,
                mem_size=1000000, fname='dqn_model.h5', replace_target = 300, Y = 20):
        # mem_size ?
        self.alpha = alpha
        self.gamma = gamma
        self.action_space = [i for i in range(n_actions)]
        self.epsilon = epsilon
        self.batch_size = batch_size
        self.n_actions = n_actions
        
        # Portion of the time that takes random actions
        self.epsilon_decay_rate = epsilon_decay_rate 
        self.eps_min = epsilon_end
        self.model_file = fname

        # The input_dims is the action space
        self.memory = ReplayBuffer(mem_size, input_dims)
        self.q_eval = build_dqn(alpha, n_actions, input_dims, n_actions)

        # Initialize action-value function Q with random weights
        self.q_target = build_dqn(alpha, n_actions, input_dims, n_actions)
        self.replace_target = replace_target
        self.Y = Y

    def store_transition(self, state, action, reward, new_state):
        self.memory.store_transition(state, action, reward, new_state)

    def choose_action(self, observation):
        if np.random.random_sample() < self.epsilon:
            action = np.random.choice(self.action_space)
        else:
            state = np.array([observation])
            actions = self.q_eval.predict(state)
            action = np.argmax(actions)
        return action

    def learn(self):
        if self.memory.mem_cntr < self.batch_size:
            return

        states, actions, rewards, states_ = \
                self.memory.sample_buffer(self.batch_size)
       
        q_eval = self.q_eval.predict(states_) 
        q_next = self.q_target.predict(states_)

        q_pred = self.q_eval.predict(states)
        max_action = np.argmax(q_eval, axis = 1)

        q_target = q_pred
        batch_index = np.arange(self.batch_size, dtype = np.int32)

        q_target[batch_index, actions] = rewards + self.gamma * q_next[batch_index, max_action.astype(int)]

        # Perform a gradient descent step
        self.q_eval.train_on_batch(states, q_target)

        # Every Y steps, train evaluation network, decrease epsilon
        if self.memory.mem_cntr % self.Y == 0:
            self.epsilon = self.epsilon * self.epsilon_decay_rate if self.epsilon > self.eps_min else self.eps_min

        # Every ζ steps, copy Q to Q'
        if self.memory.mem_cntr % self.replace_target == 0:
            self.update_network_parameters()


    def update_network_parameters(self):
        self.q_target.set_weights(self.q_eval.get_weights())

    def save_model(self):
        self.q_eval.save(self.model_file)

    def load_model(self):
        self.q_eval = load_model(self.model_file)
        if self.epsilon <= self.eps_min:
            self.update_network_parameters()