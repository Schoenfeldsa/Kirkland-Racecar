import pygame
import random

pygame.init()

width = 800
height = 600


# def is_touching(object_1_dimensions, object_2_dimensions):
    





screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Claude")

car = pygame.image.load('car.png')
pylon = pygame.image.load('traffic_cone.png')

# Scale the images to a smaller size (e.g., 50% of original size)
scaled_width = car.get_width() / 1.5
scaled_height = car.get_height() / 1.5
car = pygame.transform.scale(car, (scaled_width, scaled_height))
pylon = pygame.transform.scale(pylon, (pylon.get_width() / 20, pylon.get_height() / 20))

def display_car(x, y):
    screen.blit(car, (x, y))

def display_pylon(x, y):
    screen.blit(pylon, (x, y))

car_width = car.get_width()
car_height = car.get_height()
car_pos = [(width // 2) - car_width // 2, height - car_height]
car_speed = 1

road_color = ((55, 55, 55))
road_width = 400
road_x = (width - road_width) // 2

lane_width = road_width / 3

pylon_pos = [road_x + lane_width * random.randint(0, 2) + (lane_width - pylon.get_width()) // 2, 0]
pylon_speed = 0.2

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((124, 252, 0))

    # Draw the road (a rectangle in the middle of the screen)


    pygame.draw.rect(screen, road_color, (road_x, 0, road_width, height))

    for i in range(1, 3):
        pygame.draw.line(screen, (255, 255, 255), (road_x + lane_width * i, 0), (road_x + lane_width * i, height), 5)

    # game logic will go here.
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and car_pos[0] > road_x:
        car_pos[0] -= car_speed
    if keys[pygame.K_RIGHT] and car_pos[0] < road_x + road_width - car_width:
        car_pos[0] += car_speed
    # if keys[pygame.K_UP] and car_pos[1] > 0:
    #     car_pos[1] -= car_speed
    # if keys[pygame.K_DOWN] and car_pos[1] < height - car_height:
    #     car_pos[1] += car_speed



    display_car(car_pos[0], car_pos[1])
    display_pylon(pylon_pos[0], pylon_pos[1])
    pylon_pos[1] += pylon_speed
    if pylon_pos[1] > height:
        pylon_pos = [road_x + lane_width * random.randint(0, 2) + (lane_width - pylon.get_width()) // 2, 0]
    

    # Update the display
    pygame.display.update()


