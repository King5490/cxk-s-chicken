#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:King time:2019/7/24
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,ai_settings,screen,alien_image):
        super(Alien, self).__init__()
        self.screen=screen
        self.ai_settings=ai_settings
        self.image=alien_image
        self.rect=self.image.get_rect()
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        self.x=float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image,self.rect)

    def update(self):
        self.x+=(self.ai_settings.alien_speed_fator*self.ai_settings.fleet_direction)
        self.rect.x=self.x

    def check_edges(self):
        screen_rect=self.screen.get_rect()
        if self.rect.right>=screen_rect.right:
            return True
        elif self.rect.left<=0:
            return True

