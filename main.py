import pygame
import random

pygame.init()

# Screen setup
SCREEN_HEIGHT, SCREEN_WIDTH = 720, 1280
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
dt = 0
CENTER_LINE_POS = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

# Constants
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_RADIUS = 15
PADDLE_SPEED = 300
BALL_SPEED = 300
FRAME_INTERVAL = 0.1
WINNING_SCORE = 10
SCORE_FONT_SIZE = 36
SCALED_WIDTH, SCALED_HEIGHT = 24, 24
player1_collided = None

# Ball setup
ball_velocity = [BALL_SPEED * random.choice([-1, 1]), BALL_SPEED * random.choice([-1, 1])]

# Load the sprite
plus_sprite = pygame.image.load("plus.png").convert_alpha()
frame_width = plus_sprite.get_width() // 4
frame_height = plus_sprite.get_height()
frames = [
    pygame.transform.scale(plus_sprite.subsurface((i * frame_width, 0, frame_width, frame_height)), (SCALED_WIDTH, SCALED_HEIGHT))
    for i in range(4)
]
current_frame = 0
frame_timer = 0

# Score setup
font = pygame.font.Font(None, SCORE_FONT_SIZE)
score = [0, 0]
is_lost = False

# Classes
class Player:
    def __init__(self, color, x, y, height):
        self.color = color
        self.pos = pygame.Vector2(x, y)
        self.height = height

    def draw(self, width):
        pygame.draw.rect(screen, self.color, (self.pos.x, self.pos.y, width, self.height))

    def move(self, direction):
        self.pos.y += direction * PADDLE_SPEED * dt
        self.pos.y = max(0, min(SCREEN_HEIGHT - self.height, self.pos.y))

class Ball:
    def __init__(self):
        self.pos = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.velocity = pygame.Vector2(*ball_velocity)
        
    def draw(self):
        pygame.draw.circle(screen, "white", self.pos, BALL_RADIUS)

    def move(self):
        self.pos += self.velocity * dt
        if self.pos.y - BALL_RADIUS < 0 or self.pos.y + BALL_RADIUS > SCREEN_HEIGHT:
            self.velocity.y *= -1
        return self.pos

    def reset(self):
        global player1_collided
        self.pos = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.velocity = pygame.Vector2(BALL_SPEED * random.choice([-1, 1]), BALL_SPEED * random.choice([-1, 1]))
        player1_collided = None
        print(f'reset to false', player1_collided)
        
class Power:
    def __init__(self, x, y, current_frame, frame_timer):
        self.x = x
        self.y = y
        self.current_frame = current_frame
        self.frame_timer = frame_timer
        
    def draw(self):
        self.frame_timer += dt
        if self.frame_timer >= FRAME_INTERVAL:
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.frame_timer = 0
        screen.blit(frames[self.current_frame], (self.x, self.y))
        

# Functions
def handle_collision(ball, player1, player2):
    global player1_collided
    if player1.pos.y <= ball.pos.y <= player1.pos.y + player1.height and player1.pos.x <= ball.pos.x + BALL_RADIUS <= player1.pos.x + PADDLE_WIDTH:
        ball.velocity.x *= -1
        player1_collided = True

    if player2.pos.y <= ball.pos.y <= player2.pos.y + player2.height and player2.pos.x + ball.pos.x - BALL_RADIUS <= player2.pos.x + PADDLE_WIDTH:
        ball.velocity.x *= -1
        player1_collided = False
        
    if power.x - BALL_RADIUS <= ball.pos.x <= power.x + SCALED_WIDTH + BALL_RADIUS and power.y - BALL_RADIUS <= ball.pos.y <= power.y + SCALED_HEIGHT + BALL_RADIUS:
        if player1_collided == True:
            player1.height += 10
        elif player1_collided == False:
            player2.height += 10
    # create a red rectangle around the power up
    pygame.draw.rect(screen, "red", (power.x - 5, power.y - 5, SCALED_WIDTH + 10, SCALED_HEIGHT + 10), 2)

def count_points(ball):
    global is_lost
    if ball.pos.x < 0:
        score[1] += 1
        is_lost = True
    elif ball.pos.x > SCREEN_WIDTH:
        score[0] += 1
        is_lost = True

def display_score():
    text = font.render(f"{score[0]} - {score[1]}", True, "white")
    screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, 50))

def check_winner():
    if max(score) == WINNING_SCORE:
        text = font.render(f"Player {score.index(max(score)) + 1} wins!", True, "white")
        screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 2))
        return True
    return False

# Game setup
player1 = Player("blue", SCREEN_WIDTH - PADDLE_WIDTH, SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_HEIGHT)
player2 = Player("red", 0, SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_HEIGHT)
ball = Ball()
power = Power(random.randint(25, SCREEN_WIDTH - 25), random.randint(25, SCREEN_HEIGHT - 25), current_frame, frame_timer)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("#000000")
    pygame.draw.aaline(screen, "white", (CENTER_LINE_POS.x, 0), (CENTER_LINE_POS.x, SCREEN_HEIGHT))
    
    # Player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player1.move(-1)
    if keys[pygame.K_DOWN]:
        player1.move(1)
    if keys[pygame.K_w]:
        player2.move(-1)
    if keys[pygame.K_s]:
        player2.move(1)

    # Game mechanics
    ball.move()
    handle_collision(ball, player1, player2)
    count_points(ball)

    if is_lost:
        ball.reset()
        is_lost = False

    if check_winner():
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    # Drawing
    player1.draw(PADDLE_WIDTH)
    player2.draw(PADDLE_WIDTH)
    ball.draw()
    display_score()
    power.draw()

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
