import pygame
import random
import numpy as np
import keyboard
from tqdm import tqdm, trange

 
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


def generate_inital_state():
  row1 = get_pylon_row()
  row2 = get_empty_row()
  row3 = get_pylon_row()
  state = [1, row1, row2, row3]
  return state



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
  action = np.argmax(q_table[state])
  return action


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
  elif action == 1 and state[0] == 2:
    new_car_position = 2

  two_empty = state[1] == [0, 0, 0]
  if two_empty:
    new_state = [new_car_position, get_pylon_row(), state[1], state[2]]
  else:
    new_state = [new_car_position, get_empty_row(), state[1], state[2]]
    reward += 10
  
  if state[3][state[0]] == 1:
     reward -= 10
    
  if state[3][new_car_position] == 1:
    reward -= 100
  else:
    reward += 10                       
  return new_state, reward

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

# Training complete, q table filled

pygame.init() 

# Screen dimensions
screen_width = 300
screen_height = 400
board_rows = 4
board_cols = 3
row_height = screen_height // board_rows

# Screen setup
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Claude")

# Load images
car_image = pygame.image.load('car.png')
pylon_image = pygame.image.load('traffic_cone.png')

# Scale images
car_image = pygame.transform.scale(car_image, (car_image.get_width() // 2, car_image.get_height() // 2))
pylon_image = pygame.transform.scale(pylon_image, (pylon_image.get_width() // 20, pylon_image.get_height() // 20))

# Game variables
board = np.zeros((board_rows, board_cols))
BLACK = (0, 0, 0)
road_color = (55, 55, 55)
road_width = 300
road_x = (screen_width - road_width) // 2
lane_width = road_width / 3
lane_positions = [road_x, road_x + lane_width, road_x + 2 * lane_width]
car_width = car_image.get_width()
car_height = car_image.get_height()

# Pylon setup
pylon_width = pylon_image.get_width()
pylon_height = pylon_image.get_height()


# Text box
side_box_width = 100
TEXT_COLOR = (255, 255, 255)

font = pygame.font.SysFont('Arial', 30)

text_box_rect = pygame.Rect(screen_width - side_box_width, 0, side_box_width, screen_height)

def display_text(text):
    text_surface = font.render(text, True, TEXT_COLOR)
    screen.blit(text_surface, (0, 10))

# Game state
running = True
turn_progressed = False

def draw_grid():
    screen.fill((124, 252, 0))  # Grass background
    pygame.draw.rect(screen, road_color, (road_x, 0, road_width, screen_height))  # Road
    for x in range(1, board_cols):
        pygame.draw.line(screen, BLACK, (road_x + x * lane_width, 0), (road_x + x * lane_width, screen_height), 2)
    for y in range(1, board_rows):
        pygame.draw.line(screen, BLACK, (road_x, y * (screen_height // board_rows)), 
                         (road_x + road_width, y * (screen_height // board_rows)), 2)

def draw_pylons(state, row4):
   rows = state[1:] + [row4]
   for row_index, row in enumerate(rows):
        for column_index, pylon in enumerate(row):
            if pylon == 1:
                pylon_x = column_index * lane_width + (lane_width // 2) - (pylon_image.get_width() // 2)
                pylon_y = row_index * 100

                screen.blit(pylon_image, (pylon_x, pylon_y))


def draw_car(state):
   car_pos = [lane_positions[state[0]], screen_height - car_height - 10]
   screen.blit(car_image, car_pos)


state = generate_inital_state()
total_reward = 0
row4 = [0, 0, 0]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            try:
                draw_grid()
                draw_car(state)
                draw_pylons(state, row4)

                encoded_state = encode_state(state)
                ai_action = greedy_policy(trained_q_table, encoded_state)
                rounded_q_values = np.round(trained_q_table[encoded_state], decimals = 2)
                display_text(str(rounded_q_values))

                new_state, reward = run_tick(ai_action, state)

                total_reward += reward
                row4 = state[3]
                state = new_state

                pygame.display.flip()
                pygame.time.wait(100) 
                 
            except Exception as e:
                print(f"Error: {e}")
                running = False
   