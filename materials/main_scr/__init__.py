#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/28 17:03:36
"""THE MAIN SCREEN DEFINITION FILE
"""
import sys
import os
import json
import copy
import zipfile
from data import const, player, enemy, skill, battle, item
import pyglet
import cocos
from cocos.layer import Layer, ScrollingManager, ScrollableLayer
import materials
import random

#player_image = []
#player_image = pyglet.image.ImageGrid(pyglet.image.load('./pic/player.png'), 1, 3)
#images = {'player_img':player_image}
images = {}

player_image = const.image_from_file(const.PLAYER_IMG_FILE) 
enemy_image = const.image_from_file(const.ENEMY_IMG_FILE) 
icon_select_image = pyglet.image.load(os.path.abspath(const.ICON_SELECT_IMG_FILE)) 
item_box_image = pyglet.image.load(os.path.abspath(const.ITEM_BOX_IMG_FILE)) 
attack_style_image = pyglet.image.ImageGrid(pyglet.image.load('./pic/attack_style.png'), 5, 2)


attack_image = pyglet.image.load(os.path.abspath(const.ATTACK_IMG_FILE)) 
defend_image = pyglet.image.load(os.path.abspath(const.DEFEND_IMG_FILE)) 
luck_image = pyglet.image.load(os.path.abspath(const.LUCK_IMG_FILE)) 

main_control_image = pyglet.image.load(os.path.abspath(const.MAIN_CONTROL_IMG_FILE)) 
battle_control_image = pyglet.image.load(os.path.abspath(const.BATTLE_CONTROL_IMG_FILE)) 
loot_control_image = pyglet.image.load(os.path.abspath(const.LOOT_CONTROL_IMG_FILE)) 
corpse_control_image = pyglet.image.load(os.path.abspath(const.CORPSE_CONTROL_IMG_FILE)) 
camp_control_image = pyglet.image.load(os.path.abspath(const.CAMP_CONTROL_IMG_FILE)) 

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
        x=430, y=370)
labels['item_type'] = cocos.text.Label('',font_size=9,
        font_name = 'Gadugi',
        bold=False,
        color=const.DEFAULT_COLOR, 
        x=430, y=350, width=200, multiline=True)
labels['item_main_affix'] = cocos.text.Label('',font_size=12,
        font_name = 'Gadugi',
        bold=True,
        color=const.HIGHLIGHT_COLOR, 
        x=430, y=315)
labels['item_affix'] = cocos.text.Label('',font_size=9,
        font_name = 'Gadugi',
        bold=False,
        color=const.DEFAULT_COLOR, 
        x=430, y=295, width=200, multiline=True)
labels['player_item_name'] = cocos.text.Label('',font_size=12,
        font_name = 'Gadugi',
        bold=True,
        color=const.HIGHLIGHT_COLOR, 
        x=245, y=350)
labels['player_item_type'] = cocos.text.Label('',font_size=9,
        font_name = 'Gadugi',
        bold=False,
        color=const.DEFAULT_COLOR, 
        x=245, y=330, width=200, multiline=True)
labels['player_item_main_affix'] = cocos.text.Label('',font_size=12,
        font_name = 'Gadugi',
        bold=True,
        color=const.HIGHLIGHT_COLOR, 
        x=245, y=295)
labels['player_item_affix'] = cocos.text.Label('',font_size=9,
        font_name = 'Gadugi',
        bold=False,
        color=const.DEFAULT_COLOR, 
        x=245, y=275, width=200, multiline=True)

sprites = {}
sprites['player_sprite'] = cocos.sprite.Sprite(player_image, position=(240, 300))
sprites['enemy_sprite'] = cocos.sprite.Sprite(enemy_image, position=(640, 280))
#sprites['enemy_sprite'].anchor = sprites['enemy_sprite'].width /2, 0

for _ in range(8):
    sprites['loot' + str(_)] = cocos.sprite.Sprite(player_image, position=(590 + _ * 30, 210))
