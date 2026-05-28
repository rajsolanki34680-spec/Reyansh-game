import pygame
import random
import math
import os

pygame.init()
pygame.mixer.init()

# SCREEN
WIDTH = 1000
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Box Jump")

clock = pygame.time.Clock()

# COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (50,150,255)
RED = (255,60,60)
GREEN = (0,255,100)
YELLOW = (255,220,0)
GRAY = (170,170,170)
ORANGE = (255,120,0)
PURPLE = (180,0,255)

# FONTS
font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 60)
small_font = pygame.font.SysFont("Arial", 22)

# GROUND
ground_y = HEIGHT - 70

# PLAYER
player_size = 50
player_x = 120
player_y = HEIGHT - 120
player_vel_y = 0
gravity = 0.8
jump_power = -15
on_ground = True
jump_count = 0
max_jumps = 2

player_color = BLUE

# SCORE
score = 0
coins = 0

# HIGH SCORE SAVE
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())
else:
    high_score = 0

# GAME STATES
game_over = False
paused = False
menu = True

# BACKGROUND MODE
backgrounds = [
    (135,206,235),
    (255,180,120),
    (40,40,70),
    (180,240,180)
]
background_index = 0

# ENEMIES
obstacles = []
coins_list = []
clouds = []
particles = []

# SHIELD
shield = False
shield_timer = 0

# TOUCH BUTTON
jump_button = pygame.Rect(WIDTH - 130, HEIGHT - 130, 100, 100)

# CLOUDS
for i in range(5):
    clouds.append([
        random.randint(0, WIDTH),
        random.randint(40, 180),
        random.randint(40, 100)
    ])

# CREATE OBSTACLE

def create_obstacle():

    obstacle_type = random.choice([
        "triangle",
        "square",
        "diamond",
        "fire"
    ])

    boss = False

    if score > 0 and score % 20 == 0:
        boss = True

    size = random.randint(40, 60)

    if boss:
        size = 120

    obstacle = {
        "x": WIDTH + 100,
        "y": ground_y - size + 10,
        "size": size,
        "speed": 8 + score * 0.1,
        "angle": 0,
        "rotation": random.randint(3,8),
        "shape": obstacle_type,
        "boss": boss
    }

    obstacles.append(obstacle)

# CREATE COIN

def create_coin():

    c = {
        "x": WIDTH + random.randint(200, 600),
        "y": random.randint(160, 320),
        "size": 20,
        "speed": 7
    }

    coins_list.append(c)

create_obstacle()
create_coin()

# PARTICLES

def create_particles(x,y,color):

    for i in range(30):

        particles.append({
            "x": x,
            "y": y,
            "vx": random.uniform(-6,6),
            "vy": random.uniform(-6,6),
            "life": random.randint(20,40),
            "size": random.randint(3,7),
            "color": color
        })

# DRAW OBSTACLE

