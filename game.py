import pygame
import random
import time

pygame.init()

width = 800
height = 600

# def is_touching(object_1_dimensions, object_2_dimensions):


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Claude")

car = pygame.image.load('car.png')
pylon = pygame.image.load('traffic_cone.png')
cones = []
last_spawn_time = time.time()
spawn_interval = 1.5

# Scale the images to a smaller size (e.g., 50% of original size)
scaled_width = car.get_width() / 1.5
scaled_height = car.get_height() / 1.5
car = pygame.transform.scale(car, (scaled_width, scaled_height))
pylon = pygame.transform.scale(pylon, (pylon.get_width() / 20, pylon.get_height() / 20))

def display_car(x, y):
    screen.blit(car, (x, y))

def display_pylon(x, y):
    screen.blit(pylon, (x, y))

def display_game_over():
    font = pygame.font.SysFont('comicsansms', 100)
    text = font.render("PEEPEE WHACK", True, (255, 0, 0))  # Red color
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))

car_width = car.get_width()
car_height = car.get_height()
car_pos = [(width // 2) - car_width // 2, height - car_height]
car_speed = 0.5

road_color = ((55, 55, 55))
road_width = 400
road_x = (width - road_width) // 2

lane_width = road_width / 3
lane_positions = [road_x, road_x + lane_width, road_x + 2 * lane_width]
current_lane = 1  # Middle lane

pylon_pos = [road_x + lane_width * random.randint(0, 2) + (lane_width - pylon.get_width()) // 2, 0]
pylon_tick_size = pylon.get_height()  # Amount to move per tick
last_tick_time = pygame.time.get_ticks()  # Track time for snap movement
tick_rate = 200  # Time in milliseconds between each tick

running = True
game_over = False
target_lane = 1
score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((124, 252, 0))

    # Draw the road (a rectangle in the middle of the screen)


    pygame.draw.rect(screen, road_color, (road_x, 0, road_width, height))

    for i in range(1, 3):
        pygame.draw.line(screen, (255, 255, 255), (road_x + lane_width * i, 0), (road_x + lane_width * i, height), 5)
    if not game_over:
        # game logic will go here.
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and current_lane > 0:
            target_lane = current_lane - 1  # Move to the left lane
        if keys[pygame.K_RIGHT] and target_lane < 2:
            target_lane = current_lane + 1  # Move to the right lane

        # Smoothly transition the car horizontally towards the target lane
        if car_pos[0] < lane_positions[target_lane]:
            car_pos[0] += car_speed
        elif car_pos[0] > lane_positions[target_lane]:
            car_pos[0] -= car_speed

        # Stop car when it reaches the center of the target lane
        if abs(car_pos[0] - lane_positions[target_lane]) < car_speed:
            car_pos[0] = lane_positions[target_lane]
            current_lane = target_lane

        # LOGIC FOR SMOOTH CAR MOVEMENT. 
        # if keys[pygame.K_LEFT] and car_pos[0] > road_x:
        #     car_pos[0] -= car_speed
        # if keys[pygame.K_RIGHT] and car_pos[0] < road_x + road_width - car_width:
        #     car_pos[0] += car_speed

        current_time = pygame.time.get_ticks()
        if current_time - last_tick_time >= tick_rate:
            pylon_pos[1] += pylon_tick_size
            last_tick_time = current_time

        if pylon_pos[1] > height:
            pylon_pos = [random.choice(lane_positions) + (lane_width - pylon.get_width()) // 2, 0]

        # Create Rect objects for the car and pylon
        car_rect = pygame.Rect(car_pos[0], car_pos[1], car_width, car_height)
        pylon_rect = pygame.Rect(pylon_pos[0], pylon_pos[1], pylon.get_width(), pylon.get_height())
        if car_rect.colliderect(pylon_rect):
            game_over = True

        # Check for collision between the car and the pylon

        display_car(car_pos[0], car_pos[1])
        display_pylon(pylon_pos[0], pylon_pos[1])

        score += 1
        font = pygame.font.SysFont('comicsansms', 50)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    

    #     pylon_pos[1] += pylon_speed
    #     if pylon_pos[1] > height:
    #         pylon_pos = [road_x + lane_width * random.randint(0, 2) + (lane_width - pylon.get_width()) // 2, 0]
    else:
        display_game_over()
        if keys[pygame.K_RETURN]:
            game_over = False
            car_pos = [(width // 2) - car_width // 2, height - car_height]
            cones = []
            pylon_speed = 0.2
            spawn_interval = 1.5
            score = 0
    # Update the display
    pygame.display.update()