sprites['icon_select'] = cocos.sprite.Sprite(icon_select_image, position=(562, 185))
sprites['item_box'] = cocos.sprite.Sprite(item_box_image, position=(360, 295))


sprites['style1'] = cocos.sprite.Sprite(attack_image, position=(330, 180))
sprites['style2'] = cocos.sprite.Sprite(defend_image, position=(400, 180))
sprites['style3'] = cocos.sprite.Sprite(luck_image, position=(470, 180))
sprites['attack_style'] = cocos.sprite.Sprite(attack_style_image[0], position=(400, 115))

#sprites for control indications
sprites['control'] = cocos.sprite.Sprite(main_control_image, position=(400, 55))
sprites['control'].scale = 0.5


for _ in range(3):
    sprites['player_dice_' + str(_)] = cocos.sprite.Sprite(materials.dice_image[0], position=(370,250 + 66 * _ ))
    sprites['enemy_dice_' + str(_)] = cocos.sprite.Sprite(materials.dice_image[1], position=(450, 250 + 66 * _))

bg_music = materials.Audio(const.BG_MUSIC_FILE)
highscore_music = materials.Audio(const.HIGHSCORE_MUSIC_FILE)

class Main_Screen(ScrollableLayer):
    """The main game screen
    do a lot of key events
    """
    is_event_handler = True

    def __init__(self, game):

        super(Main_Screen, self).__init__()
        self.game = game
        self.keys_pressed = set()
        with zipfile.ZipFile(const.MONSTER_ZIP_FILE) as monster_file:
            monster_file_data = monster_file.open(const.ZONE_BACK_IMG_FILES[0])
        self.image =  pyglet.image.load('', file=monster_file_data) 

        if hasattr(materials.main_scr, 'sprites'):
            for _, _sprite in materials.main_scr.sprites.items():
                self.add(_sprite)
                _sprite.visible = False
        if hasattr(materials, 'sprites'):
            for _, _sprite in materials.sprites.items():
                self.add(_sprite)
                _sprite.visible = False
        if hasattr(materials, 'labels'):
            for _, _label in materials.labels.items():
                self.add(_label)
                _label.visible = False
        if hasattr(materials.main_scr, 'labels'):
            for _, _label in materials.main_scr.labels.items():
                self.add(_label)
                _label.visible = False
        materials.sprites['strike'].visible = False
        materials.sprites['explode'].visible = False
        materials.main_scr.sprites['icon_select'].visible = False
        materials.main_scr.sprites['icon_select'].scale = 0.25
        for _ in range(8):
            materials.main_scr.sprites['loot' + str(_)].visible = False
            materials.main_scr.sprites['loot' + str(_)].scale = 0.4

        if hasattr(materials, 'labels'):
            for _, _label in materials.labels.items():
                self.add(_label)
                _label.visible = False

        # control sprite is always visible
        materials.main_scr.sprites['control'].visible = True
        # use the time interval event to calculate the time used
        self.schedule_interval(self.refresh_time, 0.1)

        for _ in range(3):
            materials.materials.main_scr.sprites['player_dice_' + str(_)].scale = 0.5
            materials.materials.main_scr.sprites['player_dice_' + str(_)].visible = False
            materials.materials.main_scr.sprites['enemy_dice_' + str(_)].scale = 0.5
            materials.materials.main_scr.sprites['enemy_dice_' + str(_)].visible = False

    def refresh_time(self, dt):
        # the 'dt' means the time passed after the last event occured
        self.game.screen_set_focus(self.game.player.sprite.x, self.game.player.sprite.y) 
        for _, _sprite in materials.sprites.items():
            if _sprite.are_actions_running():
                return None
        for _, _sprite in materials.main_scr.sprites.items():
            if _sprite.are_actions_running():
                return None
        for _, _label in materials.front_layer.labels.items():
            if _label.are_actions_running():
                return None

        if self.game.game_status == 'STARTED':
            _style = self.style_cal(self.game.style)
            if  0<= _style <= 9: 
                # attack starts
                _r = battle.player_attack(self.game.player, self.game.enemy, _style)
                materials.main_scr.sprites['style1'].visible = False
                materials.main_scr.sprites['style2'].visible = False
                materials.main_scr.sprites['style3'].visible = False
                materials.main_scr.sprites['attack_style'].visible = True
                materials.main_scr.sprites['attack_style'].scale = 0.35
                materials.main_scr.sprites['attack_style'].image = materials.main_scr.attack_style_image[_style]
                self.game.style = [0, 0, 0]
                if not _r:
                    for _ in range(3):
                        materials.main_scr.sprites['player_dice_' + str(_)].visible = False
                        materials.main_scr.sprites['enemy_dice_' + str(_)].visible = False
                    self.game.game_status = 'BATTLE_END'
                    self.game.save()
                    if self.game.player.hp <= 0:
                        self.game.game_over()
                    return None
                self.game.save()
        if self.game.game_status == 'BATTLE_END':
            materials.main_scr.sprites['enemy_sprite'].visible = True
            materials.main_scr.sprites['enemy_sprite'].image = materials.main_scr.images['rip']
            _loot_list = self.game.player.loot
            if _loot_list:
                self.game.game_status = 'LOOT'
                self.game.show_loot()
                item.show(_loot_list[0], self.game.player.item_equiped[_loot_list[0].equiped_pos])
            else:
                self.game.game_status = 'END'
            self.game.player.show_player()
        elif  self.game.game_status == 'LOOT':
            if not self.game.player.loot:
                self.game.game_status = 'END'


    def on_key_press(self, key, modifiers):
        # use a set(keys_pressed) to store all the keys pressed
        # the number '983547510784' means 'SHIFT + SPACE' key
        _str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if key != 983547510784:
            self.keys_pressed.add(key)
        key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]
        # press the SPACE key to return to the title anywhere any time
        #print(key_names)
        if 'F2' in key_names:
            # return to the menu(title) screen
            self.keys_pressed.clear()
            self.game.show_menu()
        if 'I' in key_names:
            # open the player information screen
            self.keys_pressed.clear()
            self.game.show_info()
        # get the input of the attack style     
        elif self.game.game_status == 'STARTED':
            _round = self.game.style[0] + self.game.style[1] + self.game.style[2]
            _style = self.style_cal(self.game.style)
            if _style >= 10:
                if 'RIGHT' in key_names:
                    self.game.style[0] += 1
                    sprites['style' + str(_round + 1)].visible = True
                    sprites['style' + str(_round + 1)].image = attack_image
                elif 'LEFT' in key_names:
                    self.game.style[1] += 1
                    sprites['style' + str(_round + 1)].visible = True
                    sprites['style' + str(_round + 1)].image = defend_image
                elif 'UP' in key_names:
                    self.game.style[2] += 1
                    sprites['style' + str(_round + 1)].visible = True
                    sprites['style' + str(_round + 1)].image = luck_image
        # when the battle ends
        elif self.game.game_status == 'LOOT':
            if self.game.player.loot:
                _loot = self.game.player.loot
                # sell, equip or take
                if 'UP' in key_names or 'DOWN' in key_names or 'ENTER' in key_names:
                    # take the loot
                    if 'DOWN' in key_names:
                        self.game.player.add_to_item_box(_loot[self.game.loot_selected])
                    # sell the loot
                    elif 'UP' in key_names:
                        self.game.player.sell_item(_loot[self.game.loot_selected])
                    # equip the loot
                    elif 'ENTER' in key_names:
                        self.game.player.equip_item(_loot[self.game.loot_selected])
                    self.game.player.loot.remove(self.game.player.loot[self.game.loot_selected])
                    if self.game.loot_selected > len(self.game.player.loot) - 1:
                        self.game.loot_selected -= 1
                    if self.game.loot_selected == -1:
                        self.game.loot_selected = 0
                    self.game.player.show_player()
                    self.game.show_loot()
                    self.game.save()
                # select the next(right) loot
                elif 'RIGHT' in key_names:
                    for _ in range(self.game.loot_selected + 1, len(_loot)):
                        if _loot[_]:
                            self.game.loot_selected = _
                            materials.main_scr.sprites['icon_select'].x = 562 + (30 * _)
                            item.show(_loot[_], self.game.player.item_equiped[_loot[_].equiped_pos])
                            break
                # select the left loot
                elif 'LEFT' in key_names:
                    for _ in range(self.game.loot_selected -1, -1, -1):
                        if _loot[_]:
                            self.game.loot_selected = _
                            materials.main_scr.sprites['icon_select'].x = 562 + (30 * _)
                            item.show(_loot[_], self.game.player.item_equiped[_loot[_].equiped_pos])
                            break
                # not used
                elif 'SPACE' in key_names:
                    pass
        elif self.game.game_status == 'END':
            _set = set(['DOWN','RIGHT','LEFT'])
            _map_set = set(['_1', '_2', '_3', '_4', '_5', '_6'])
            _map = list(_map_set & set(key_names))
            if _set & set(key_names):
                self.game.move_on()
            elif _map:
                _map_no = int(_map[0][1]) - 1
                if _map_no <= self.game.max_stage:
                    self.game.set_stage(_map_no)

        elif self.game.game_status == 'GAME_OVER':
            if 'SPACE' in key_names:
                # return to the menu(title) screen
                self.keys_pressed.clear()
                self.game.show_menu()

        elif self.game.game_status == 'CORPSE':
            # press UP to buy all the equiped items of the dead player
            # now the player don't pay for the loot, to be added later
            if 'UP' in key_names:
                _equiped_item_data = []
                with open(const.SAVE_FILE) as _file:
                    save_data = json.load(_file)
                    _equiped_item_data = copy.deepcopy(save_data[self.game.corpse]['item_equiped'])
                with open(const.SAVE_FILE, 'w') as _file:
                    del save_data[self.game.corpse]
                    json.dump(save_data, _file)
                    #print('failed to load the save file and to delete the copse data and to save the file again')

                for _ in _equiped_item_data:
                    if _ and len(self.game.player.item_box) < const.MAX_ITEM_BOX:
                        self.game.player.item_box.append(item.dict_to_item(_))
                
                materials.main_scr.sprites['enemy_sprite'].visible = False
                self.game.save()
                self.game.game_status = 'END'
                print('looting the corpse succeed, game status changes to END')

            elif 'LEFT' in key_names or 'RIGHT' in key_names:
                self.game.move_on()

        elif self.game.game_status == 'CAMP':
            # rest for 1000 * (zone + 1)
            if 'RIGHT' in key_names or 'LEFT' in key_names:
                self.game.move_on()
            elif 'UP' in key_names and self.game.player.gold >= 1000 * (self.game.player.zone + 1) and self.game.player.hp < self.game.player.max_hp:
                self.game.player.gold -= 1000 * (self.game.player.zone + 1)
                self.game.player.hp = self.game.player.max_hp
                self.game.player.show_player()
                self.game.save()
                self.game.game_status = 'END'
                

                
    def style_cal(self, _style):
        if _style[0] + _style[1] + _style[2] != 3:
            return 10
        if _style[0] == 0:
            if _style[1] == 0:
                return 9
            elif _style[1] == 1:
                return 6
            elif _style[2] == 2:
                return 7
            else:
                return 8
        elif _style[0] == 1:
            if _style[1] == 0:
                return 5
            elif _style[1] == 1:
                return 4
            else:
                return 3
        elif _style[0] == 2:
            if _style[1] == 0:
                return 2
            else:
                return 1
        else:
            return 0

        print('attack style calculate error!')
        sys.exit()


    def on_key_release(self, key, modifiers):
        
        #print('main key:', self.keys_pressed)
        if self.keys_pressed and key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def draw(self):
        self.image.blit(0, 230)



def show(level=None):
    """to display main game screen
    """
    materials.menu.bg_music.stop()
    materials.main_scr.highscore_music.stop()
    bg_music.play(-1)
    return None
    
