
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 
# @Contributers : 
# @Date:   15-07-2023
# @Email:  
# @Last Modified by:   
# @Last Modified by:   
# @Last Modified by:   
# @Last Modified time: 

## Imports
import pygame
import sys
import random
import os
pygame.init()
###############################

## Path Directories 
img_dir = os.path.join(os.path.dirname(__file__), 'images')
sound_folder = os.path.join(os.path.dirname(__file__), 'music')
###############################

###############################

## Initialisation of components
win_width, win_height = 800, 700
win = pygame.display.set_mode((win_width, win_height))
POWERUP_TIME = 2000
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ARIAL = pygame.font.match_font('arial')



###############################


menu_bg = pygame.image.load(img_dir+'\main_menu.webp')
menu_bg = pygame.transform.scale(menu_bg, (win_width, win_height))

game_bg = pygame.image.load(img_dir+'\cartoon_space.webp')
game_bg = pygame.transform.scale(game_bg, (win_width, win_height))

rocket_img = pygame.image.load(img_dir+'\player.png')
rocket_img = pygame.transform.scale(rocket_img, (50, 50))  # Adjust the size as desired
rocket_x = win_width // 2 - rocket_img.get_width() // 2
rocket_y = win_height - rocket_img.get_height() - 20
rocket_speed = 1
rocket_mini_img = pygame.transform.scale(rocket_img, (25, 19))
rocket_mini_img.set_colorkey(BLACK)

bullet_img = pygame.image.load(img_dir+'\laserRed.png')
bullet_img = pygame.transform.scale(bullet_img, (10, 10))  # Adjust the size as desired
bullet_x = 0
bullet_y = rocket_y
bullet_speed = 1
bullet_state = "ready"

meteor_img = pygame.image.load(img_dir+'\enemyShip.png')
meteor_img = pygame.transform.scale(meteor_img, (50, 50))
meteor_x = random.randint(0, win_width - meteor_img.get_width())
meteor_y = -meteor_img.get_height()
meteor_speed = 0.2

score = 0
score_font = pygame.font.Font(None, 36)

game_over_font = pygame.font.Font(None, 72) 
lives = 5

###############################



def settingsMenu():
    pass
    

def display_menu():
    font = pygame.font.Font(ARIAL, 36)
    option_start = font.render("START GAME", True, (255, 255, 255))
    option_quit = font.render("Quit", True, (255, 255, 255))
    option_settings = font.render("Settings", True, (255, 255, 255))


    menu_song = pygame.mixer.music.load(os.path.join(sound_folder, "main_menu.OGG")) 
    pygame.mixer.music.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if option_start_rect.collidepoint(event.pos):
                    start_game()
                if option_quit_rect.collidepoint(event.pos):
                    sys.exit()
                if option_settings_rect.collidepoint(event.pos):
                    settingsMenu()

        win.blit(menu_bg, (0, 0))
        option_start_rect = win.blit(option_start, (win_width/2 - option_start.get_width()/2, win_height/2 - 150))
        option_quit_rect = win.blit(option_quit, (win_width/2 - option_start.get_width()/2, win_height/2 + 150))
        option_settings_rect = win.blit(option_settings, (win_width/2 - option_start.get_width()/2, win_height/2))

        pygame.display.update()

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect= img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def show_game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    win.blit(game_over_text, (win_width/2 - game_over_text.get_width()/2, win_height/2))

def start_game():
    global all_sprites, player, bullets, bullet_y, bullet_state, meteor_x, meteor_y, score 
    all_sprites = pygame.sprite.Group()
 
    player = Player()
    all_sprites.add(player)
    bullets = pygame.sprite.Group()
    
    while True:
        

        
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    player.shoot()
                
        # ## event for shooting the bullets
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         player.shoot()      ## we have to define the shoot()  function

        win.blit(game_bg, (0, 0))
      

        
        all_sprites.update()
        all_sprites.draw(win)

        win.blit(meteor_img, (meteor_x, meteor_y))
        meteor_y += meteor_speed
        
        if meteor_y > win_height:
            meteor_x = random.randint(0, win_width - meteor_img.get_width())
            meteor_y = -meteor_img.get_height()





        score_text = score_font.render("Score: " + str(score), True, (255, 255, 255))
        win.blit(score_text, (10, 10))
        draw_lives(win, win_width - 100, 5, player.lives, rocket_mini_img)
        pygame.display.update()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        ## scale the player img down
        self.image = pygame.transform.scale(rocket_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = win_width / 2
        self.rect.bottom = win_height - 10
        self.speedx = 0 
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()
    
    def shoot(self):
        ## to tell the bullet where to spawn
        now = pygame.time.get_ticks()
        keystate = pygame.key.get_pressed()     
        
        self.rect.x += self.speedx

        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
        
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
    

    def update(self):


        self.speedx = 0     ## makes the player static in the screen by default. 
        # then we have to check whether there is an event hanlding being done for the arrow keys being 
        ## pressed 

        ## will give back a list of the keys which happen to be pressed down at that moment
        keystate = pygame.key.get_pressed()     
        if keystate[pygame.K_LEFT]:
            self.speedx = -1
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 1

        #Fire weapons by holding spacebar
        if keystate[pygame.K_SPACE]:
            self.shoot()

        ## check for the borders at the left and right
        if self.rect.right > win_width:
            self.rect.right = win_width
        if self.rect.left < 0:
            self.rect.left = 0

        self.rect.x += self.speedx
            




class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        ## place the bullet according to the current position of the player
        self.rect.bottom = y 
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        """should spawn right in front of the player"""
        self.rect.y += self.speedy
        ## kill the sprite after it moves over the top border
        if self.rect.bottom < 0:
            self.kill()

        ## now we need a way to shoot
        ## lets bind it to "spacebar".
        ## adding an event for it in Game loop

display_menu()