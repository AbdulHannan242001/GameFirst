import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
running = True
dt = 0
# set up the player
player1_pos= pygame.Vector2(screen.get_width() - 20, screen.get_height()/2)
player2_pos = pygame.Vector2(0, screen.get_height()/2)
player1_colided = False


center_line_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
# set up the ball
ball_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
ball_velocity = [300, 300]
ball_radius = 20

# load the sprites
# Plus Sprite
plus_sprite = pygame.image.load("plus.png").convert_alpha()
frame_width = plus_sprite.get_width() // 4
frame_height = plus_sprite.get_height()
frame_count = 4
scaled_width, scaled_height = 200, 200

# extract frames from sprite sheet and scale them
frames = []
for i in range(frame_count):
    frame_x = i * frame_width
    frame_rect = pygame.Rect(frame_x, 0, frame_width, frame_height)
    frame_image = plus_sprite.subsurface(frame_rect)
    frame_image = pygame.transform.scale(frame_image, (scaled_width, scaled_height))
    frames.append(frame_image)
    
# animate the plus sprite
current_frame = 0
frame_timer = 0
frame_interval = 0.1


def animate_plus():
    global current_frame, frame_timer
    frame_timer += dt
    if frame_timer >= frame_interval:
        current_frame = (current_frame + 1) % frame_count
        frame_timer = 0
    return frames[current_frame]


def display_plus():
    plus_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
    screen.blit(animate_plus(), plus_pos)
    return plus_pos

isLost = False
font = pygame.font.Font(None, 36)
score = [0, 0]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill("#000000")
    
    #  ball position
    pygame.draw.circle(screen, "red", ball_pos, ball_radius)
    
    # def player(area, color, playerPos, width, height):
    #     pygame.draw.rect(screen, color, (playerPos.x, playerPos.y, width, height))
    class player:
        def __init__(self, color, playerPosX, playerPosY, width, height):
            self.color = color
            self.playerPosX = playerPosX
            self.playerPosY = playerPosY
            self.width = width
            self.height = height
            
        def draw(self, screen):
            pygame.draw.rect(screen, self.color, (self.playerPosX, self.playerPosY, self.width, self.height))
            
    player1 = player("blue", player1_pos.x, player1_pos.y, 20, 100)
    player1.draw(screen)
    player2 = player("blue", player2_pos.x, player2_pos.y, 20, 100)
    player2.draw(screen)

        
    # center line position
    pygame.draw.aaline(screen, "white", (center_line_pos.x, 0), (center_line_pos.x, screen.get_height()))
    
    keys = pygame.key.get_pressed()
     
    def registerKeys(keys):
        if keys[pygame.K_UP]:
            player1_pos.y -= 300 * dt
        if keys[pygame.K_DOWN]: 
            player1_pos.y += 300 * dt
        if keys[pygame.K_w]:
            player2_pos.y -= 300 * dt
        if keys[pygame.K_s]:
            player2_pos.y += 300 * dt
    registerKeys(keys)
    

    def moveBall(ball_pos):
        global player1_colided
        ball_pos.x += ball_velocity[0] * dt
        ball_pos.y += ball_velocity[1] * dt
        plus_position = display_plus()
        
        if ball_pos.y - ball_radius < 0:
            ball_velocity[1] *= -1
            ball_pos.y = ball_radius  # Reset to inside the boundary
        elif ball_pos.y + ball_radius > screen.get_height():
         ball_velocity[1] *= -1
         ball_pos.y = screen.get_height() - ball_radius  # Reset to inside the boundary
         
        #  Detect collision with player 1 and bounce the ball
        if ball_pos.y >= player1_pos.y and ball_pos.y <= player1_pos.y + 100 and ball_pos.x <= player1_pos.x + 20 and ball_pos.x >= player1_pos.x:
            ball_velocity[0] *= -1
            player1_colided = True
        #  Detect collision with player 2 and bounce the ball
        if ball_pos.y >= player2_pos.y and ball_pos.y <= player2_pos.y + 100 and ball_pos.x <= player2_pos.x + 20 and ball_pos.x >= player2_pos.x:
            ball_velocity[0] *= -1
            player1_colided = False
        print(plus_position[0])
        #  Detect collision with the sprite
        if ball_pos.y >= plus_position[1] and ball_pos.y <= plus_position[1] + 200 and ball_pos.x <= plus_position[0] + 200 and ball_pos.x >= plus_position[0]:
            if player1_colided == True:
                player1.height += 10
            else:
                player2.height += 10
            
    moveBall(ball_pos)
    
    def sliderMovement(player1_pos, player2_pos):
        if player1_pos.y <= 0:
            player1_pos.y = 0
        elif player1_pos.y + 100 >= screen.get_height():
            player1_pos.y = screen.get_height() - 100
        if player2_pos.y <= 0:
            player2_pos.y = 0
        elif player2_pos.y + 100 >= screen.get_height():
            player2_pos.y = screen.get_height() - 100
    
    sliderMovement(player1_pos, player2_pos)
    
    def countPoints(score, ball_pos):
        global isLost
        if ball_pos.x <= 0:
            score[0] += 1
            isLost = True
        elif ball_pos.x >= screen.get_width():
            score[1] += 1
            isLost = True
            
    countPoints(score, ball_pos)
    
    if isLost:
            resetBall(ball_velocity)
    
    def resetBall(ball_velocity):
        global isLost
        
        ball_pos.x = screen.get_width()/2
        ball_pos.y = screen.get_height()/2
        ball_velocity[0] = 300 * random.choice([-1, 1])
        ball_velocity[1] = 300 * random.choice([-1, 1])
        isLost = False
    
    def winner():
        if score[0] == 10 or score[1] == 10:
            global running
            isLost = True
            text = font.render(f"Player { score.index(max(score)) } wins", True, "white")
            text_rect = text.get_rect(center=screen.get_rect().center)
            screen.blit(text, text_rect)
            # stop the game
            running = False
    
    
    def displayScore(score):
        text = font.render(f"{score[0]} - {score[1]}", True, "white")
        text_pos = pygame.Vector2(screen.get_width()/2, 50)
        screen.blit(text, text_pos)
        winner()
    displayScore(score)
    
    display_plus()
    
    pygame.display.flip()
    dt = clock.tick(60)/1000
    
pygame.quit() 