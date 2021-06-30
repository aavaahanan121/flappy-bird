import pygame
import random

gravity = 0.7
jump_force = 10
pygame.init()

animation = [pygame.image.load("big project/assets/pictures/player/yellowbird-midflap.png"), pygame.image.load("big project/assets/pictures/player/yellowbird-upflap.png"), pygame.image.load("big project/assets/pictures/player/yellowbird-downflap.png")]

class bird(pygame.sprite.Sprite):
    def __init__(self, pipes : pygame.sprite.Group, game_over, win_h):
        super().__init__()
        self.image = pygame.image.load("big project/assets/pictures/player/yellowbird-midflap.png")
        self.rect = pygame.rect.Rect(30, 0, self.image.get_rect().width, self.image.get_rect().height)
        self.x = 0
        self.y = 0
        self.x_vel = 0
        self.y_vel = 0
        self.maxspeed = 7
        self.pipes = pipes
        self.game_over = game_over
        self.win_h = win_h
        self.sound = pygame.mixer.Sound("big project/assets/sound/wing.ogg")
        self.diesound = pygame.mixer.Sound("big project/assets/sound/die.ogg")
        self.hurtsound = pygame.mixer.Sound("big project/assets/sound/hit.ogg")
        self.h = 3
        self.start_time = pygame.time.get_ticks()
        self.i = 0
    
    def update(self):
        self.i += 0.3
        if int(self.i) > len(animation):
            self.i = 0
        self.image = animation[int(self.i) - 1]
        if self.rect.y < 0:
            self.y_vel = 0
        if self.y_vel <= self.maxspeed:
            self.y_vel += 1
        
        self.y += self.y_vel
        self.rect.y = self.y

        if pygame.sprite.spritecollideany(self, self.pipes) != None:
            if self.start_time + 2000 <= pygame.time.get_ticks():
                self.h -= 1
                self.start_time = pygame.time.get_ticks()
                self.hurtsound.play()
            
            if self.h <= 0:
                self.die()
        if self.rect.y > self.win_h:
            self.die()
        

    def jump(self):
        self.y_vel = -jump_force
        self.sound.play()
        
    
    def die(self):
        self.diesound.play()
        pygame.event.post(pygame.event.Event(self.game_over))

speed = 2
offset = 15

class pipe(pygame.sprite.Sprite):
    def __init__(self, starting_pos, window, rot):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.image.load("big project/assets/pictures/pipe/pipe-green.png"), rot)
        self.rect = pygame.rect.Rect(starting_pos, ( self.image.get_rect().w, self.image.get_rect().h))
        self.x, self.y = starting_pos[0], starting_pos[1]
        self.window = window
        self.rot = rot
        self.finished = False
    
    def update(self):
        self.x -= speed
        if self.rot == 0:
            self.rect.x = self.x - self.image.get_width()/2
            self.rect.y = self.y - self.image.get_height()/2 - 95
        else:
            self.rect.x = self.x - self.image.get_width()/2
            self.rect.y = self.y - 63
        
        if self.rect.x + self.rect.width + offset <= 0:
            self.kill()
            

hole = 150

class obstacle:
    def __init__(self, window : pygame.surface.Surface):
        self.randomint = random.randint(0 - int(window.get_height()/5), int(window.get_height()/5))
        self.pipe1 = pipe((window.get_rect().width + offset, 0 - hole/2 + self.randomint), window, 180)
        self.pipe2 = pipe((window.get_rect().width + offset, window.get_height() + hole/2 + self.randomint), window, 0)
    

