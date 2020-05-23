#Difficulty is 1, 2, 3, 4, or 5
DIFFICULTY = 3

import pygame
from pygame.locals import *
import sys, os, traceback, random
if sys.platform in ["win32","win64"]: os.environ["SDL_VIDEO_CENTERED"]="1"
pygame.display.init()
pygame.font.init()
pygame.mixer.init(buffer=128)

xs = [50,50+1+50,50+1+50+1+50]
screen_size = [50*4+3,300]
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
pygame.display.set_caption("bblock - Ian Mallett - v.1.0.0 - 2014")
surface = pygame.display.set_mode(screen_size)

clock = pygame.time.Clock()
font12 = pygame.font.SysFont("Times New Roman",12)
font18 = pygame.font.SysFont("Times New Roman",18)
font24 = pygame.font.SysFont("Times New Roman",24)

sounds = {
    "click" : pygame.mixer.Sound("data/click.ogg"),
    "begin" : pygame.mixer.Sound("data/begin.ogg"),
    "end"   : pygame.mixer.Sound("data/end.ogg")
}

file = open("data/hs.txt","r")
high_score = int(file.read().strip())
file.close()

class Game(object):
    class Block(object):
        def __init__(self,column):
            self.column = column
            self.x = self.column*51
            self.bottom = screen_size[1]
        @staticmethod
        def update(game):
            game.block_counter += 1
            if game.block_counter == game.H/game.rate:
                game.block_counter = 0
                
                added = []
                for i in range(4):
                    added.append(random.choice([0,1,2,3]))
                    if random.random() < 0.75: break
                    
                done = []
                for a in added:
                    if a in done: continue
                    game.blocks.append(Game.Block(a))
                    done.append(a)
        def move(self,game):
            self.bottom -= game.rate
        def draw(self,game):
            rect = (self.x,screen_size[1]-self.bottom-game.H,game.W,game.H)
            pygame.draw.rect(surface,(  0,0,  0),rect,0)
            pygame.draw.rect(surface,(255,0,255),rect,1)
    def __init__(self):
        self.score = 0
        self.blocks = []
        self.block_counter = 0

        self.W = 50
        if   DIFFICULTY == 1:
            self.H = 100
            self.rate = 2
        elif DIFFICULTY == 2:
            self.H = 100
            self.rate = 3
        elif DIFFICULTY == 3:
            self.H = 100
            self.rate = 4
        elif DIFFICULTY == 4:
            self.H = 90
            self.rate = 4.5
        elif DIFFICULTY == 5:
            self.H = 80
            self.rate = 6
    def get_input(self):
        global high_score
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if   event.type == QUIT: return False
            elif event.type == KEYDOWN:
                if   event.key == K_ESCAPE: return False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mpos = [mouse_position[0],screen_size[1]-mouse_position[1]]
                    for block in self.blocks:
                        if mpos[0] >= block.x and mpos[0] <= block.x+51:
                            if mpos[1] >= block.bottom and mpos[1] <= block.bottom+self.H:
                                sounds["click"].play()
                                self.blocks.remove(block)
                                self.score += 1
                                if self.score > high_score:
                                    high_score = self.score
                                break
        return True
    def update(self):
        Game.Block.update(self)
        for block in self.blocks:
            block.move(self)

            if block.bottom <= self.rate:
                return False
        return True
    def draw(self):
        surface.fill((255,255,255))
        
        for x in xs:
            pygame.draw.line(surface,(255,0,0),(x,0),(x,screen_size[1]-25),1)

        for block in self.blocks:
            block.draw(self)
            
        surface.blit(font12.render("Current: "+str(self.score),True,(0,0,255)),(5,screen_size[1]-20))
        surface.blit(font12.render("Best: "+str(high_score),True,(0,0,255)),(150,screen_size[1]-20))
        
        pygame.display.flip()
    def run(self):
        while True:
            if not self.get_input(): return -1
            if not self.update(): return self.score
            self.draw()
            clock.tick(60)
def get_input():
    keys_pressed = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_position = pygame.mouse.get_pos()
    mouse_rel = pygame.mouse.get_rel()
    for event in pygame.event.get():
        if   event.type == QUIT: return False
        elif event.type == KEYDOWN:
            if   event.key == K_ESCAPE: return False

            sounds["begin"].play()
            game = Game()
            score = game.run()
            if score == -1:
                return False
            sounds["end"].play()
            file = open("data/hs.txt","w")
            file.write(str(high_score))
            file.close()
    return True
blink = -30
def draw():
    global blink
    surface.fill((255,255,255))
    surface.blit(font24.render("bblock",True,(255,0,0)),(65,80))
    surface.blit(font18.render("Ian Mallett",True,(255,0,0)),(60,105))
    if blink < 0:
        surface.blit(font18.render("PRESS ANY KEY",True,(255,0,0)),(30,150))
    blink += 1
    if blink == 30:
        blink = -30
    surface.blit(font18.render("HIGH SCORE "+str(high_score),True,(255,0,0)),(35,260))
    pygame.display.flip()
def main():
    pygame.event.set_grab(True)
    while True:
        if not get_input(): break
        draw()
        clock.tick(60)
    pygame.event.set_grab(False)
    pygame.quit()
if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
        input()
