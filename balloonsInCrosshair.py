import pygame
import random
import time

def display_score():
    score_surf=game_font.render("Score: "+str(score),True,FONT_COLOR)
    score_rect=score_surf.get_rect(topleft=(10,10))
    screen.blit(score_surf,score_rect)

def final_score():
    final_score_surf=game_font.render("Your scores: "+str(score),True,FONT_COLOR)
    final_score_rect=final_score_surf.get_rect(center=(WIDTH/2,HEIGHT-220))
    screen.blit(final_score_surf,final_score_rect)

def display_time():
    time_left_surf=game_font.render("Time left: " + str(time_left), False, FONT_COLOR)
    time_left_rect=time_left_surf.get_rect(topleft=(10,50))
    screen.blit(time_left_surf,time_left_rect)

def display_level():
    level_surf=game_font.render("Level: "+str(level),True,FONT_COLOR)
    level_rect=level_surf.get_rect(topleft=(10,90))
    screen.blit(level_surf,level_rect)

def display_reloading():
    screen.fill(WHITE)
    reloading_surf=game_font.render("RELOADING", True, FONT_COLOR)
    reloading_rect=reloading_surf.get_rect(center=(WIDTH/2,HEIGHT/2))
    screen.blit(reloading_surf,reloading_rect)
    pygame.display.flip()
    time.sleep(1.2)

WIDTH = 1280
HEIGHT = 620
SPEED = 3
FONT_COLOR=(27, 131, 142)
GAME_TIME=15000
WHITE=(255,255,255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloons in crosshair")
clock = pygame.time.Clock()

bg_surf = pygame.image.load("img/sky.png").convert_alpha()
bg_surf = pygame.transform.rotozoom(bg_surf,0,1.25)
bg_rect = bg_surf.get_rect(bottomleft=(0,HEIGHT))

balloon_surf = pygame.image.load('img/balloon.png').convert_alpha()
balloons_rect = []
balloons_timer = pygame.USEREVENT+1
pygame.time.set_timer(balloons_timer,1000)

crosshair_surf = pygame.image.load('img/crosshair.png').convert_alpha()
crosshair_surf = pygame.transform.rotozoom(crosshair_surf,0,0.7)
crosshair_rect = crosshair_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))

#ammo
ammo=4
ammo0=pygame.image.load("img/ammo0.png").convert_alpha()
ammo1=pygame.image.load("img/ammo1.png").convert_alpha()
ammo2=pygame.image.load("img/ammo2.png").convert_alpha()
ammo3=pygame.image.load("img/ammo3.png").convert_alpha()
ammo4=pygame.image.load("img/ammo4.png").convert_alpha()
ammo_surf=[ammo0,ammo1,ammo2,ammo3,ammo4]
ammo_rect=ammo_surf[ammo].get_rect(bottomleft=(5,HEIGHT-5))

#hangok
shot=pygame.mixer.Sound("sound/shot.mp3")
reload=pygame.mixer.Sound("sound/reload.mp3")

#nyitó és záró képernyő feliratai
game_font=pygame.font.SysFont("arial", 30, bold=True)
title_surf=game_font.render("Balloons in crosshair", True, FONT_COLOR)
title_rect=title_surf.get_rect(center=(WIDTH/2, 200))
run_surf=game_font.render("Press space to the next run!",True,FONT_COLOR)
run_rect=run_surf.get_rect(center=(WIDTH/2, HEIGHT-150))

running = True
score=0
level=0
tikk=5
start_time=pygame.time.get_ticks()
game_active=False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION and ammo>0:
            crosshair_rect = crosshair_surf.get_rect(center=event.pos)
        if event.type==pygame.MOUSEBUTTONDOWN and game_active:
            screen.fill(WHITE)
            pygame.display.flip()
            time.sleep(0.1)
            ammo-=1
            dogSmile=True
            shot.play()
            if ammo==0:
                reload.play()
                display_reloading()
                ammo=4

        #Lufik létrehozása megadott időközönként    
        if event.type == balloons_timer:
            balloons_rect.append(balloon_surf.get_rect(center=(random.randint(50,WIDTH-50),HEIGHT+50)))

    screen.blit(bg_surf,bg_rect)

    if game_active:      
        for index, balloon_rect in enumerate(balloons_rect):
            #lufik emelkedése
            balloons_rect[index].top-=SPEED
            #lufik oldalirányú mozgása
            mov_y=random.randint(0,3)
            if mov_y==0:
                balloons_rect[index].left-=2
            else:
                balloons_rect[index].left+=2
            #lufik törlése
            if balloons_rect[index].bottom<=-10:
                del balloons_rect[index]
            if balloon_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed(num_buttons=3)[0]:
                del balloons_rect[index]
                score+=1
            
            screen.blit(balloon_surf, balloon_rect)
        screen.blit(crosshair_surf, crosshair_rect)
        screen.blit(ammo_surf[ammo],ammo_rect)

        display_score()

        #játékidő meghatározása
        time_left=int((start_time+GAME_TIME-pygame.time.get_ticks()))/1000
        if time_left<0:
            game_active=False
        display_time()
        display_level()

    #nyitó és záróképernyő
    else:
        screen.blit(title_surf, title_rect)
        screen.blit(balloon_surf,balloon_surf.get_rect(center=(WIDTH/2,HEIGHT/2)))
        screen.blit(crosshair_surf,crosshair_surf.get_rect(center=(WIDTH/2,HEIGHT/2)))
        screen.blit(run_surf,run_rect)

        #pontszám
        if score>0:
            final_score()

        #játék inditás
        keys=pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and score==0:
            start_time=pygame.time.get_ticks()
            game_active=True

        if keys[pygame.K_SPACE]:
            balloons_rect=[]
            start_time=pygame.time.get_ticks()
            game_active=True
            tikk+=15
            level+=1
    
    pygame.display.update()
    clock.tick(tikk)

pygame.quit()    
