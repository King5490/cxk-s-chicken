#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:King time:2019/7/25
class GameStats():
    def __init__(self,ai_settings):
        self.ai_settings=ai_settings
        self.reset_stats()
        self.game_active=False
        self.ships_left = self.ai_settings.ship_limit
        self.high_score=0
        self.level=1

    def reset_stats(self):
        self.ships_left=self.ai_settings.ship_limit
        self.score=0
        self.level=1

