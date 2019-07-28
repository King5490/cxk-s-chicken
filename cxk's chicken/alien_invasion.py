#!/usr/bin/env python3.7.4
# -*-coding:utf-8-*-
# author:King time:2019/7/18
import sys
import pygame
import game_functions as gf
from ship import Ship
from time import sleep
from alien import Alien
from button import Button
from settings import Settings
from pygame.sprite import Group
from game_stats import GameStats
from scoreboard import Scoreboard

#原版无用代码均已注释

def run_game():
    pygame.font.init()
    pygame.init()
    pygame.mixer.init()
    ai_settings=Settings()
    screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption('Chicken Ivasion')

    play_button=Button(ai_settings,screen,'play')

    background = pygame.image.load('pictures/backimage.png').convert()
    background= pygame.transform.scale(background, (1200,612))
    screen.blit(background, (0, 0))

    bullets_image=pygame.image.load('pictures/basketball.png').convert_alpha()#优先外部读取素材，避免重复读取占用系统资源造成卡顿
    bullets_image=pygame.transform.smoothscale(bullets_image, (ai_settings.bullet_width,ai_settings.bullet_height))
    bullets=Group()

    aliens_image=pygame.image.load('pictures/ji.png').convert_alpha()
    aliens_image=pygame.transform.smoothscale(aliens_image, (ai_settings.alien_width,ai_settings.alien_height))
    aliens=Group()

    shot_sound = pygame.mixer.Sound("sounds/ji.wav")
    hit_sound=pygame.mixer.Sound("sounds/ntm.wav")
    crash_sound=pygame.mixer.Sound("sounds/ngm.wav")
    game_over_sound=pygame.mixer.Sound("sounds/1.wav")
    BGM= pygame.mixer.music.load("sounds/xbd.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(5)


    my_font = pygame.font.Font("font/GIGI.ttf",60)
    game_over_text1 = my_font.render('Game over!', True, (255, 10, 10))
    game_over_text2 = my_font.render('The chicken got your brain!', True, (255, 10, 10))

    ship = Ship(ai_settings, screen)
    gf.create_fleet(ai_settings,screen,ship,aliens,aliens_image)

    stats=GameStats(ai_settings)

    sb=Scoreboard(ai_settings,screen,stats)

    while True:
        gf.update_screen(ai_settings, screen, stats,sb, ship, aliens, bullets, play_button)
        gf.check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets,bullets_image,aliens_image,shot_sound,sb)
        if stats.game_active:
            ship.update()
            bullets.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,aliens_image,bullets,hit_sound)
            gf.update_aliens(ai_settings,stats,screen,ship,aliens,aliens_image,bullets,crash_sound,game_over_text1,game_over_text2,game_over_sound,sb)

            screen.blit(background, (0, 0))

run_game()