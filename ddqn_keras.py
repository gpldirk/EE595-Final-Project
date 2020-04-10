from keras.layers import Dense, Activation
from keras.models import Sequential, load_model
from keras.optimizers import Adam
import numpy as np
import sys
import Env

class ReplayBuffer(object):
  def __init__(self, max_size, input_shape, n_actions, discrete = False):
    self.mem_size = max_size
    self.mem_cntr = 0
    self.discrete = discrete
    self.state_memory = np.zeros((max_size, input_shape))
    self.new_state_memory = np.zeros((max_size, input_shape))
    dtype = np.int8 if discrete else np.float32
    self.action_memory = np.zeros((max_size, n_actions), dtype = dtype)
    self.reward_memory = np.zeros(max_size)
  
  def store_transition(self, state, action, reward, new_state):
    index = self.mem_cntr % self.mem_size
    self.state_memory[index] = state
    self.new_state_memory[index] = new_state
    self.reward_memory[index] = reward

    if self.discrete:
      actions = np.zeros(self.action_memory.shape[1])
      actions[action] = 1.0
      self.action_memory[index] = actions
    else:
      self.action_memory[index] = action
    self.mem_cntr += 1

  def sample_buffer(self, batch_size):
    max_mem = min(self.mem_cntr, self.mem_size)
    batch = np.random.choice(max_mem, batch_size)
    states = self.state_memory[batch]
    new_states = self.new_state_memory[batch]
    actions = self.action_memory[batch]
    rewards = self.reward_memory[batch]
    return states, actions, rewards, new_states

def build_dqn(lr, n_actions, input_dims, fc1_dims, fc2_dims):
  model = Sequential([
      Dense(fc1_dims, input_shape = (input_dims,)),
      Activation('relu'),
      Dense(fc2_dims),
      Activation('relu'),
      Dense(n_actions)
  ])

  model.compile(optimizer = Adam(lr = lr), loss = 'mse')
  return model

class DDQNAgent(object):
  def __init__(self, alpha, gamma, n_actions, epsilon, batch_size, input_dims, epsilon_decay_rate = 0.95, epsilon_end = 0.01, mem_size = 500, fname = 'ddqn_model.h5', replace_target = 300, Y = 20):
    self.n_actions = n_actions
    self.action_space = [i for i in range(self.n_actions)]
    self.alpha = alpha
    self.gamma = gamma
    self.epsilon = epsilon
    self.epsilon_decay_rate = epsilon_decay_rate
    self.epsilon_min = epsilon_end
    self.batch_size = batch_size
    self.model_file = fname
    self.replace_target = replace_target
    self.memory = ReplayBuffer(mem_size, input_dims, n_actions, True)
    self.q_eval = build_dqn(alpha, n_actions, input_dims, 256, 256)
    self.q_target = build_dqn(alpha, n_actions, input_dims, 256, 256)
        
    
  def remember(self, state, action, reward, new_state):
    self.memory.store_transition(state, action, reward, new_state)
  
  def choose_action(self, state):
    rand = np.random()
    if rand < self.epsilon:
        action = np.random.choice(self.action_space) # randomly select a cluster as action
    else:
        actions = self.q_eval.predict(state)
        action = np.argmax(actions)
    return action
  
  def learn(self):
    if self.memory.mem_cntr > self.batch_size:
      state, action, reward, new_state = self.memory.sample_buffer(self.batch_size)
      action_values = np.array(self.action_space, dtype = np.int8)
      action_index = np.dot(action, action_values)
      
      q_eval = self.q_eval.predict(new_state)
      q_next = self.q_target.predict(new_state)
      q_pred = self.q_eval.predict(state)
      max_action = np.argmax(q_eval, axis = 1)
      
      q_target = q_pred
      batch_index = np.arange(self.batch_size, dtype = np.int32)
      q_target[batch_index, action_index] = reward + self.gamma * q_next[batch_index, max_action.astype(int)]

      # Perform a gradient descent step
      _ = self.q_eval.fit(state, q_target, verbose = 0) # train or gredient descent 

      # Every Y steps, train evaluation network, decrease epsilon
      if self.memory.mem_cntr % Y == 0:
        self.epsilon = self.epsilon * self.epsilon_decay_rate if self.epsilon > self.epsilon_min else self.epsilon_min

      # Every ζ steps, copy Q to Q'
      if self.memory.mem_cntr % self.replace_target == 0:
          self.update_network_parameters()
        
  def update_network_parameters(self):
    self.q_target.model.set_weights(self.q_eval.model.get_weights())
  
  def save_model(self):
    self.q_eval.save(self.model_file)
  
  
  def load_model(self):
    self.q_eval = load_model(self.model_file)
    if self.epsilon <= self.epsilon_min:
      self.update_network_parameters()

  
