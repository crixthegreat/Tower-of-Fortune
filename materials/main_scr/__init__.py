#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/28 17:03:36
"""THE MAIN SCREEN DEFINITION FILE
"""
import json
import copy
import pyglet
import cocos
from cocos.layer import Layer, ScrollableLayer
import materials
import random
from data import const, player, enemy, battle, item
from data.const import image_from_file

images = {}

player_image = image_from_file(const.PLAYER_IMG_FILE) 
enemy_image = image_from_file(const.ENEMY_IMG_FILE) 
icon_select_image = image_from_file(
        const.ICON_SELECT_IMG_FILE, const.GUI_ZIP_FILE) 
item_box_image = image_from_file(const.ITEM_BOX_IMG_FILE, const.GUI_ZIP_FILE) 

attack_style_image = pyglet.image.ImageGrid(
        pyglet.image.load(const.ATTACK_STYLE_IMG_FILE), 5, 2)


attack_image = image_from_file(const.ATTACK_IMG_FILE, const.GUI_ZIP_FILE) 
defend_image = image_from_file(const.DEFEND_IMG_FILE, const.GUI_ZIP_FILE) 
luck_image = image_from_file(const.LUCK_IMG_FILE, const.GUI_ZIP_FILE) 

main_control_image = image_from_file(
        const.MAIN_CONTROL_IMG_FILE, const.GUI_ZIP_FILE) 
battle_control_image = image_from_file(
        const.BATTLE_CONTROL_IMG_FILE, const.GUI_ZIP_FILE) 
loot_control_image = image_from_file(
        const.LOOT_CONTROL_IMG_FILE, const.GUI_ZIP_FILE) 
corpse_control_image = image_from_file(
        const.CORPSE_CONTROL_IMG_FILE, const.GUI_ZIP_FILE) 
camp_control_image = image_from_file(
        const.CAMP_CONTROL_IMG_FILE, const.GUI_ZIP_FILE) 

images['rip'] = image_from_file(const.RIP_IMG_FILE, const.GUI_ZIP_FILE) 
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
sprites['player_sprite'] = cocos.sprite.Sprite(
        player_image, position=(240, 300))
sprites['enemy_sprite'] = cocos.sprite.Sprite(enemy_image, position=(640, 280))
#sprites['enemy_sprite'].anchor = sprites['enemy_sprite'].width /2, 0

for _ in range(8):
    sprites['loot' + str(_)] = cocos.sprite.Sprite(
            player_image, position=(590 + _ * 30, 210))
sprites['icon_select'] = cocos.sprite.Sprite(
        icon_select_image, position=(562, 185))
sprites['item_box'] = cocos.sprite.Sprite(item_box_image, position=(360, 295))


sprites['style1'] = cocos.sprite.Sprite(attack_image, position=(330, 180))
sprites['style2'] = cocos.sprite.Sprite(defend_image, position=(400, 180))
sprites['style3'] = cocos.sprite.Sprite(luck_image, position=(470, 180))
sprites['attack_style'] = cocos.sprite.Sprite(
        attack_style_image[0], position=(400, 115))

#sprites for control indications
sprites['control'] = cocos.sprite.Sprite(main_control_image, position=(400, 55))
sprites['control'].scale = 0.5

# parameters for the control indications
CONTROL_PARA = dict()
CONTROL_PARA = {
        const.GAME_STATUS['END']:dict(
            position=(400, 50), image=main_control_image, scale=0.4),
        const.GAME_STATUS['STARTED']:dict(
            position=(400, 65), image=battle_control_image, scale=0.55),
        const.GAME_STATUS['LOOT']:dict(
            position=(400, 50), image=loot_control_image, scale=0.4),
        const.GAME_STATUS['CORPSE']:dict(
            position=(400, 65), image=corpse_control_image, scale=0.55),
        const.GAME_STATUS['CAMP']:dict(
            position=(400, 65), image=camp_control_image, scale=0.55)}


