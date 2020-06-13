import os
import sys
import pygame
import traceback
from collections import deque
import random

os.chdir(os.path.dirname(__file__))

# Centralizar o jogo na tela do computador
if sys.platform in ["win32", "win64"]:
    os.environ["SDL_VIDEO_CENTERED"] = "1"

# Inicializar PyGame
pygame.init()

# Definir janela que ocorrerá o jogo
background = pygame.image.load('8320.png')
bg_main = pygame.image.load('main.png')

# Definir largura e comprimento da tela do jogo
(width, height) = (750, 700)
screen = pygame.display.set_mode((width, height))

# Definir nome do jogo
pygame.display.set_caption("Destroy Blocks")

clock = pygame.time.Clock()
font32 = pygame.font.SysFont("Indie Flower", 32)
font60 = pygame.font.SysFont("Indie Flower", 60)

# Arquivo para guardar o Highest Score
file = open("hs.txt", "r")
highest_score = int(file.read().strip())
file.close()

# Algumas definições de cores
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BUTTON_PRESSED = (230, 194, 62)
BUTTON_NON_PRESSED = (255, 235, 161)


class Game:
    def __init__(self, player):
        self.blocks_type = deque()
        self.line_org = [0, 0, 0, 0]
        self.score_1 = 0
        self.score_2 = 0
        self.radius = 15
        if player == 1:
            self.player1_x = 105
            self.player1_y = 635
            self.player2_x = 1000
            self.player2_y = 1000
        if player == 2:
            self.player1_x = 105
            self.player1_y = 590
            self.player2_x = 105
            self.player2_y = 655

    def blocks(self):
        for i in range(0, 2):
            self.line_org[2 * i + 1] = 1
        if self.blocks_type:
            if self.blocks_type[0][1][1] > height - 100:
                self.blocks_type.popleft()
            for elem in self.blocks_type:
                elem[1][1] = elem[1][1] + 3
                if self.line_org[2 * elem[3]] > 0 and self.line_org[2 * elem[3] + 1] == 1:
                    self.line_org[2 * elem[3]] = self.line_org[2 * elem[3]] - 1
                    self.line_org[2 * elem[3] + 1] = 0
                pygame.draw.rect(screen, elem[0], (elem[1][0], elem[1][1], elem[1][2], elem[1][3]))

        line = random.randrange(1, 7)
        color = random.randrange(2)
        if self.line_org[2 * color] == 0:
            if self.blocks_type and self.blocks_type[-1][2] == line:
                return
            if color:
                block = [RED, [115 + 95 * (line - 1), 0, 45, 70], line, color]
            else:
                block = [BLUE, [115 + 95 * (line - 1), 0, 45, 70], line, color]
            self.blocks_type.append(block)
            self.line_org[2 * color] = 100
            pygame.draw.rect(screen, block[0], (block[1][0], block[1][1], block[1][2], block[1][3]))

    def destroy(self, x, y, player):
        isRemove = False
        for elem in self.blocks_type:
            if elem[1][0] < x < (elem[1][0] + elem[1][2]):
                if elem[1][1] < y < (elem[1][1] + elem[1][3]):
                    if player == elem[3] or (player - 2) == elem[3]:
                        isRemove = True
                        item = elem
                        if player == 1:
                            self.score_1 = self.score_1 + 1
                        if player == 2:
                            self.score_2 = self.score_2 + 1
                        break
        if isRemove:
            self.blocks_type.remove(item)

    def to_dodge(self, x, y, player):
        isRemove = False
        for elem in self.blocks_type:
            if elem[1][0] < x < (elem[1][0] + elem[1][2]):
                if elem[1][1] < y < (elem[1][1] + elem[1][3]):
                    if not (player == elem[3] or (player - 2) == elem[3]):
                        isRemove = True
                        item = elem
                        if player == 1:
                            self.score_1 = self.score_1 - 1
                        if player == 2:
                            self.score_2 = self.score_2 - 1
                        break
        if isRemove:
            self.blocks_type.remove(item)

    def timer(self, stop):
        y_time = (1 - (stop - pygame.time.get_ticks()) / stop) * 200
        pygame.draw.rect(screen, WHITE, (260, 60, 200, 20))
        pygame.draw.rect(screen, BLACK, (260, 60, y_time, 20))

    def run(self, player, time):
        global highest_score
        running = True
        stop = pygame.time.get_ticks() + time * 1000 * 60
        while stop > pygame.time.get_ticks() and running:
            screen.fill((0, 0, 0))
            # Background Image
            if player == 1:
                screen.fill((0, 0, 0))
                screen.blit(background, (0, 0))
                # screen.blit(bg_player1, (0, 0))
                screen.blit(font60.render("HS: " + "{}".format(highest_score), True, (255, 255, 255)), (300, 20))
                screen.blit(font60.render("P: " + "{}".format(self.score_1), True, (255, 0, 0)), (30, 20))
            if player == 2:
                screen.blit(background, (0, 0))
                # screen.blit(bg_player2, (0, 0))
                screen.blit(font60.render("HS: " + "{}".format(highest_score), True, (255, 255, 255)), (300, 20))
                screen.blit(font60.render("P1: " + "{}".format(self.score_1), True, (255, 0, 0)), (30, 20))
                screen.blit(font60.render("P2: " + "{}".format(self.score_2), True, (0, 0, 255)), (600, 20))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.K_ESCAPE:
                    running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.player1_x > 105:
                self.player1_x -= 1
            if keys[pygame.K_RIGHT] and self.player1_x < 660 - self.radius:
                self.player1_x += 1
            if keys[pygame.K_a] and self.player2_x > 105:
                self.player2_x -= 1
            if keys[pygame.K_d] and self.player2_x < 660 - self.radius:
                self.player2_x += 1
            if keys[pygame.K_DOWN]:
                self.destroy(self.player1_x, self.player1_y, 1)
            if keys[pygame.K_s]:
                self.destroy(self.player2_x, self.player2_y, 2)
            self.to_dodge(self.player1_x, self.player1_y, 1)
            self.to_dodge(self.player2_x, self.player2_y, 2)
            self.blocks()
            self.timer(stop)
            pygame.draw.circle(screen, RED, (self.player1_x, self.player1_y), self.radius)
            pygame.draw.circle(screen, BLUE, (self.player2_x, self.player2_y), self.radius)
            pygame.display.update()
            clock.tick(200)
        return max(self.score_1, self.score_2)


