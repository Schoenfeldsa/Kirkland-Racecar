import numpy as np
import pygame
import random

pygame.init()

board_width = 400
board_height = 500
screen_width = 700


car_width = 40
car_height = 80
pylon_width = 40
pylon_height = 60

BLACK = (55, 55, 55)
font = pygame.font.SysFont('Arial', 30)

screen = pygame.display.set_mode((screen_width, board_height))
pygame.display.set_caption("2-eyed Q")

car_image = pygame.image.load('car.png')
pylon_image = pygame.image.load('traffic_cone.png')

car_image = pygame.transform.scale(car_image, (car_width, car_height))
pylon_image = pygame.transform.scale(pylon_image, (pylon_width // 1.2, pylon_height// 1.2))

width_range = [0, board_width - car_width]

def get_random_width():
    return random.randint(0, board_width - car_width)


def create_initial_state():
    car_position = (board_width / 2) - (car_width / 2)
    pylon1 = [get_random_width(), random.randint(0, board_height - pylon_height * 3)]
    pylon2 = [get_random_width(), random.randint(0, board_height - pylon_height * 3)]
    pylon3 = [get_random_width(), random.randint(0, board_height - pylon_height * 3)]
    pylon4 = [get_random_width(), random.randint(0, board_height - pylon_height * 3)]
    pylon5 = [get_random_width(), random.randint(0, board_height - pylon_height * 3)]
    state = [car_position, pylon1, pylon2, pylon3, pylon4, pylon5]
    return state

def draw_pylons(state):
    # take in state, draw those pylons
    pylons = state[1:]  # Exclude the car position

    for pylon in pylons:
        pylon_x = pylon[0]
        pylon_y = pylon[1]
        screen.blit(pylon_image, (pylon_x, pylon_y))

def create_new_pylon(pylon):
    # create new pylon at a random width at the top of the screen  
    pylon[0] = get_random_width()  # Set a random x-coordinate
    pylon[1] = -pylon_height 

def draw_car(car_position):
    screen.blit(car_image, (car_position, board_height - car_height))

def run_tick(action, state):
    car_position = state[0]
    pylons = state[1:]

    # Update car position based on action
    if action == "0" and car_position > 0:
        car_position -= 40  # Move car left
    elif action == "2" and car_position < board_width - car_width:
        car_position += 40  # Move car right

    if car_position < 0:
        car_position = 0  # Prevent the car from going off the left side
    elif car_position > board_width - car_width:
        car_position = board_width - car_width

    # Move pylons down
    for pylon in pylons:
        pylon[1] += 50  # Move down by 50 pixels
        if pylon[1] > board_height:
            create_new_pylon(pylon)  # new pylon if go bye bye

    state[0] = car_position  # Update car position in the state
    return state

def user_action(event, state):
    action = None
    if event.key == pygame.K_LEFT:  # Move car left
        action = "0"
    elif event.key == pygame.K_RIGHT:  # Move car right
        action = "2"
    elif event.key == pygame.K_SPACE:  # Spacebar to advance game
        action = "1" 

    # Pass the action into run_tick to update the state
    state = run_tick(action, state)

    return state

def draw_stats(ai_action, state, q_value):
    pygame.draw.rect(screen, (50, 50, 50), (board_width, 0, board_width, board_height))
    stats_title = font.render("Statistics", True, (255, 255, 255))
    screen.blit(stats_title, (board_width + 20, 20))

    if ai_action == 0:
       ai_action = "Left"
    elif ai_action == 1:
       ai_action = "Stay"
    elif ai_action == 2:
       ai_action = "Right"

    stat_1_label = font.render("Next AI action:" + str(ai_action), True, (255, 255, 255))
    stat_2_label = font.render("State:" + str(state), True, (255, 255, 255))
    stat_3_label = font.render("Q-values:" + str(q_value), True, (255, 255, 255))

    screen.blit(stat_1_label, (board_width + 20, 60))
    screen.blit(stat_2_label, (board_width + 20, 100))
    screen.blit(stat_3_label, (board_width + 20, 140))

state = create_initial_state()
running = True
while running:
    screen.fill(BLACK)  # Clear screen for redrawing
    draw_pylons(state)  # Draw pylons
    draw_car(state[0])  # Draw the car


    # fix stats when we get actual numbers.
    draw_stats(1,2000, "damn")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            state = user_action(event, state)  

    pygame.display.flip()  # Update the screen
    pygame.time.wait(100)
# make method for movement, if K.LEft, action 0 so go left....