#Modules and Packages
import pygame
import time
import random


# Classes
class dino():
    def __init__(self, width, height):
        self.width = 50
        self.height = 50
        self.height_initial = self.height
        self.x = width/10.0
        self.y = height - self.height
        self.y_initial = height - self.height
        self.gravity = 2
        self.velocity = 0

    def run(self, height):
        self.velocity += self.gravity
        self.y += self.velocity
        if self.y > height - self.height:
            self.y = height - self.height
        if self.height < self.width:
            self.height *= 2
            self.y -= self.height/2.0

    def squat(self):
        if self.height >= self.width:
            self.height = self.height / 2
        self.y += self.height

    def jump(self, height):
        if player.y >= height - player.height:
            self.velocity = -20

    def draw(self, window, color):
        pygame.draw.rect(window, color,
                         (self.x, self.y, self.width, self.height))


class obstacle():
    def __init__(self, width, height, player, type, speed=10, ):
        types = [
            [player.y_initial, player.height_initial, 5],
            [player.y_initial - player.height_initial/2.0 - 10,
                player.height_initial/2.0, player.width],
            [player.y_initial -
                10, player.height_initial/2.0, player.width]
        ]
        self.type = type
        self.x = width
        self.y = types[self.type][0]
        self.height = types[self.type][1]
        self.width = types[self.type][2]
        self.speed = speed
        self.acceleration = 0.007

    def update_pos(self):
        self.speed += self.acceleration
        self.x -= self.speed

    def draw(self, window, color):
        pygame.draw.rect(window, color,
                         (self.x, self.y, self.width, self.height), 5)


# Variables
width = 800
height = 600
fps = pygame.time.Clock()
background_color = (0, 0, 0)  # (#000000)
player_color = (255, 255, 0)  # (#ffff00)
obstacle_color = (255, 255, 0)  # (#ffff00)
pygame.init()
window = pygame.display.set_mode((width, height))

player = dino(width, height)
obs = []

running = True
squat = False
jump = False
score = 0

# Functions


def obstacles(obs):
    if len(obs) < 3:
        if score < random.randint(5, 10):
            type = 0
        else:
            type = random.randint(0, 2)

        if len(obs) > 0 and obs[-1].x < 0.4*width:
            ob = obstacle(width, height, player,  type, obs[-1].speed)
            obs.append(ob)
        elif len(obs) == 0:
            ob = obstacle(width, height, player, type)
            obs.append(ob)


def update_obstacles(obs, score):
    for i in range(len(obs)):
        obs[i].update_pos()
    if obs[0].x < 0 - width/2.0:
        obs.pop(0)
        score += 1
    return score, obs


def draw_obstacles(obs):
    for i in range(len(obs)):
        obs[i].draw(window, obstacle_color)


def game_over(player, obs):
    for i in obs:
        if i.y <= player.y <= i.y+i.height or i.y <= player.y+player.height <= i.y+i.height:
            if player.x <= i.x <= player.x+player.width or player.x <= i.x+i.width <= player.x+player.width:
                return False
    return True


def text_to_screen_score(window, score, pos, text):
    font = pygame.font.SysFont(None, 50)
    stext = text + str(score)
    score_text = font.render(stext, True, (255, 255, 255))
    window.blit(score_text, pos)
    pygame.display.update()


# Main code
while running:
    running = game_over(player, obs)
    window.fill(background_color)
    player.draw(window, player_color)

    obstacles(obs)

    draw_obstacles(obs)

    player.run(height)
    score, obs = update_obstacles(obs, score)
    ###Controls###
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                jump = True
            if event.key == pygame.K_DOWN:
                squat = True
        else:
            squat = False
            jump = False

    if squat == True:
        player.squat()
    if jump and not squat:
        player.jump(height)
    ##############
    text_to_screen_score(window, score, (20, 20), "score: ")
    fps.tick(27)
    pygame.display.update()

time.sleep(1)
window.fill(background_color)
text_to_screen_score(
    window, score, (width / 2.0, height / 2.0), "Your score is: ")
time.sleep(3)
