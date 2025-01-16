import numpy as np
import pygame
import random

screen_width = 400
screen_height = 300

car_width = 40
car_height = 80
pylon_width = 40
pylon_height = 60


car_image = pygame.image.load('car.png')
pylon_image = pygame.image.load('traffic_cone.png')

car_image = pygame.transform.scale(car_image, (car_width, car_height))
pylon_image = pygame.transform.scale(pylon_image, (pylon_width, pylon_height))

width_range = [0, screen_width - car_width]

def get_random_width():
    return random.randint(0, screen_width - car_width)


def create_initial_state():
    car_position = (screen_width / 2) - (car_width / 2)
    pylon1 = [get_random_width(), random.randint(0, screen_height - pylon_height * 3)]
    pylon2 = [get_random_width(), random.randint(0, screen_height - pylon_height * 3)]
    pylon3 = [get_random_width(), random.randint(0, screen_height - pylon_height * 3)]
    pylon4 = [get_random_width(), random.randint(0, screen_height - pylon_height * 3)]
    pylon5 = [get_random_width(), random.randint(0, screen_height - pylon_height * 3)]
    state = [car_position, pylon1, pylon2, pylon3, pylon4, pylon5]
    return state


initial_state = create_initial_state()
car_position = initial_state[0]

def draw_pylons():

    screen.blit()

def draw_car():
    screen.blit()