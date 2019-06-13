#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/28 17:03:36
"""THE MAIN SCREEN DEFINITION FILE
"""
import os
from data import const
import pyglet
import cocos
import materials
import random

#player_image = []
#player_image = pyglet.image.ImageGrid(pyglet.image.load('./pic/player.png'), 1, 3)
#images = {'player_img':player_image}

player_image =pyglet.image.load(os.path.abspath(const.PLAYER_IMG_FILE)) 
enemy_image =pyglet.image.load(os.path.abspath(const.ENEMY_IMG_FILE)) 
"""
time_label & best_time_label : as the name says
"""

sprites = {}
sprites['player_sprite'] = cocos.sprite.Sprite(player_image, position=(200, 300))
sprites['enemy_sprite'] = cocos.sprite.Sprite(enemy_image, position=(600, 400))
for _ in range(3):
    sprites['player_dice_' + str(_)] = cocos.sprite.Sprite(materials.dice_image[0], position=(370,250 + 66 * _ ))
    sprites['enemy_dice_' + str(_)] = cocos.sprite.Sprite(materials.dice_image[1], position=(450, 250 + 66 * _))

bg_music = materials.Audio(const.BG_MUSIC_FILE)
highscore_music = materials.Audio(const.HIGHSCORE_MUSIC_FILE)

def show(level=None):
    """to display main game screen
    """
    if level == 'Normal':
        pass
    elif level == 'Hard':
        pass
    else:
        pass
        #sys.exit()
    materials.menu.bg_music.stop()
    materials.main_scr.highscore_music.stop()
    bg_music.play(-1)
    return None
    
