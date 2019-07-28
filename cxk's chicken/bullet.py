#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:King time:2019/7/21
import  pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self,ai_settings,screen,ship,bullets_image):
        super(Bullet,self).__init__()
        self.screen=screen
        self.image = bullets_image
        self.rect=self.image.get_rect() #使用素材的边界值
        #self.rect=pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
        self.rect.centerx=ship.rect.centerx-19#调整素材(篮球)的中心与cxk手中球中心一致
        self.rect.top=ship.rect.top
        self.y=float(self.rect.y)
        #self.color=ai_settings.bullet_color
        self.speed_factor=ai_settings.bullet_speed_factor


    def update(self):
        self.y-=self.speed_factor
        self.rect.y=self.y

    def blitme(self):
            self.screen.blit(self.image, self.rect)

    #def draw_bullet(self):
        #pygame.draw.rect(self.screen,self.color,self.rect)

