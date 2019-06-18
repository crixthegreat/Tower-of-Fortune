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
images = {}

player_image = pyglet.image.load(os.path.abspath(const.PLAYER_IMG_FILE)) 
enemy_image = pyglet.image.load(os.path.abspath(const.ENEMY_IMG_FILE)) 
icon_select_image = pyglet.image.load(os.path.abspath(const.ICON_SELECT_IMG_FILE)) 
item_box_image = pyglet.image.load(os.path.abspath(const.ITEM_BOX_IMG_FILE)) 

images['rip'] = pyglet.image.load(os.path.abspath(const.RIP_IMG_FILE)) 
images['enemy_image'] = enemy_image
"""
time_label & best_time_label : as the name says
"""
labels = {}
labels['item_name'] = cocos.text.Label('',font_size=12,
        font_name = 'Gadugi',
        bold=True,
        color=const.HIGHLIGHT_COLOR, 
        x=430, y=360)
labels['item_type'] = cocos.text.Label('',font_size=9,
        font_name = 'Gadugi',
        bold=False,
        color=const.DEFAULT_COLOR, 
        x=430, y=340, width=200, multiline=True)
labels['item_main_affix'] = cocos.text.Label('',font_size=12,
        font_name = 'Gadugi',
        bold=True,
        color=const.HIGHLIGHT_COLOR, 
        x=430, y=305)
labels['item_affix'] = cocos.text.Label('',font_size=9,
        font_name = 'Gadugi',
        bold=False,
        color=const.DEFAULT_COLOR, 
        x=430, y=285, width=200, multiline=True)
labels['player_item_name'] = cocos.text.Label('',font_size=12,
        font_name = 'Gadugi',
        bold=True,
        color=const.HIGHLIGHT_COLOR, 
        x=245, y=340)
labels['player_item_type'] = cocos.text.Label('',font_size=9,
        font_name = 'Gadugi',
        bold=False,
        color=const.DEFAULT_COLOR, 
        x=245, y=320, width=200, multiline=True)
labels['player_item_main_affix'] = cocos.text.Label('',font_size=12,
        font_name = 'Gadugi',
        bold=True,
        color=const.HIGHLIGHT_COLOR, 
        x=245, y=285)
labels['player_item_affix'] = cocos.text.Label('',font_size=9,
        font_name = 'Gadugi',
        bold=False,
        color=const.DEFAULT_COLOR, 
        x=245, y=265, width=200, multiline=True)

sprites = {}
sprites['player_sprite'] = cocos.sprite.Sprite(player_image, position=(240, 300))
sprites['enemy_sprite'] = cocos.sprite.Sprite(enemy_image, position=(600, 300))
for _ in range(8):
    sprites['loot' + str(_)] = cocos.sprite.Sprite(player_image, position=(590 + _ * 30, 210))
sprites['icon_select'] = cocos.sprite.Sprite(icon_select_image, position=(562, 185))
sprites['item_box'] = cocos.sprite.Sprite(item_box_image, position=(360, 285))

for _ in range(3):
    sprites['player_dice_' + str(_)] = cocos.sprite.Sprite(materials.dice_image[0], position=(370,250 + 66 * _ ))
    sprites['enemy_dice_' + str(_)] = cocos.sprite.Sprite(materials.dice_image[1], position=(450, 250 + 66 * _))

bg_music = materials.Audio(const.BG_MUSIC_FILE)
highscore_music = materials.Audio(const.HIGHSCORE_MUSIC_FILE)

def show(level=None):
    """to display main game screen
    """
    materials.menu.bg_music.stop()
    materials.main_scr.highscore_music.stop()
    bg_music.play(-1)
    return None
    
