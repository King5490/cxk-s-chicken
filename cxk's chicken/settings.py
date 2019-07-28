#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:King time:2019/7/18
class Settings():
    def __init__(self):
        self.screen_width=1200
        self.screen_height=612
        #self.bg_color=(200,200,200)
        self.ship_limit = 2

        self.bullet_width=12  #必须是整数，建议12
        self.bullet_height=self.bullet_width
        #self.bullet_color=60,60,60
        self.bullets_allowed=3

        self.alien_width=45  #必须是整数，建议45
        self.alien_height=int(0.9*self.alien_width)
        self.fleet_drop_speed=10

        self.speedup_scale=1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor=1.5
        self.bullet_speed_factor=2.5
        self.alien_speed_fator=0.5

        self.fleet_direction=1 #fleet_direction=1向右移动，-1为左

        self.alien_points=50
        self.score_scale=1.5

    def increase_speed(self):
        self.ship_speed_factor*=self.speedup_scale
        self.bullet_speed_factor*=self.speedup_scale
        self.alien_speed_fator*=self.speedup_scale
        self.alien_points=int(self.alien_points*self.score_scale)

