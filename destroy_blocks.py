import os
import pygame
import traceback
from collections import deque
import random

os.chdir(os.path.dirname(__file__))

pygame.init()

# Definir janela que ocorrera o jogo
background = pygame.image.load('8320.png')
bg_main = pygame.image.load('main.png')
(width, height) = (800,680)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Destroy Blocks")

clock = pygame.time.Clock()
font12 = pygame.font.SysFont("Times New Roman",12)
font18 = pygame.font.SysFont("Times New Roman",18)
font24 = pygame.font.SysFont("Times New Roman",24)
font = pygame.font.SysFont("Indie Flower", 32)

BLUE = (0,0,255)
RED = (255,0,0)

    
class Game():
    def __init__(self):
        self.blocks_type = deque()
        self.line_org = [0,0,0,0]
        self.score_1 = 0
        self.score_2 = 0
        self.player1_x = 50
        self.player1_y = 440
        self.player2_x = 50
        self.player2_y = 500
        self.radius = 15

    def blocks(self):
        for i in range(0,2): self.line_org[2*i+1] = 1
        if self.blocks_type:
            if self.blocks_type[0][1][1] > height-100: self.blocks_type.popleft()
            for elem in self.blocks_type:
                elem[1][1] = elem[1][1] + 1
                if self.line_org[2*elem[3]] > 0 and self.line_org[2*elem[3]+1] == 1: 
                    self.line_org[2*elem[3]] = self.line_org[2*elem[3]] - 1
                    self.line_org[2*elem[3]+1] = 0
                pygame.draw.rect(screen, elem[0], (elem[1][0], elem[1][1], elem[1][2], elem[1][3]))
        
        line = random.randrange(1,7)
        color = random.randrange(2)
        if self.line_org[2*color] == 0:
            if self.blocks_type and self.blocks_type[-1][2] == line: return
            if color: block = [RED, [75*line,0,50,70], line, color]
            else: block = [BLUE, [75*line,0,50,70], line, color]
            self.blocks_type.append(block)
            self.line_org[2*color] = 100
            pygame.draw.rect(screen, block[0], (block[1][0], block[1][1], block[1][2], block[1][3]))

    def destroy(self, x, y, player):
        isRemove = False
        for elem in self.blocks_type:
            if elem[1][0] < x and (elem[1][0] + elem[1][2]) > x:
                if elem[1][1] < y and (elem[1][1] + elem[1][3]) > y:
                    if player == elem[3] or (player-2) == elem[3]:
                        isRemove = True
                        item = elem
                        break
        if isRemove: self.blocks_type.remove(item)

    def get_pressed(self):
        running = True
        while running:
            screen.fill((0, 0, 0))
            # Background Image
            screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running =  False
                if event.type == pygame.K_ESCAPE : running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.player1_x > self.radius:
                self.player1_x -= 1
            if keys[pygame.K_RIGHT] and self.player1_x < width - self.radius:
                self.player1_x += 1
            if keys[pygame.K_a] and self.player2_x > self.radius:
                self.player2_x -= 1
            if keys[pygame.K_d] and self.player2_x < width - self.radius:
                self.player2_x += 1
            if keys[pygame.K_DOWN]:
                self.destroy(self.player1_x, self.player1_y, 1)
            if keys[pygame.K_s]:
                self.destroy(self.player2_x, self.player2_y, 2)
            self.movement()
            pygame.draw.circle(screen, RED, (self.player1_x, self.player1_y), self.radius)
            pygame.draw.circle(screen, BLUE, (self.player2_x, self.player2_y), self.radius)
            pygame.display.update()
            clock.tick(200)

def button():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: return False
        if event.type == pygame.K_ESCAPE : return False
    return True

blink = -30
def draw():
    global blink
    screen.fill((255, 253, 208))
    screen.blit(bg_main,(0, 0))
    screen.blit(font.render("HIGHEST SCORE ",True,(0,0,0)),(150,550))
    pygame.display.flip()

def main():
    while True:
        if not button(): break
        draw()
    #game = Game()
    #game.get_pressed()

if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
        input()
