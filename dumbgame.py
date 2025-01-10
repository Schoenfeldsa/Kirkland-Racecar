import pygame
import random
import numpy as np

pygame.init()

# Screen dimensions
width = 300
height = 400
board_rows = 4
board_cols = 3
row_height = height // board_rows

# Screen setup
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Claude")

# Load images
car = pygame.image.load('car.png')
pylon = pygame.image.load('traffic_cone.png')

# Scale images
car = pygame.transform.scale(car, (car.get_width() // 2, car.get_height() // 2))
pylon = pygame.transform.scale(pylon, (pylon.get_width() // 20, pylon.get_height() // 20))

# Game variables
board = np.zeros((board_rows, board_cols))
BLACK = (0, 0, 0)
road_color = (55, 55, 55)
road_width = 300
road_x = (width - road_width) // 2
lane_width = road_width / 3
lane_positions = [road_x, road_x + lane_width, road_x + 2 * lane_width]
current_lane = 1
target_lane = 1
car_width = car.get_width()
car_height = car.get_height()
car_pos = [lane_positions[current_lane], height - car_height - 10]
car_speed = 3

# Pylon setup
pylon_width = pylon.get_width()
pylon_height = pylon.get_height()
lane1 = random.choice(lane_positions)
lane2 = random.choice(lane_positions)
while lane2 == lane1:  # Make sure the second pylon is in a different lane
    lane2 = random.choice(lane_positions)

pylon_pos = [
    [lane1, 0],  # First pylon in a random lane
    [lane2, 0]   # Second pylon in a different random lane
]
turn_count = 0

def draw_grid():
    screen.fill((124, 252, 0))  # Grass background
    pygame.draw.rect(screen, road_color, (road_x, 0, road_width, height))  # Road
    for x in range(1, board_cols):
        pygame.draw.line(screen, BLACK, (road_x + x * lane_width, 0), (road_x + x * lane_width, height), 2)
    for y in range(1, board_rows):
        pygame.draw.line(screen, BLACK, (road_x, y * (height // board_rows)), 
                         (road_x + road_width, y * (height // board_rows)), 2)

def move_pylons():
    """Move pylons down one row."""
    for pos in pylon_pos[:]:
        pos[1] += 1
        if pos[1] >= board_rows:  # Reset pylon when it goes off-screen
            pylon_pos.remove(pos)

def spawn_pylons():
    lanes = random.sample(lane_positions, 2)  # Choose two random lanes
    for lane in lanes:
        pylon_pos.append([lane, 0]) 
# Game state
running = True
turn_progressed = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Background and road

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_SPACE]:
        turn_progressed = True
     # Handle player input for lane change
    if keys[pygame.K_LEFT] and current_lane > 0:
        current_lane -= 1
        car_pos[0] = lane_positions[current_lane]
    if keys[pygame.K_RIGHT] and current_lane < board_cols - 1:
        current_lane += 1
        car_pos[0] = lane_positions[current_lane]

    if turn_progressed:
        turn_count += 1
        move_pylons()
        if turn_count % 2 == 0:
            spawn_pylons()
        turn_progressed = False

    draw_grid()
    screen.blit(car, car_pos)
    for pos in pylon_pos:
        pylon_draw_y = pos[1] * row_height + (row_height - pylon.get_height()) // 2
        screen.blit(pylon, (pos[0], pylon_draw_y))

    pygame.display.flip()
    pygame.time.wait(100)
    #     # Smoothly move car to target lane
    #     if car_pos[0] < lane_positions[target_lane]:
    #         car_pos[0] += 1
    #     elif car_pos[0] > lane_positions[target_lane]:
    #         car_pos[0] -= 1

    #     # Adjust car position precisely when aligned with the target lane
    #     if abs(car_pos[0] - lane_positions[target_lane]) <= 2:
    #         car_pos[0] = lane_positions[target_lane]
    #         current_lane = target_lane

    #     if car_pos[0] < lane_positions[0]:
    #         car_pos[0] = lane_positions[0]
    #     elif car_pos[0] > lane_positions[2]:
    #         car_pos[0] = lane_positions[2]
    #     # Move the pylon only when the player has moved
    #     if car_pos[0] != lane_positions[current_lane] or keys[pygame.K_SPACE]:  # Only move the pylon if the car has moved
    #         pylon_pos[1] += 1
    #         if pylon_pos[1] > height:
    #             pylon_pos = [random.choice(lane_positions) + (lane_width - pylon_width) // 2, -pylon_height]
    #             score += 1

    #     # Collision detection
    #     car_rect = pygame.Rect(car_pos[0], car_pos[1], car_width, car_height)
    #     pylon_rect = pygame.Rect(pylon_pos[0], pylon_pos[1], pylon_width, pylon_height)
    #     if car_rect.colliderect(pylon_rect):
    #         game_over = True

        # Draw car and pylon
        # screen.blit(car, car_pos)
        # screen.blit(pylon, pylon_pos)

        # # Display score
        # score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        # screen.blit(score_text, (10, 10))

    # else:
    #     # Display game-over screen
    #     game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
    #     screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))

    #     # Check if enough time has passed since the last reset to allow restarting the game
    #     if keys[pygame.K_RETURN] and pygame.time.get_ticks() - last_reset_time >= reset_delay:
    #         reset_game()

    # pygame.display.flip()