for _ in range(3):
    sprites['player_dice_' + str(_)] = cocos.sprite.Sprite(
            materials.dice_image[0], position=(370,250 + 66 * _ ))
    sprites['enemy_dice_' + str(_)] = cocos.sprite.Sprite(
            materials.dice_image[1], position=(450, 250 + 66 * _))

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
        self.image = image_from_file(
                const.ZONE_BACK_IMG_FILES[0], const.GUI_ZIP_FILE)

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

        _sprites = materials.main_scr.sprites
        for _ in range(3):
            _sprites['player_dice_' + str(_)].scale = 0.5
            _sprites['player_dice_' + str(_)].visible = False
            _sprites['enemy_dice_' + str(_)].scale = 0.5
            _sprites['enemy_dice_' + str(_)].visible = False

        # map the keys to methods of every status
        # the keys in GLOBAL status take effects always
        self.key_events = {
                "GLOBAL":{
                    ("I",):self.open_info,
                    ("F2",):self.return_menu},
                "STARTED":{
                    ("UP","LEFT","RIGHT"):self.choose_style},
                "LOOT":{
                    ("LEFT","RIGHT"):self.move_loot_cursor,
                    ("DOWN","UP","ENTER"):self.handle_loot},
                "END":{
                    ("LEFT","RIGHT","DOWN"):self.game.move_on,
                    ("_1","_2","_3","_4","_5","_6"):self.set_stage},
                "GAME_OVER":{
                    ("SPACE",):self.return_menu},
                "CORPSE":{
                    ("LEFT","DOWN"):self.game.move_on,
                    ("UP",):self.buy_corpse},
                "CAMP":{
                    ("LEFT","DOWN"):self.game.move_on,
                    ("UP",):self.go_camp}
                }

    def go_camp(self):
        # have a rest for the price of 1000 * (zone + 1)
        if (self.game.player.gold < 1000 * (self.game.player.zone + 1) 
                or self.game.player.hp >= self.game.player.max_hp):
            return None

        self.game.player.gold -= 1000 * (self.game.player.zone + 1)
        self.game.player.hp = self.game.player.max_hp
        self.game.player.show_player()
        self.game.save()
        self.game.game_status = const.GAME_STATUS['END']


    def buy_corpse(self):
        # press UP to buy all the equiped items of the dead player
        # now the player don't pay for the loot, to be added later
        _equiped_item_data = []
        with open(const.SAVE_FILE) as _file:
            save_data = json.load(_file)
            _equiped_item_data = copy.deepcopy(
                    save_data[self.game.corpse]['item_equiped'])
        with open(const.SAVE_FILE, 'w') as _file:
            del save_data[self.game.corpse]
            json.dump(save_data, _file)

        for _ in _equiped_item_data:
            if _ and len(self.game.player.item_box) < const.MAX_ITEM_BOX:
                self.game.player.item_box.append(item.dict_to_item(_))
        
        materials.main_scr.sprites['enemy_sprite'].visible = False
        self.game.save()
        self.game.game_status = const.GAME_STATUS['END']
        #print('looting the corpse succeed, game status changes to END')



    def set_stage(self, key):
        _map_no = int(key[1]) - 1
        if _map_no <= self.game.max_stage:
            self.game.set_stage(_map_no)


    def handle_loot(self, key):
        """sell, equip or take the loot
        """
        if not(self.game.player.loot):
            return None
        _loot = self.game.player.loot
        # take the loot
        if 'DOWN' == key:
            self.game.player.add_to_item_box(_loot[self.game.loot_selected])
        # sell the loot
        elif 'UP' == key:
            self.game.player.sell_item(_loot[self.game.loot_selected])
        # equip the loot
        elif 'ENTER' == key:
            self.game.player.equip_item(_loot[self.game.loot_selected])
        self.game.player.loot.remove(
                self.game.player.loot[self.game.loot_selected])
        if self.game.loot_selected > len(self.game.player.loot) - 1:
            self.game.loot_selected -= 1
        if self.game.loot_selected == -1:
            self.game.loot_selected = 0
        self.game.player.show_player()
        self.game.show_loot()
        self.game.save()

    def move_loot_cursor(self, key):
        if not(self.game.player.loot):
            return None
        _loot = self.game.player.loot
        # select the next(right) loot
        if 'RIGHT' == key:
            for _ in range(self.game.loot_selected + 1, len(_loot)):
                if _loot[_]:
                    self.game.loot_selected = _
                    materials.main_scr.sprites['icon_select'].x = 562 + (30 * _)
                    item.show(
                            _loot[_], 
                            self.game.player.item_equiped[_loot[_].equiped_pos])
                    break
        # select the left loot
        elif 'LEFT' == key:
            for _ in range(self.game.loot_selected -1, -1, -1):
                if _loot[_]:
                    self.game.loot_selected = _
                    materials.main_scr.sprites['icon_select'].x = 562 + (30 * _)
                    item.show(
                            _loot[_], 
                            self.game.player.item_equiped[_loot[_].equiped_pos])
                    break

    def open_info(self):
        # open the player information screen
        self.keys_pressed.clear()
        self.game.show_info()
    
    def return_menu(self):
        # return to the menu(title) screen
        self.keys_pressed.clear()
        self.game.show_menu()

    def choose_style(self, key):
        _style = self.style_cal(self.game.style)
        # 10 is used to tell that the style choose is not finished
        if _style >= 10:
            _round = self.game.style[0] + self.game.style[1] + self.game.style[2]
            if 'RIGHT' == key:
                self.game.style[0] += 1
                sprites['style' + str(_round + 1)].visible = True
                sprites['style' + str(_round + 1)].image = attack_image
            elif 'LEFT' == key:
                self.game.style[1] += 1
                sprites['style' + str(_round + 1)].visible = True
                sprites['style' + str(_round + 1)].image = defend_image
            elif 'UP' == key:
                self.game.style[2] += 1
                sprites['style' + str(_round + 1)].visible = True
                sprites['style' + str(_round + 1)].image = luck_image
        

    def refresh_time(self, dt):
        """this is a method executed automatically every time-interval
        if a status-change should happen after a special-effects(namely Actions)
        then it need be put into this method
        """
        # the 'dt' means the time passed after the last event occured
        
        # the set focus method is not used in this game
        #self.game.screen_set_focus(
        #    self.game.player.sprite.x, self.game.player.sprite.y)
        
        # if any actions (namely some effects) are running 
        # exit the method
        for _, _sprite in materials.sprites.items():
            if _sprite.are_actions_running():
                return None
        for _, _sprite in materials.main_scr.sprites.items():
            if _sprite.are_actions_running():
                return None
        for _, _label in materials.front_layer.labels.items():
            if _label.are_actions_running():
                return None

        _action_label = []
        _action_label.append(materials.front_layer.labels['enemy_hp_change_label'])
        _action_label.append(materials.front_layer.labels['player_hp_change_label'])
        _action_label.append(materials.front_layer.labels['player_hp_regen_label'])
        _action_label.append(materials.front_layer.labels['player_hp_absorb_label'])
        for _ in _action_label:
            _.visible = False

        _sprites = materials.main_scr.sprites
        if self.game.game_status == const.GAME_STATUS['STARTED']:
            _style = self.style_cal(self.game.style)
            if  0<= _style <= 9: 
                # attack starts
                _r = battle.player_attack(
                        self.game.player, self.game.enemy, _style)
                _sprites['style1'].visible = False
                _sprites['style2'].visible = False
                _sprites['style3'].visible = False
                _sprites['attack_style'].visible = True
                _sprites['attack_style'].scale = 0.35
                _sprites['attack_style'].image = (
                        materials.main_scr.attack_style_image[_style])
                self.game.style = [0, 0, 0]
                if not _r:
                    self.game.game_status = const.GAME_STATUS['BATTLE_END']
                    self.game.save()
                    if self.game.player.hp <= 0:
                        self.game.game_over()
                    return None
                self.game.save()
        if self.game.game_status == const.GAME_STATUS['BATTLE_END']:
            for _ in range(3):
                _sprites['player_dice_' + str(_)].visible = False
                _sprites['enemy_dice_' + str(_)].visible = False
            _sprites['enemy_sprite'].visible = True
            _sprites['enemy_sprite'].image = images['rip']
            _loot_list = self.game.player.loot
            if _loot_list:
                self.game.game_status = const.GAME_STATUS['LOOT']
                self.game.show_loot()
                item.show(_loot_list[0], 
                        self.game.player.item_equiped[_loot_list[0].equiped_pos])
            else:
                self.game.game_status = const.GAME_STATUS['END']
            self.game.player.show_player()
        elif  self.game.game_status == const.GAME_STATUS['LOOT']:
            if not self.game.player.loot:
                self.game.game_status = const.GAME_STATUS['END']


    def on_key_press(self, key, modifiers):
        # use a set(keys_pressed) to store all the keys pressed
        # the number '983547510784' means 'SHIFT + SPACE' key
        #_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if key != 983547510784:
            self.keys_pressed.add(key)
        key_names = [
                pyglet.window.key.symbol_string(k) for k in self.keys_pressed]

        materials.do_key_events(self, 'GLOBAL', key_names)
        materials.do_key_events(self, self.game.game_status, key_names)
                
    def style_cal(self, _style):
        """calculate the style value by the three cards(_style)
        _style is a list containing the three cards the player chosed
        """
        if _style[0] + _style[1] + _style[2] != 3:
            return 10
        
        return const.STYLE_VALUE[tuple(_style)]
        

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
    