def draw_obstacle(o):

    size = o["size"]

    surface = pygame.Surface((size*2,size*2), pygame.SRCALPHA)

    if o["shape"] == "triangle":

        pygame.draw.polygon(surface, RED, [
            (size,0),
            (0,size*2),
            (size*2,size*2)
        ])

    elif o["shape"] == "square":

        pygame.draw.rect(surface, GREEN, (size//2,size//2,size,size))

    elif o["shape"] == "diamond":

        pygame.draw.polygon(surface, YELLOW, [
            (size,0),
            (0,size),
            (size,size*2),
            (size*2,size)
        ])

    elif o["shape"] == "fire":

        pygame.draw.circle(surface, ORANGE, (size,size), size)
        pygame.draw.circle(surface, YELLOW, (size,size), size//2)

    rotated = pygame.transform.rotate(surface, o["angle"])

    rect = rotated.get_rect(center=(o["x"], o["y"]))

    screen.blit(rotated, rect)

# MAIN LOOP
running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                paused = not paused

            if event.key == pygame.K_1:
                player_color = BLUE

            if event.key == pygame.K_2:
                player_color = PURPLE

            if event.key == pygame.K_3:
                player_color = GREEN

        if event.type == pygame.MOUSEBUTTONDOWN or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
        ):

            mouse_pos = pygame.mouse.get_pos()

            if menu:
                menu = False

            elif game_over:

                if score > high_score:
                    high_score = score

                    with open("highscore.txt", "w") as f:
                        f.write(str(high_score))

                score = 0
                coins = 0
                game_over = False
                obstacles.clear()
                coins_list.clear()
                particles.clear()

                player_y = HEIGHT - 120
                player_vel_y = 0

                create_obstacle()
                create_coin()

            else:

                if jump_count < max_jumps:
                    player_vel_y = jump_power
                    jump_count += 1

    # BACKGROUND
    screen.fill(backgrounds[background_index])

    # CLOUDS
    for c in clouds:

        pygame.draw.ellipse(screen, WHITE, (c[0], c[1], c[2], 40))

        c[0] -= 2

        if c[0] < -120:
            c[0] = WIDTH + 100

    # GROUND
    pygame.draw.rect(screen, GRAY, (0, ground_y, WIDTH, 80))

    if menu:

        title = big_font.render("ULTIMATE BOX JUMP", True, BLACK)
        play = font.render("CLICK TO PLAY", True, BLACK)

        screen.blit(title, (WIDTH//2 - 280, 150))
        screen.blit(play, (WIDTH//2 - 120, 260))

    elif not paused and not game_over:

        # PLAYER PHYSICS
        player_vel_y += gravity
        player_y += player_vel_y

        if player_y >= HEIGHT - 120:
            player_y = HEIGHT - 120
            player_vel_y = 0
            jump_count = 0

        # PLAYER
        pygame.draw.rect(
            screen,
            player_color,
            (player_x, player_y, player_size, player_size),
            border_radius=10
        )

        # SHIELD EFFECT
        if shield:
            pygame.draw.circle(
                screen,
                (100,200,255),
                (player_x + 25, player_y + 25),
                40,
                4
            )

            shield_timer -= 1

            if shield_timer <= 0:
                shield = False

        # OBSTACLES
        for o in obstacles[:]:

            o["x"] -= o["speed"]
            o["angle"] += o["rotation"]

            draw_obstacle(o)

            player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

            obstacle_rect = pygame.Rect(
                o["x"] - o["size"]//2,
                o["y"] - o["size"]//2,
                o["size"],
                o["size"]
            )

            if player_rect.colliderect(obstacle_rect):

                if shield:
                    shield = False
                    obstacles.remove(o)
                    create_particles(o["x"], o["y"], BLUE)
                    continue

                create_particles(player_x+25, player_y+25, RED)
                game_over = True

            if o["x"] < -150:

                obstacles.remove(o)
                score += 1

                if score % 10 == 0:
                    background_index = (background_index + 1) % len(backgrounds)

                if random.randint(1,4) == 1:
                    shield = True
                    shield_timer = 500

                create_obstacle()

        # COINS
        for c in coins_list[:]:

            c["x"] -= c["speed"]

            pygame.draw.circle(screen, YELLOW, (int(c["x"]), int(c["y"])), c["size"])
            pygame.draw.circle(screen, ORANGE, (int(c["x"]), int(c["y"])), c["size"], 4)

            coin_rect = pygame.Rect(c["x"]-20, c["y"]-20, 40, 40)
            player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

            if player_rect.colliderect(coin_rect):
                coins += 1
                create_particles(c["x"], c["y"], YELLOW)
                coins_list.remove(c)
                create_coin()

            elif c["x"] < -50:
                coins_list.remove(c)
                create_coin()

        # PARTICLES
        for p in particles[:]:

            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= 1

            pygame.draw.circle(screen, p["color"], (int(p["x"]), int(p["y"])), p["size"])

            if p["life"] <= 0:
                particles.remove(p)

        # JUMP BUTTON
        pygame.draw.circle(screen, BLUE, jump_button.center, 50)
        txt = font.render("JUMP", True, WHITE)
        screen.blit(txt, (jump_button.x + 10, jump_button.y + 30))

        # SCORE
        score_text = font.render(f"Score : {score}", True, BLACK)
        hi_text = font.render(f"HI : {high_score}", True, BLACK)
        coin_text = font.render(f"Coins : {coins}", True, BLACK)

        screen.blit(score_text, (20,20))
        screen.blit(hi_text, (20,60))
        screen.blit(coin_text, (20,100))

        skin_text = small_font.render("Press 1/2/3 for skins", True, BLACK)
        screen.blit(skin_text, (20,140))

    elif paused:

        pause_text = big_font.render("PAUSED", True, BLACK)
        screen.blit(pause_text, (WIDTH//2 - 120, 200))

    else:

        over = big_font.render("YOU DIED", True, RED)
        restart = font.render("CLICK TO RESTART", True, BLACK)

        screen.blit(over, (WIDTH//2 - 170, 160))
        screen.blit(restart, (WIDTH//2 - 140, 250))

    pygame.display.update()

pygame.quit()