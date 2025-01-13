import numpy as np
from tqdm import tqdm, trange
import random
import keyboard

q_table_dimension = [1536, 3] 
q_table = np.zeros(q_table_dimension)

learning_rate = 0.7                                      
max_steps = 99             
gamma = 0.95
max_epsilon = 1.0           
min_epsilon = 0.05           
decay_rate = 0.0005 
epsilon = max_epsilon
n_episodes = 10000
max_steps = 100

def encode_state(state):
  lane = state[0]  # Lane position (0, 1, or 2)
  
  # Convert pylon rows to 3-bit integers
  row1 = state[1][0] * 4 + state[1][1] * 2 + state[1][2] * 1  # [1, 0, 0] -> 4
  row2 = state[2][0] * 4 + state[2][1] * 2 + state[2][2] * 1  # [0, 0, 0] -> 0
  row3 = state[3][0] * 4 + state[3][1] * 2 + state[3][2] * 1  # [0, 0, 1] -> 1
  
  # Combine lane and rows into one integer (we can use a base-8 system for each part)
  # We'll shift row values to make space for the lane
  encoded_state = lane + row1 * 3**1 + row2 * 3**2 + row3 * 3**3
  
  return encoded_state


def random_lane():
  return random.randint(0,2)

def get_pylon_row():
  row = [0, 0, 0]
  lane = random_lane()
  lane2 = random_lane()
  row[lane] = 1
  row[lane2] = 1
  return row

def get_empty_row():
  return [0, 0, 0]


def generate_inital_state():
  row1 = get_pylon_row()
  row2 = get_empty_row()
  row3 = get_pylon_row()
  state = [1, row1, row2, row3]
  return state

# [1, 0, 0] 1
# [0, 0, 0] 2
# [0, 1, 0] 3

# two_empty means there are two empty rows
def run_tick(action, state):
  reward = 0
  new_state = state
  new_car_position = 0
  if action == 0 and state[0] == 0:
    new_car_position = 0
  elif action == 2 and state[0] == 2:
    new_car_position = 2
  elif state[0] == 1:
    new_car_position = action
  elif state[0] == 0 and action == 2 or state[0] == 2 and action == 0:
    new_car_position = 1

  two_empty = state[1] == [0, 0, 0]
  if two_empty:
    new_state = [new_car_position, get_pylon_row(), state[1], state[2]]
  else:
    new_state = [new_car_position, get_empty_row(), state[1], state[2]]
    reward += 10

  # car_position = state[0]
  # if state[3][car_position] == 1 and action != 1:
  #   reward += 50
    
  if state[3][new_car_position] == 1:
    reward -= 100
  else:
    reward += 10                       
  return new_state, reward


def epsilon_greedy_policy(q_table, state, epsilon):
  """
  depending on epsilon, either the best action is chosen or a random action is chosen
  action is 0, 1, or 2 representing moving left, staying, or moving right
  """

  random_int = random.uniform(0,1)
  if random_int > epsilon:
    # the "best" action is chosen, or the action with highest q value, given the state
    action = np.argmax(q_table[state])
  else:
    # random action
    action = random.randint(0, 2)
  return action



def greedy_policy(q_table, state):
  """
  Used when the q_table is done training
  """
  print("action values:", q_table[state])
  action = np.argmax(q_table[state])
  return action



def train(n_episodes, min_epsilon, max_epsilon, decay_rate, max_steps, q_table):
    """
    train method that takes in hyperparameters and returns a good Q table for the game
    """

    # loop that itertaes through entire training process n_episodes number of times
    for episode in trange(n_episodes):
    # trange is like range but will display a progress bar, from tqdm library

        # epsiolon updated at the start of the loop
        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)

        # TODO: create/reset environment, provide initial/random state
        state = generate_inital_state()

        # this is the loop of the game in one episode, so step is each tick, action, etc.
        for step in range(max_steps):
           encoded_state = encode_state(state)
           
           action = epsilon_greedy_policy(q_table, encoded_state, epsilon)

           new_state, reward = run_tick(action, state)

           
           encoded_new_state = encode_state(new_state)
           # learning rate is how much the q-value is updated based on new info
           # gamma is the time discount factor - the importance of future rewards
           # reward is the immediate reward for taking the action
           q_table[encoded_state][action] = q_table[encoded_state][action] + learning_rate * (reward + gamma * np.max(q_table[encoded_new_state]) - q_table[encoded_state][action])

           # update the state 
           state = new_state

    return q_table



trained_q_table = train(n_episodes, min_epsilon, max_epsilon, decay_rate, max_steps, q_table)

def test_ai():
  state = generate_inital_state() 
  total_reward = 0
  print(state[1])
  print(state[2])
  print(state[3])
  print(state[0])
  print("Reward:", total_reward)
  encoded_state = encode_state(state)
  for i in range(100):
    encoded_state = encode_state(state)
    print("---------------------------------------------")
    keyboard.wait("space")
    ai_action = greedy_policy(trained_q_table, encoded_state)
    new_state, reward = run_tick(ai_action, state) 
    print("state:", encoded_state)
    print("Action:", ai_action)                      
    print(new_state[1])
    print(new_state[2])
    print(new_state[3])
    print(new_state[0])
    total_reward += reward
    print("Reward:", total_reward)                      
    state = new_state
  
test_ai()

