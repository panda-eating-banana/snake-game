# Import necessary libraries
import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Define colors
black = (0, 0, 0)        # Snake color
white = (255, 255, 255)  # Background color
red = (200, 0, 0)        # Poison block color
green = (34, 139, 34)    # Food color
dark_gray = (60, 60, 60) # Game screen background color

# Fonts for displaying messages and score
font_style = pygame.font.SysFont("bahnschrift", 30)
score_font = pygame.font.SysFont("comicsansms", 35)

# Game settings
snake_block = 20          # Size of each block in the snake
start_speed = 10          # Initial game speed
speed_increase = 0.3      # Speed increment per food consumed
max_speed = 20            # Maximum speed of the game

# Poison settings
poison_blocks = []              # List to store poison block positions
poison_block_timer = {}         # Timer for each poison block's lifespan
poison_interval_range = (5, 20) # Random interval (in seconds) for poison block spawn
poison_lifespan_range = (10, 30) # Lifespan (in seconds) of poison blocks

# Function to display the score
def your_score(score):
    value = score_font.render(f"Score: {score}", True, green)
    screen.blit(value, [0, 0])

# Function to draw the snake
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, black, [x[0], x[1], snake_block, snake_block], border_radius=5)

# Function to display messages on the screen
def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    text_width = mesg.get_width()
    x_pos = (width - text_width) / 2
    y_pos = height / 3 + y_offset
    screen.blit(mesg, [x_pos, y_pos])

# Function to generate a random position for food or poison blocks
def generate_food_or_poison():
    # Ensure the food/poison block is placed on a grid with snake block size
    return round(random.randrange(0, width - snake_block) / snake_block) * snake_block, \
           round(random.randrange(0, height - snake_block) / snake_block) * snake_block

# Function to spawn a poison block
def spawn_poison_block():
    # Generate a random position for the poison block and add it to the list
    poison_x, poison_y = generate_food_or_poison()
    poison_blocks.append((poison_x, poison_y))
    # Store the expiration time of the poison block (current time + random lifespan)
    poison_block_timer[(poison_x, poison_y)] = time.time() + random.randint(*poison_lifespan_range)

# Main game loop function
def game_loop():
    global poison_blocks, poison_block_timer

    # Reset the game state
    poison_blocks = []
    poison_block_timer = {}

    game_over = False       # Tracks if the game is over
    game_close = False      # Tracks if the player has lost

    # Snake starting position
    x1, y1 = width / 2, height / 2
    x1_change, y1_change = 0, 0

    # Snake body
    snake_list = []
    length_of_snake = 1

    # Food position
    foodx, foody = generate_food_or_poison()

    # Initial speed
    current_speed = start_speed
    clock = pygame.time.Clock()

    # Timer for poison block spawning
    next_poison_spawn_time = time.time() + random.randint(*poison_interval_range)

    # Wait for the player to press a key to start
    waiting_to_start = True
    while waiting_to_start:
        screen.fill(white)
        message("Press any arrow key to start", black)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    waiting_to_start = False
                    # Set initial direction based on the key pressed
                    if event.key == pygame.K_LEFT:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = snake_block
                        x1_change = 0

    # Main gameplay loop
    while not game_over:
        while game_close:
            # Display "Game Over" message and options to restart or quit
            screen.fill(white)
            message("Game Over!", red)
            message("Press R to Restart or Q to Quit", black, 50)
            your_score(length_of_snake - 1)
            pygame.display.update()

            # Handle events when game is over
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False  # Exit the game
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return False  # Exit the game
                    if event.key == pygame.K_r:
                        return True  # Restart the game

        # Handle movement and controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        # Wrap-around logic: makes the snake appear on the opposite side if it moves off-screen
        x1 = (x1 + x1_change) % width
        y1 = (y1 + y1_change) % height

        screen.fill(dark_gray)

        # Draw the food
        pygame.draw.rect(screen, green, [foodx, foody, snake_block, snake_block], border_radius=10)

        # Draw poison blocks and remove expired ones
        current_time = time.time()
        for poison in poison_blocks:
            pygame.draw.rect(screen, red, [poison[0], poison[1], snake_block, snake_block], border_radius=10)
            # Remove expired poison blocks
            if current_time > poison_block_timer[poison]:
                poison_blocks.remove(poison)
                del poison_block_timer[poison]

        # Spawn new poison blocks if the timer is up
        if current_time >= next_poison_spawn_time:
            spawn_poison_block()
            next_poison_spawn_time = current_time + random.randint(*poison_interval_range)

        # Update the snake's position and body
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check for collisions with the snake's own body
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        # Check for collisions with poison blocks
        for poison in poison_blocks:
            if x1 == poison[0] and y1 == poison[1]:
                game_close = True

        # Draw the snake and display the score
        our_snake(snake_block, snake_list)
        your_score(length_of_snake - 1)
        pygame.display.update()

        # Check if the snake eats the food
        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food_or_poison()  # Generate new food
            length_of_snake += 1  # Increase snake length
            current_speed = min(current_speed + speed_increase, max_speed)  # Increase speed up to a limit

        # Control the game speed
        clock.tick(current_speed)  # This controls the game speed (frames per second)

# Main loop to allow restarting the game
while True:
    if not game_loop():
        break

# Quit Pygame when the game ends
pygame.quit()
quit()
