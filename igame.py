#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/29 11:22:10

import sys
import os
import random
import cocos
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer, ScrollingManager, ScrollableLayer
import pyglet
import materials 
from materials.front_layer import show_message
"""i-game written by Crix 2019.06 - 2019.06 
I-GAME is a general struction of a python cocos 2d platform game
which has:
    i-game.py -- main program
        /data
            __init__.py
            Const.py -- stores the game CONSTs
            highscore.py -- handler the highscore
            highscore.tp -- the highscore data file
        /materials
            __init__.py -- defines the labels, sprites, imgs to be used globally
            /background
                the background tiled map (.tmx file & tile(.png) files)
            /main_scr
                __init__.py -- defines the labels, sprites, imgs to be used in main game screen
            /front_layer
                __init__.py -- defines the labels, sprites, imgs to be used in front layer
            /menu
                __init__.py -- defines the labels, sprites, imgs to be used in menu layer
        /tool
            file_test.py -- to initialise the high score record file
        /pic
            alpha.png -- the alphabet image file
            bg.png -- the backgroud image file (800 x 600)
            start.png -- the 'start' image file


A new start
Tower of fortune (indicate to the great game Tower of fortune in iOS)
"""
import pickle
from data import const, player, item, enemy, battle, skill

class Game(object):
    """main game class
    """
    def __init__(self, _player):
        self.player = _player
        self.enemy = None
        # The game has 3 status: STARTED, END, HIGHSCORE
        self.game_status = 'END'
        self.enter = 0
        self.msg = []
        self.zone = 0
        self.style = [0, 0, 0]
        self.loot_selected = 0

    def start_game(self):
        """start the game screen and initial the game
        """
        materials.main_scr.sprites['enemy_sprite'].visible = False
        for _ in range(3):
            materials.main_scr.sprites['player_dice_' + str(_)].visible = False
            materials.main_scr.sprites['enemy_dice_' + str(_)].visible = False
        self.player.sprite.visible = True
        self.zone = self.player.zone
        materials.front_layer.labels['zone_label'].element.text = const.ZONE_NAME[self.zone]
        director.replace(Scene(game_screen, front_layer))

    def show_game(self):

        director.replace(Scene(game_screen, front_layer))
        self.player.show_player()

    def show_loot(self):
        item.hide()
        materials.main_scr.sprites['icon_select'].visible = False
        for _ in range(8):
            materials.main_scr.sprites['loot' + str(_)].visible = False

        if self.player.loot:
            _loot = self.player.loot
            for _ in range(len(_loot)):
                materials.main_scr.sprites['loot' + str(_)].visible = True
                materials.main_scr.sprites['loot' + str(_)].image = materials.item_image[(59-_loot[_].type) * 5 + _loot[_].rare_type]
            materials.main_scr.sprites['icon_select'].visible = True
            materials.main_scr.sprites['icon_select'].x = 562 + (30 * self.loot_selected)

            item.show(self.player.loot[self.loot_selected], self.player.item_equiped[self.player.loot[self.loot_selected].equiped_pos])

    def show_info(self):
        """display the screen of player information
        """
        my_info.status = 'view'
        director.replace(Scene(my_info))
        self.refresh_info()

    def refresh_info(self):
        self.player.show_player()
        _value_string = ''
        _value_string += str(int(self.player.value['Atk'])) + ' '
        _value_string += str(int(self.player.value['Def'])) + ' '
        _value_string += str(int(self.player.value['Luc'])) + ' '
        _value_string += str(int(self.player.value['Vit'])) + ' '
        _value_string += str(int(self.player.value['CriDmg'])) + ' '
        _value_string += str(int(self.player.value['BlockValue'])) + '%' + ' '
        _value_string += str(int(self.player.value['ShortDistanceAtkDecreaseRate'])) + '%' + ' '
        _value_string += str(int(self.player.value['BrambleDmg'])) + ' '
        _value_string += str(int(self.player.value['HpBonusRate'])) + '%' + ' '
        _value_string += str(int(self.player.value['HpRegen'])) + ' '
        _value_string += str(int(self.player.value['HpAbsorb'])) + '%' + ' '
        _value_string += str(int(self.player.value['HpHit'])) + ' '
        _value_string += str(int(self.player.value['MagicFind'])) + ' '
        _value_string += str(int(self.player.value['GoldFind'])) + ' '
        _value_string += str(int(self.player.value['ExpBonus'])) + '%' + ' '
        _value_string += str(int(self.player.value['ExpWhenKill'])) + ' '
        _value_string += str(int(self.player.value['MaxDice'])) + ' '
        _value_string += str(int(self.player.value['MinDice'])) + ' '
        _value_string += str(int(self.player.value['DebuffRoundMinus'])) + ' '
        _value_string += str(int(self.player.value['EliteDamage'])) + '%' + ' '
        materials.info_layer.labels['player_value_label'].element.text = _value_string

    def screen_set_focus(self, x, y):
        game_screen.set_focus(self.player.sprite.x, self.player.sprite.y)
    
    def show_menu(self):
        self.game_status = 'END'
        director.replace(FlipY3DTransition(Scene(my_menu)))


if __name__ == '__main__':
    msg = []
    # change the working dir to the exe temp dir 
    # when you use pyinstaller to make a one-file exe package, you need doing this above
    if getattr(sys, 'frozen', False):
        os.chdir(sys._MEIPASS)
    my_game = Game(player.Player())
    game_screen = ScrollingManager()
    # the tile map 'map.tmx' which has a layer called 'start'
    # use the editor software called 'Tiled' to make a tile map 
    front_layer = materials.front_layer.Front_Layer()
    map_layer = cocos.tiles.load('./materials/background/map.tmx')['start']
    my_info = materials.info_layer.Info_Layer(my_game)
    my_menu = materials.menu.Menu_Screen(my_game)
    my_main = materials.main_scr.Main_Screen(my_game)
    # the order of the 'add' makes sense!
    game_screen.add(map_layer)
    game_screen.add(my_main)
    #game_screen.add(front_layer)
    main_scene = Scene(my_menu)
    #print ('game initialised')
    cocos.director.director.run(main_scene)
    #print('game end')