def button(main_org):
    global highest_score
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.K_ESCAPE:
            return False
        if 215 + 60 > mouse[0] > 215:
            if 320 + 60 > mouse[1] > 320:
                if click[0] == 1:
                    if main_org[1] == 0:
                        main_org[0] = 1
                        main_org[1] = 1
                        break
                    if main_org[1] == 1:
                        main_org[0] = 0
                        main_org[1] = 0
                        break
            if 400 + 60 > mouse[1] > 400:
                if click[0] == 1:
                    if main_org[1] == 0:
                        main_org[0] = 2
                        main_org[1] = 1
                        break
                    if main_org[1] == 1:
                        main_org[0] = 0
                        main_org[1] = 0
                        break
        if 565 + 60 > mouse[0] > 565:
            if 320 + 60 > mouse[1] > 320:
                if click[0] == 1:
                    if main_org[3] == 0:
                        main_org[2] = 1
                        main_org[3] = 1
                        break
                    if main_org[3] == 1:
                        main_org[2] = 0
                        main_org[3] = 0
                        break
            if 400 + 60 > mouse[1] > 400:
                if click[0] == 1:
                    if main_org[3] == 0:
                        main_org[2] = 2
                        main_org[3] = 1
                        break
                    if main_org[3] == 1:
                        main_org[2] = 0
                        main_org[3] = 0
                        break
        if main_org[1] == 1 and main_org[3] == 1:
            if 345 + 60 > mouse[0] > 345 and 595 + 60 > mouse[1] > 535:
                if click[0] == 1:
                    if main_org[0] == 1:
                        player = 1
                    else:
                        player = 2
                    if main_org[2] == 1:
                        time = 1
                    else:
                        time = 2
                    game = Game(player)
                    score = game.run(player, time)
                    if score > highest_score:
                        highest_score = score
    return True


def draw(main_org):
    screen.blit(bg_main, (0, 0))
    screen.blit(font32.render("HIGHEST SCORE   {}".format(highest_score), True, (0, 0, 0)), (150, 620))
    if main_org[1] == 1:
        if main_org[0] == 1:
            pygame.draw.circle(screen, BUTTON_PRESSED, (245, 350), 30)
            pygame.draw.circle(screen, BUTTON_NON_PRESSED, (245, 430), 30)
        if main_org[0] == 2:
            pygame.draw.circle(screen, BUTTON_NON_PRESSED, (245, 350), 30)
            pygame.draw.circle(screen, BUTTON_PRESSED, (245, 430), 30)
    if main_org[1] == 0:
        pygame.draw.circle(screen, BUTTON_NON_PRESSED, (245, 350), 30)
        pygame.draw.circle(screen, BUTTON_NON_PRESSED, (245, 430), 30)
    if main_org[3] == 1:
        if main_org[2] == 1:
            pygame.draw.circle(screen, BUTTON_PRESSED, (595, 350), 30)
            pygame.draw.circle(screen, BUTTON_NON_PRESSED, (595, 430), 30)
        if main_org[2] == 2:
            pygame.draw.circle(screen, BUTTON_NON_PRESSED, (595, 350), 30)
            pygame.draw.circle(screen, BUTTON_PRESSED, (595, 430), 30)
    if main_org[3] == 0:
        pygame.draw.circle(screen, BUTTON_NON_PRESSED, (595, 350), 30)
        pygame.draw.circle(screen, BUTTON_NON_PRESSED, (595, 430), 30)
    pygame.display.update()
    pygame.display.flip()


def main():
    main_org = [0, 0, 0, 0]
    while True:
        if not button(main_org):
            break

        file = open("hs.txt", "w")
        file.write(str(highest_score))
        file.close()
        draw(main_org)


if __name__ == "__main__":
    try:
        main()

    except:
        traceback.print_exc()
        pygame.quit()
        input()
