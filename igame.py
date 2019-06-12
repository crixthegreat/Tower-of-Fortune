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
from cocos.scenes import FlipY3DTransition
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
    
    def show_menu(self):
        """display the menu screen
        """
        materials.menu.show()
        

    def show_game(self):
        """show the game screen and initial the game
        """
        self.show_enemy(self.enemy)


    def show_enemy(self, enemy):
        if not enemy:
            return None
        show_message((const.ENEMY_ATK_NAME[enemy.type[0]] + const.ENEMY_CRIDMG_NAME[enemy.type[1]] + const.ENEMY_MAXHP_NAME[enemy.type[2]] + '的' + const.ENEMY_RANK_NAME[enemy.rank]))
        show_message(('LV ' + str(enemy.level)))
        show_message((const.ENEMY_DATA[enemy.no]['enemy_name'][enemy.zone] + '在' + const.ZONE_NAME[enemy.zone] + '出现了'))
        #print(enemy.value)
        #print('它拥有技能：')
        #for _ in enemy.skill:
        #    print(const.SKILL_DATA[_.skill_no]['name'])



class Menu_Screen(Layer):
    """The menu layer class, where the player starts the game 
    and changes the game level
    """
    is_event_handler = True

    def __init__(self, game):

        super(Menu_Screen, self).__init__()
        
        self.game = game
        self.keys_pressed = set()


        self.image = materials.images['bg_img']
        for _, _label in materials.labels.items():
            self.add(_label)
        for _, _label in materials.menu.labels.items():
            self.add(_label)
        for _, _sprite in materials.sprites.items():
            self.add(_sprite)
        for _, _sprite in materials.menu.sprites.items():
            self.add(_sprite)
        #materials.menu.sprites['t2_sprite'].scale = 1.5

        self.game.show_menu()


    def on_key_press(self, key, modifiers):
        """key press handler for menu class
        """
        self.keys_pressed.add(key)
        key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]
        _enter_list = ['continue', 'enter', 'credit']
        _enter = 0
        if 'ENTER' in key_names:
            #Start the game
            self.keys_pressed.clear()
            if self.game.enter == 2:
                director.replace(Scene(credit_layer))
                return 1
            if self.game.enter == 1:
                self.game.player = player.gen_player(1)
            elif self.game.enter == 0:
                self.game.player = player.load()
            else:
                print('game enter error!')
                sys.exit()
            self.game.show_game()
            director.replace(Scene(game_screen, front_layer))
        # use the LEFT or RIGHT to change the game level
        elif 'UP' in key_names:
            if self.game.enter != 0:
                self.game.enter -= 1
                materials.menu.sprites['start_sprite'].y += 55
        elif 'DOWN' in key_names:
            if self.game.enter != 2:
                self.game.enter += 1
                materials.menu.sprites['start_sprite'].y -= 55
        elif 'F12' in key_names:
            pass
            #materials.menu.show_highscore()



    def on_key_release(self, key, modifiers):
        # release the key_pressed set
        # be careful that the layer changing when key is be pressed (but not released)
        if self.keys_pressed and key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def draw(self):
        self.image.blit(0, 0)
    
class Front_Layer(Layer):

    def __init__(self):

        super(Front_Layer, self).__init__()
        for _, _label in materials.front_layer.labels.items():
            self.add(_label)
    

class Main_Screen(ScrollableLayer):
    """The main game screen
    do a lot of key events
    """
    is_event_handler = True

    def __init__(self, game):

        super(Main_Screen, self).__init__()
        self.game = game
        self.keys_pressed = set()
        self.player = player.Player(materials.main_scr.sprites['player_sprite'])

        for _, _sprite in materials.main_scr.sprites.items():
            self.add(_sprite)
        # use the time interval event to calculate the time used
        self.schedule_interval(self.refresh_time, 0.04)


    def refresh_time(self, dt):
        # the 'dt' means the time passed after the last event occured
        if self.game.game_status == 'STARTED':
            #print(self.tx, self.ty, materials.alpha_sprite(5).x, materials.alpha_sprite(5).y)
            game_screen.set_focus(self.player.sprite.x, self.player.sprite.y) 

    def on_key_press(self, key, modifiers):
        # use a set(keys_pressed) to store all the keys pressed
        # the number '983547510784' means 'SHIFT + SPACE' key
        _str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if key != 983547510784:
            self.keys_pressed.add(key)
        key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]
        # press the SPACE key to return to the title anywhere any time
        if 'SPACE' in key_names:
            # return to the menu(title) screen
            self.keys_pressed.clear()
            self.game.show_menu()
            director.replace(FlipY3DTransition(Scene(my_menu)))
        elif self.game.game_status == 'STARTED':
            if 'RIGHT' in key_names:
                _r = battle.player_attack(self.game.player, self.game.enemy, 0)
                if not _r:
                    self.game.game_status = 'END'
                
        # play the game again
        elif self.game.game_status == 'END':
            if 'DOWN' in key_names:
                self.game.enemy = enemy.gen_enemy(None, None, self.game.zone, random.randrange(self.game.zone * 10 + 1, (self.game.zone + 1) * 10))
                self.game.game_status = 'STARTED'
                self.game.show_game()
                

    def on_key_release(self, key, modifiers):
        
        #print('main key:', self.keys_pressed)
        if self.keys_pressed and key in self.keys_pressed:
            self.keys_pressed.remove(key)

    #def draw(self):
     #   self.image.blit(0, 0)


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
    front_layer = Front_Layer()
    map_layer = cocos.tiles.load('./materials/background/map.tmx')['start']
    my_main = Main_Screen(my_game)
    my_menu = Menu_Screen(my_game)

    # the order of the 'add' makes sense!
    game_screen.add(map_layer)
    game_screen.add(my_main)
    #game_screen.add(front_layer)
    
    main_scene = Scene(my_menu)
    #print ('game initialised')
    cocos.director.director.run(main_scene)

    #print('game end')

