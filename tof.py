#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/29 11:22:10

import sys
import os
import zipfile
import random
import json
import copy
import cocos
from cocos.director import director
from cocos.scene import Scene
from cocos.scenes import FlipY3DTransition
from cocos.layer import Layer, ScrollingManager, ScrollableLayer
import pyglet
import materials 
from materials.front_layer import show_message
from data import const, player, skill
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


------------ A new start ---------------------------------
Tower of fortune (pays homage to the following great games:
- Tower of fortune (iOS)
- Diablo
- The Gambling God (FC)
)
----------------------------------------------------------
"""
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
        self.corpse = None

    @property
    def max_stage(self):
        return (self.player.level - 1) // 10

    @property
    def game_status(self):
        return self._game_status

    @game_status.setter
    def game_status(self, status):
        self._game_status = status
        materials.main_scr.sprites['control'].anchor = 0, 0
        if status == 'END':
            materials.main_scr.sprites['control'].position = 400, 50
            materials.main_scr.sprites['control'].image = materials.main_scr.main_control_image
            materials.main_scr.sprites['control'].scale = 0.4
        elif status == 'STARTED':
            materials.main_scr.sprites['control'].position = 400, 65
            materials.main_scr.sprites['control'].image = materials.main_scr.battle_control_image
            materials.main_scr.sprites['control'].scale = 0.55
        elif status == 'LOOT':
            materials.main_scr.sprites['control'].position = 400, 50
            materials.main_scr.sprites['control'].image = materials.main_scr.loot_control_image
            materials.main_scr.sprites['control'].scale = 0.4
        elif status == 'CORPSE':
            materials.main_scr.sprites['control'].position = 400, 65
            materials.main_scr.sprites['control'].image = materials.main_scr.corpse_control_image
            materials.main_scr.sprites['control'].scale = 0.55
        elif status == 'CAMP':
            materials.main_scr.sprites['control'].position = 400, 65
            materials.main_scr.sprites['control'].image = materials.main_scr.camp_control_image
            materials.main_scr.sprites['control'].scale = 0.55


    def start_game(self):
        """start the game screen and initial the game
        """
        materials.main_scr.sprites['enemy_sprite'].visible = False
        for _ in range(3):
            materials.main_scr.sprites['player_dice_' + str(_)].visible = False
            materials.main_scr.sprites['enemy_dice_' + str(_)].visible = False
        self.player.sprite.visible = True
        self.player.sprite.image = materials.main_scr.player_image
        self.set_stage(self.player.zone)
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
        # show the value of the player
        my_info.show_player_value()

        # show the equiped items of the player
        my_info.show_player_item()
        # show the items in the player's item box
        my_info.show_item_box()

    def screen_set_focus(self, x, y):
        game_screen.set_focus(self.player.sprite.x, self.player.sprite.y)
    
    def show_menu(self):
        self.game_status = 'END'
        director.replace(FlipY3DTransition(Scene(my_menu)))

    def show_save_load(self):
        director.replace(FlipY3DTransition(Scene(my_save_load_layer)))
        my_save_load_layer.show_save_slot()
    

    def save(self):
        
        _player = self.player
        
        # turn the player's attribution into a dict
        save_data = dict()

        # load the exist player data
        if os.path.isfile(const.SAVE_FILE):
            with open(const.SAVE_FILE) as _file:
                try:
                    save_data = json.load(_file)
                except:
                    print('open file failed')

        _item_equiped_list = []
        _item_box_list = []
        _skill_list = []
        # use the item_to_dict function to turn a item object into a dictionary
        for _ in _player.item_equiped:
            if _:
                _item_equiped_list.append(_.item_to_dict())
            else:
                _item_equiped_list.append(None)
        for _ in _player.item_box:
            _item_box_list.append(_.item_to_dict())
        # for skills, just store the N.O. of the skills
        for _ in _player.skill:
            if _:
                _skill_list.append(_.skill_no)
            else:
                _skill_list.append(None)

        # the name of the player is used to identify the save data
        save_data['slot' + str(_player.save_slot)] = dict(
                player_level=_player.level, 
                hp=_player.hp, 
                item_equiped=_item_equiped_list, 
                gold=_player.gold, 
                exp=_player.exp, 
                zone=_player.zone, 
                alive=_player.alive, 
                epitaph=_player.epitaph, 
                item_box=_item_box_list, 
                skill=_skill_list
                )
        with open(const.SAVE_FILE, 'w') as _file:
            try:
                json.dump(save_data, _file)
            except:
                print('write file failed')

    def load(self, save_slot):
        _player = player.Player(materials.main_scr.sprites['player_sprite'])
        _player.save_slot = save_slot
        with open(const.SAVE_FILE) as _file:
            try:
                save_data = json.load(_file)
            except:
                print('load save file failed')
                sys.exit()
        _data = save_data['slot' + str(save_slot)]

        _player.level = _data['player_level']
        _player.hp = _data['hp']
        _player.gold = _data['gold']
        _player.exp = _data['exp']
        _player.zone = _data['zone']
        _player.alive = _data['alive']
        _player.epitaph = _data['epitaph']

        _player.skill = []
        for _ in _data['skill']:
            if _ is None:
                _player.skill.append(None)
            else:
                _player.skill.append(skill.Skill(_))

        _player.item_equiped = []
        for _ in _data['item_equiped']:
            if _:
                _player.item_equiped.append(item.dict_to_item(_))
            else:
                _player.item_equiped.append(None)

        _player.item_box = []
        for _ in _data['item_box']:
            _player.item_box.append(item.dict_to_item(_))

        return _player

    
    def game_over(self):
        self.game_status = 'GAME_OVER'
        self.player.sprite.image = materials.main_scr.images['rip']

    # the event CORPSE, when the player can pay some money to loot the corpse 
    def show_corpse(self):
        _no_corpse = True
        with open(const.SAVE_FILE) as _file:
            try:
                save_data = json.load(_file)
            except:
                print('load save file failed')
                sys.exit()

        for _, _data in save_data.items():
            if _data['zone']== self.player.zone and (not(_data['alive'])):
                _no_corpse = False
                # e.g self.corpse = 'slot1'
                self.corpse = _
                break

        if _no_corpse:
            self.show_battle()
            return 1

        

        #print('game changes into CORPSE status')
        #print('the COPRSE slot is ', self.corpse)
        self.game_status = 'CORPSE'
        with zipfile.ZipFile(const.MONSTER_ZIP_FILE) as monster_file:
            monster_file_data = monster_file.open(const.CORPSE_EVENT_IMG_FILE)
        materials.main_scr.sprites['enemy_sprite'].image =  pyglet.image.load('', file=monster_file_data) 
        materials.main_scr.sprites['enemy_sprite'].visible = True
    
    # the event CAMP, when the player can pay some money to recover the HP
    # and Enchant the item
    def show_camp(self):
        # if the HP is full then generate enemy
        if self.player.hp >= self.player.max_hp:
            self.show_battle()
            return 1
        self.game_status = 'CAMP'
        with zipfile.ZipFile(const.MONSTER_ZIP_FILE) as monster_file:
            monster_file_data = monster_file.open(const.CAMP_EVENT_IMG_FILE[self.player.zone])
        materials.main_scr.sprites['enemy_sprite'].image =  pyglet.image.load('', file=monster_file_data) 
        materials.main_scr.sprites['enemy_sprite'].visible = True

    def show_battle(self):
        self.enemy = enemy.gen_enemy(None, None, self.player.zone, random.randrange(self.zone * 10 + 1, (self.zone + 1) * 10))
        if self.enemy:
            self.game_status = 'STARTED'
            enemy.show_enemy(self.enemy)
            self.player.loot = []

    def move_on(self):
        self.save()
        _r = random.randrange(1,100)
        if 1<= _r <= const.CORPSE_RATE:
            print('now game is going to show the corpse')
            self.show_corpse()
        elif const.CORPSE_RATE < _r <= const.CORPSE_RATE + const.TENT_RATE:
            self.show_camp()
        else:
            self.show_battle()

    def set_stage(self, no):
        self.player.zone = no
        self.zone = no
        materials.front_layer.labels['zone_label'].element.text = const.ZONE_NAME[no]
        with zipfile.ZipFile(const.MONSTER_ZIP_FILE) as monster_file:
            monster_file_data = monster_file.open(const.ZONE_BACK_IMG_FILES[no])
        my_main.image =  pyglet.image.load('', file=monster_file_data) 
        for _ in range(self.max_stage + 1):
            materials.front_layer.sprites['number' + str(_+1)].visible = True
        materials.front_layer.sprites['map_select'].position = materials.front_layer.sprites['number' + str(no + 1)].position[0], materials.front_layer.sprites['number' + str(no + 1)].position[1] - 20 

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
    my_save_load_layer = materials.save_load_layer.Save_Load_Layer(my_game)
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
