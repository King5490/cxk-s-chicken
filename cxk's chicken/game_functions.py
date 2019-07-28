#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:King time:2019/7/20
import sys
import pygame
from time import sleep
from alien import Alien
from bullet import Bullet

def update_aliens(ai_settings, stats, screen, ship, aliens, aliens_image, bullets, crash_sound, game_over_text1,
                  game_over_text2, game_over_sound,sb):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, aliens_image, bullets, crash_sound, game_over_text1,
                 game_over_text2, game_over_sound,sb)
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, aliens_image, bullets, crash_sound, game_over_text1,
                        game_over_text2, game_over_sound,sb)

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    #screen.fill(ai_settings.bg_color)
    sb.show_score()
    for bullet in bullets.sprites():
        bullet.blitme()
    ship.blitme()
    aliens.draw(screen)
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,aliens_image,bullets,hit_sound):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_collisions(ai_settings,screen,stats,sb,ship,aliens,aliens_image,bullets,hit_sound)

def check_keydown_events(event,ai_settings,screen,ship,bullets,bullets_image,shot_sound):
    if event.key == pygame.K_d:
            ship.moving_right = True
    if event.key == pygame.K_a:
            ship.moving_left = True
    if event.key==pygame.K_KP0:
        fire_bullets(ai_settings,screen,ship,bullets,bullets_image,shot_sound)
    if event.key==pygame.K_ESCAPE:
        sys.exit()

def check_keyup_events(event,ship):
    if event.key == pygame.K_d:
        ship.moving_right = False
    if event.key == pygame.K_a:
        ship.moving_left = False

def check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets,bullets_image,aliens_image,shot_sound,sb):
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets,bullets_image,shot_sound)
        elif event.type==pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats,sb, play_button, ship, aliens, bullets, mouse_x, mouse_y,aliens_image)

def check_collisions(ai_settings,screen,stats,sb,ship,aliens,aliens_image,bullets,hit_sound):
    collisions=pygame.sprite.groupcollide(bullets, aliens, True,True)

    if collisions:
        for aliens in collisions.values():
            stats.score+=ai_settings.alien_points*len(aliens)
            hit_sound.play()
            sb.prep_score()
        check_high_score(stats,sb)
    if len(aliens)==0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level+=1
        sb.prep_level()
        create_fleet(ai_settings,screen,ship,aliens,aliens_image)

def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,aliens_image,bullets,crash_sound, game_over_text1,game_over_text2, game_over_sound,sb):
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, aliens_image, bullets, crash_sound, game_over_text1,game_over_text2, game_over_sound,sb)
            break

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y,aliens_image):
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y )
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        stats.reset_stats()
        stats.game_active=True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        pygame.mouse.set_visible(False)
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens, aliens_image)
        ship.center_ship()

def check_high_score(stats,sb):
    if stats.score>stats.high_score:
        stats.high_score=stats.score
        sb.prep_high_score()

def create_fleet(ai_settings,screen,ship,aliens,aliens_image):
    alien = Alien(ai_settings, screen, aliens_image)
    number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows=get_number_aliens_rows(ai_settings,ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number,aliens_image)

def create_alien(ai_settings,screen,aliens,aliens_number,row_number,aliens_image):
    alien = Alien(ai_settings, screen, aliens_image)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * aliens_number
    alien.rect.x = alien.x
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)

def ship_hit(ai_settings,stats,screen,ship,aliens,aliens_image,bullets,crash_sound,game_over_text1,game_over_text2,game_over_sound,sb):
    if stats.ships_left>0:
        crash_sound.play()
        stats.ships_left-=1

        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings,screen,ship,aliens,aliens_image)
        ship.center_ship()

        sleep(0.5)

    else:
        stats.game_active=False
        pygame.mixer.music.stop()
        screen.blit(game_over_text1, (455, 186))
        screen.blit(game_over_text2, (300, 306))
        pygame.display.flip()
        game_over_sound.play()
        pygame.mouse.set_visible(True)
        sleep(4)

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def fire_bullets(ai_settings,screen,ship,bullets,bullets_image,shot_sound):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship, bullets_image)
        bullets.add(new_bullet)
        shot_sound.play()

def get_number_aliens_x(ai_settings,alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_aliens_rows(ai_settings,ship_height,alien_height):
    available_space_y=ai_settings.screen_height-3*alien_height-ship_height
    number_rows=int(available_space_y/(2*alien_height))
    return number_rows