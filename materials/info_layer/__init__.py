#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/28 17:03:36
"""The info layer definition file
"""
import os
import copy
from data import const, skill, item
import pyglet
import cocos
from cocos.layer import Layer, ScrollingManager, ScrollableLayer
import materials


images = {}

single_item_box_image = pyglet.image.load(os.path.abspath(const.SINGLE_ITEM_BOX_IMG_FILE)) 
single_equiped_item_box_image = pyglet.image.load(os.path.abspath(const.SINGLE_EQUIPED_ITEM_BOX_IMG_FILE)) 
"""
time_label & best_time_label : as the name says
"""

labels = {}

labels['skill_description_label'] = cocos.text.Label('', 
        font_size=10,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=35, y=435, width = 10, multiline=True)
labels['player_value_label'] = cocos.text.Label('', 
        font_size=12.5,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=295, y=562, width = 10, multiline=True)
labels['item_box_page'] = cocos.text.Label('NA/NA', 
        font_size=12,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=715, y=20)

labels['item_name'] = cocos.text.Label('',font_size=12,
        font_name = 'Gadugi',
        bold=True,
        color=const.HIGHLIGHT_COLOR, 
        x=648, y=325)
labels['item_type'] = cocos.text.Label('',font_size=9,
        font_name = 'Gadugi',
        bold=False,
        color=const.DEFAULT_COLOR, 
        x=648, y=305, width=200, multiline=True)
labels['item_main_affix'] = cocos.text.Label('',font_size=12,
        font_name = 'Gadugi',
        bold=True,
        color=const.HIGHLIGHT_COLOR, 
        x=648, y=270)
labels['item_affix'] = cocos.text.Label('',font_size=9,
        font_name = 'Gadugi',
        bold=False,
        color=const.DEFAULT_COLOR, 
        x=648, y=250, width=200, multiline=True)

labels['player_item_name'] = cocos.text.Label('',font_size=12,
        font_name = 'Gadugi',
        bold=True,
        color=const.HIGHLIGHT_COLOR, 
        x=648, y=555)
labels['player_item_type'] = cocos.text.Label('',font_size=9,
        font_name = 'Gadugi',
        bold=False,
        color=const.DEFAULT_COLOR, 
        x=648, y=535, width=200, multiline=True)
labels['player_item_main_affix'] = cocos.text.Label('',font_size=12,
        font_name = 'Gadugi',
        bold=True,
        color=const.HIGHLIGHT_COLOR, 
        x=648, y=500)
labels['player_item_affix'] = cocos.text.Label('',font_size=9,
        font_name = 'Gadugi',
        bold=False,
        color=const.DEFAULT_COLOR, 
        x=648, y=480, width=200, multiline=True)


skill_select_image = pyglet.image.load(os.path.abspath(const.SKILL_SELECT_IMG_FILE)) 
item_select_image =  pyglet.image.load(os.path.abspath(const.ITEM_SELECT_IMG_FILE)) 

sprites = {}

sprites['skill_select'] = cocos.sprite.Sprite(skill_select_image, position=(45, 520))
sprites['skill_choose'] = cocos.sprite.Sprite(skill_select_image, position=(45, 400))

sprites['single_item_box'] = cocos.sprite.Sprite(single_item_box_image, position=(670, 260))
sprites['single_item_box'].scale = 0.45
sprites['single_equiped_item_box'] = cocos.sprite.Sprite(single_equiped_item_box_image, position=(670, 485))
sprites['single_equiped_item_box'].scale = 0.45
sprites['item'] = cocos.sprite.Sprite(materials.item_image[0], position = (620,285))
sprites['item'].scale = 0.6
sprites['player_item'] = cocos.sprite.Sprite(materials.item_image[0], position = (620,515))
sprites['player_item'].scale = 0.6

# sprites of equiped items
for n in range(13):
    sprites['equiped_item' + str(n)] = cocos.sprite.Sprite(materials.item_image[0], position=(0,0))
    _start_x = 455
    _start_y = 527
    # main hand
    if n == 0:
        _tx = _start_x - 66
        _ty = _start_y - 291
    # off hand
    elif n == 1:
        _tx = _start_x + 63
        _ty = _start_y - 291
    # head
    elif n == 2:
        _tx = _start_x
        _ty = _start_y
    # shoulder
    elif n == 3:
        _tx = _start_x - 50
        _ty = _start_y - 50
    # necklace
    elif n == 4:
        _tx = _start_x + 53
        _ty = _start_y - 23
    #chest
    elif n == 5:
        _tx = _start_x
        _ty = _start_y - 68
    # wrist
    elif n == 6:
        _tx = _start_x + 53
        _ty = _start_y - 105
    # gloove
    elif n == 7:
        _tx = _start_x - 66
        _ty = _start_y - 145
    # waist    
    elif n == 8:
        _tx = _start_x
        _ty = _start_y - 140
    # leg
    elif n == 9:
        _tx = _start_x + 17
        _ty = _start_y - 215
    # shoe
    elif n == 10:
        _tx = _start_x - 26
        _ty = _start_y - 265
    # ringA
    elif n == 11:
        _tx = _start_x - 64
        _ty = _start_y - 215
    # ringB
    elif n == 12:
        _tx = _start_x + 63
        _ty = _start_y - 215
    
    sprites['equiped_item' + str(n)].position = _tx, _ty

# sprites of current page of the item box
for _ in range(13):
    sprites['item_box' + str(_)] = cocos.sprite.Sprite(materials.item_image[0], position=(47 + 59 * _, 79))
    sprites['item_box' + str(_)].scale = 0.6


sprites['equiped_item_select'] = cocos.sprite.Sprite(item_select_image, position=(350, 400))
sprites['item_box_select'] = cocos.sprite.Sprite(item_select_image, position=(46, 80))
#bg_music = materials.Audio(Const.BG_MUSIC_FILE)

class Info_Layer(Layer):
    """the player information screen
    """

    is_event_handler = True

    def __init__(self, game):
        super(Info_Layer, self).__init__()

        self.keys_pressed = set()


        if hasattr(materials.info_layer, 'sprites'):
            for _, _sprite in materials.info_layer.sprites.items():
                self.add(_sprite)
                _sprite.visible = False
        materials.info_layer.sprites['skill_select'].scale = 0.4
        materials.info_layer.sprites['skill_choose'].scale = 0.4
        materials.info_layer.sprites['equiped_item_select'].scale = 0.3
        materials.info_layer.sprites['item_box_select'].scale = 0.4

        if hasattr(materials.info_layer, 'labels'):
            for _, _label in materials.info_layer.labels.items():
                self.add(_label)
        self.add(materials.front_layer.labels['level_label'])
        self.add(materials.front_layer.labels['gold_label'])
        self.add(materials.front_layer.labels['hp_label'])
        self.add(materials.front_layer.labels['exp_label'])
        self.add(materials.front_layer.labels['player_skill_label'])

        self.game = game
        self.image = materials.images['info_layer_img']
        self.status = 'view'
        self.skill_selected = 0
        self.skill_chosen = 0
        self.item_equiped_selected = 0
        self.item_box_selected = 0

        #self.game.show_info()

    def on_key_press(self, key, modifiers):
        """key press handler for info class
        """
        self.keys_pressed.add(key)
        key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]
        
        if 'I' in key_names:
            self.skill_choose()
            self.skill_select()
            self.equiped_item_select()
            self.item_box_select('clear')
            self.status == 'view'
            self.game.show_game()
            self.game.save()

        if self.status == 'view':

            if 'ENTER' in key_names:
                pass
            elif 'UP' in key_names:
                pass
            # check the equiped item
            elif 'E' in key_names:
                self.item_equiped_selected = 0
                self.status = 'equiped_item_select'
                self.equiped_item_select(self.game.player, 0)
                
            # set skill
            elif 'S' in key_names and self.game.game_status == 'END':
                self.skill_selected = 0
                self.skill_select(self.game.player, 0)
                self.status = 'skill'

            # check the item box
            elif 'B' in key_names and self.game.game_status == 'END' and self.game.player.item_box:
                self.status = 'item_box'
                self.item_box_selected = 0
                self.item_box_select()


        elif self.status == 'item_box':
            if 'LEFT' in key_names:
                _pos = self.item_box_selected % 13
                if _pos > 0:
                    self.item_box_selected -= 1
                else:
                    _pos = self.item_box_selected // 13 * 13 + 12
                    if _pos > (len(self.game.player.item_box) - 1):
                        self.item_box_selected = len(self.game.player.item_box) - 1
                    else:
                        self.item_box_selected = _pos
                self.item_box_select()
            elif 'RIGHT' in key_names:
                if self.item_box_selected >= len(self.game.player.item_box) - 1 or (self.item_box_selected % 13) == 12:
                    self.item_box_selected = self.item_box_selected // 13 * 13
                else:
                    self.item_box_selected += 1
                self.item_box_select()
            # show the next page
            elif 'DOWN' in key_names:
                # the _pos is the first position of next page
                _pos = self.item_box_selected // 13 * 13 + 13
                if _pos <= len(self.game.player.item_box) - 1:
                    self.item_box_selected = _pos
                else:
                    self.item_box_selected = 0
                self.show_item_box()
                self.item_box_select()
            # show the upper page
            elif 'UP' in key_names:
                if self.item_box_selected > 12:
                    self.item_box_selected -= 12
                elif len(self.game.player.item_box) > 13:
                    self.item_box_selected = (len(self.game.player.item_box) - 1) // 13 * 13
                self.show_item_box()
                self.item_box_select()
            # sell the item in the item box
            elif 'S' in key_names:
                self.game.player.sell_item(self.game.player.item_box.pop(self.item_box_selected))
                if self.game.player.item_box:
                    if self.item_box_selected >= len(self.game.player.item_box):
                        self.item_box_selected = len(self.game.player.item_box) - 1
                    self.item_box_select()
                # if sold out
                else:
                    self.item_box_select('clear')
                self.show_item_box()
                self.game.save()
            # close the item box    
            elif 'SPACE' in key_names:
                self.item_box_select(clear=True)
                self.hide_item()
                self.status = 'view'
            # equip the item from the item box
            elif 'ENTER' in key_names:
                self.game.player.equip_item(self.game.player.item_box.pop(self.item_box_selected))
                self.show_item_box()
                self.show_player_item()
                self.item_box_select()
                self.show_player_value()
                if self.game.player.hp > self.game.player.max_hp:
                    self.game.player.hp = self.game.player.max_hp
                self.game.player.show_player()
                self.game.save()
                


        elif self.status == 'equiped_item_select':
            if 'LEFT' in key_names:
                if self.item_equiped_selected > 0:
                    self.item_equiped_selected -= 1
                    self.equiped_item_select(self.game.player, self.item_equiped_selected)
                else:
                    self.item_equiped_selected = 12
                    self.equiped_item_select(self.game.player, self.item_equiped_selected)

            elif 'RIGHT' in key_names:
                if self.item_equiped_selected < 12:
                    self.item_equiped_selected += 1
                    self.equiped_item_select(self.game.player, self.item_equiped_selected)
                else:
                    self.item_equiped_selected = 0
                    self.equiped_item_select(self.game.player, self.item_equiped_selected)
                        
            elif 'SPACE' in key_names:
                self.equiped_item_select()
                self.hide_item()
                self.status = 'view'
        elif self.status == 'skill':
            _skill_no = self.game.player.skill_quantity
            if 'LEFT' in key_names:
                if self.skill_selected > 0:
                    self.skill_selected -= 1
                else:
                    self.skill_selected = _skill_no -1
                self.skill_select(self.game.player, self.skill_selected)
            elif 'RIGHT' in key_names:
                if self.skill_selected < _skill_no -1:
                    self.skill_selected += 1
                else:
                    self.skill_selected = 0
                self.skill_select(self.game.player, self.skill_selected)
            elif 'UP' in key_names or 'SPACE' in key_names:
                self.skill_select()
                self.status = 'view'
            elif 'DOWN' in key_names or 'ENTER' in key_names:
                self.status = 'skill_choose'
                self.skill_chosen = 0
                self.skill_choose(0)
        elif self.status == 'skill_choose':
            if 'LEFT' in key_names:
                if self.skill_chosen > 0:
                    self.skill_chosen -= 1
                else:
                    self.skill_chosen = 14
                self.skill_choose(self.skill_chosen)
            elif 'RIGHT' in key_names:
                if self.skill_chosen < 14:
                    self.skill_chosen += 1
                else:
                    self.skill_chosen = 0
                self.skill_choose(self.skill_chosen)
            elif 'UP' in key_names:
                if self.skill_chosen > 2:
                    self.skill_chosen -= 3
                else:
                    self.skill_chosen += 12
                self.skill_choose(self.skill_chosen)
            elif 'DOWN' in key_names:
                if self.skill_chosen < 12:
                    self.skill_chosen += 3
                else:
                    self.skill_chosen -= 12
                self.skill_choose(self.skill_chosen)
            elif 'ENTER' in key_names:
                _skill = skill.Skill(self.skill_chosen)
                # for skill 12- dual swing,13- double hand weapon,14- standard style
                if self.skill_chosen == 12:
                    if self.game.player.item_equiped[1].main_type != 0:
                        _skill = None
                elif self.skill_chosen == 13:
                    if self.game.player.item_equiped[0].main_type != 1:
                        _skill = None
                elif self.skill_chosen == 14:
                    if self.game.player.item_equiped[1].main_type != 2:
                        _skill = None

                # if the player had the skill already:
                for _ in self.game.player.skill:
                    if _:
                        if _.skill_no == self.skill_chosen:
                            _skill = None
                            break

                if _skill:
                    self.game.player.skill[self.skill_selected] = _skill
                    self.skill_choose()
                    self.skill_select(self.game.player, self.skill_selected)
                    self.status = 'skill'
                    self.game.refresh_info()
                    self.game.save()

            elif 'SPACE' in key_names:
                self.skill_choose()
                self.status = 'skill'

    def show_item_box(self):
        if self.game.player.item_box:
            _page = self.item_box_selected // 13
            for _ in range(13):
                _item_no = _page * 13 + _
                if _item_no >= len(self.game.player.item_box):
                    sprites['item_box' + str(_)].visible = False
                else:
                    sprites['item_box' + str(_)].visible = True
                    sprites['item_box' + str(_)].image = materials.item_image[(59 - self.game.player.item_box[_item_no].type) * 5 + self.game.player.item_box[_item_no].rare_type]
            labels['item_box_page'].element.text = str((self.item_box_selected // 13) + 1) + '/' + str(len(self.game.player.item_box) // 13 + 1)
        else:
            for _ in range(13):
                sprites['item_box' + str(_)].visible = False
            self.hide_item()


    def item_box_select(self, clear=None):
        if clear:
            sprites['item_box_select'].visible = False
            self.item_box_selected = 0
            self.status = 'view'
            self.hide_item()
        else:
            if self.game.player.item_box:
                _item_no = self.item_box_selected % 13
                sprites['item_box_select'].visible = True
                sprites['item_box_select'].position = 47 + 59 * _item_no, 79
                self.show_item(self.game.player.item_box[self.item_box_selected], self.game.player.item_equiped[self.game.player.item_box[self.item_box_selected].equiped_pos])

    # show the item for the info_layer
    def show_item(self, item, player_item):

        if item:
            sprites['item'].visible = True
            sprites['item'].image = materials.item_image[(59-item.type) * 5 + item.rare_type]
            sprites['single_item_box'].visible = True

            labels['item_name'].element.text = item.name
            labels['item_type'].element.text = 'Lv ' + str(item.level) + '\n' + const.RARE_TYPE_NAME[item.rare_type] + ' ' + const.MAIN_TYPE_NAME[item.main_type]
            labels['item_name'].visible = True
            labels['item_type'].visible = True
            labels['item_main_affix'].visible = True
            labels['item_affix'].visible = True
            _list = []
            for _ in range(const.AFFIX_MAX_USED_NO):
                if item.affix[_]:
                    _list.append(_)
            # move the affix whose def-value is 4 and 3 to front
            for _ in _list:
                if const.ITEMS_DATA[item.type]['affix_value'][_] == 3:
                    _list.remove(_)
                    _list = [_] + _list
            for _ in _list:
                if const.ITEMS_DATA[item.type]['affix_value'][_] == 4:
                    _list.remove(_)
                    _list = [_] + _list
            labels['item_main_affix'].element.text = const.ITEM_AFFIX_CNAME[_list[0]] + ' ' + str(item.affix[_list[0]])
            _str = ''
            for _ in range(1, len(_list)):
                _str +=  (const.ITEM_AFFIX_CNAME[_list[_]] + ' ' + str(item.affix[_list[_]]) + '\n')
            labels['item_affix'].element.text = _str

            #print(item.name, item.level, const.RARE_TYPE_NAME[item.rare_type], const.MAIN_TYPE_NAME[item.main_type])
            
            #for _ in range(const.AFFIX_MAX_USED_NO):
            #    if item.affix[_]:
            #        print(const.ITEM_AFFIX_CNAME[_], item.affix[_])

        if player_item:

            sprites['player_item'].visible = True
            sprites['player_item'].scale = 0.6
            sprites['player_item'].image = materials.item_image[(59-player_item.type) * 5 + player_item.rare_type]
            sprites['single_equiped_item_box'].visible = True

            labels['player_item_name'].element.text = player_item.name
            labels['player_item_type'].element.text = 'Lv ' + str(player_item.level) + '\n' + const.RARE_TYPE_NAME[player_item.rare_type] + ' ' + const.MAIN_TYPE_NAME[player_item.main_type]
            labels['player_item_name'].visible = True
            labels['player_item_type'].visible = True
            labels['player_item_main_affix'].visible = True
            labels['player_item_affix'].visible = True
            _list = []
            for _ in range(const.AFFIX_MAX_USED_NO):
                if player_item.affix[_]:
                    _list.append(_)
            # move the affix whose def-value is 4 and 3 to front
            for _ in _list:
                if const.ITEMS_DATA[player_item.type]['affix_value'][_] == 3:
                    _list.remove(_)
                    _list = [_] + _list
            for _ in _list:
                if const.ITEMS_DATA[player_item.type]['affix_value'][_] == 4:
                    _list.remove(_)
                    _list = [_] + _list
            labels['player_item_main_affix'].element.text = const.ITEM_AFFIX_CNAME[_list[0]] + ' ' + str(player_item.affix[_list[0]])
            _str = ''
            for _ in range(1, len(_list)):
                _str +=  (const.ITEM_AFFIX_CNAME[_list[_]] + ' ' + str(player_item.affix[_list[_]]) + '\n')
            labels['player_item_affix'].element.text = _str
            

    def hide_item(self):
        sprites['single_item_box'].visible = False
        sprites['single_equiped_item_box'].visible = False
        sprites['item'].visible = False
        sprites['player_item'].visible = False
        labels['item_name'].visible = False
        labels['item_type'].visible = False
        labels['item_main_affix'].visible = False
        labels['item_affix'].visible = False
        labels['player_item_name'].visible = False
        labels['player_item_type'].visible = False
        labels['player_item_main_affix'].visible = False
        labels['player_item_affix'].visible = False

    def show_player_value(self):
        _value_string = ''
        _value_string += str(int(self.game.player.value['Atk'])) + ' '
        _value_string += str(int(self.game.player.value['Def'])) + ' '
        _value_string += str(int(self.game.player.value['Luc'])) + ' '
        _value_string += str(int(self.game.player.value['Vit'])) + ' '
        _value_string += str(int(self.game.player.value['CriDmg'])) + ' '
        _value_string += str(int(self.game.player.value['BlockValue'])) + '%' + ' '
        _value_string += str(int(self.game.player.value['ShortDistanceAtkDecreaseRate'])) + '%' + ' '
        _value_string += str(int(self.game.player.value['BrambleDmg'])) + ' '
        _value_string += str(int(self.game.player.value['HpBonusRate'])) + '%' + ' '
        _value_string += str(int(self.game.player.value['HpRegen'])) + ' '
        _value_string += str(int(self.game.player.value['HpAbsorb'])) + '%' + ' '
        _value_string += str(int(self.game.player.value['HpHit'])) + ' '
        _value_string += str(int(self.game.player.value['MagicFind'])) + ' '
        _value_string += str(int(self.game.player.value['GoldFind'])) + ' '
        _value_string += str(int(self.game.player.value['ExpBonus'])) + '%' + ' '
        _value_string += str(int(self.game.player.value['ExpWhenKill'])) + ' '
        _value_string += str(int(self.game.player.value['MaxDice'])) + ' '
        _value_string += str(int(self.game.player.value['MinDice'])) + ' '
        _value_string += str(int(self.game.player.value['DebuffRoundMinus'])) + ' '
        _value_string += str(int(self.game.player.value['EliteDamage'])) + '%' + ' '
        labels['player_value_label'].element.text = _value_string

    def show_player_item(self):
        for _ in range(13):
            if self.game.player.item_equiped[_]:
                sprites['equiped_item' + str(_)].visible = True
                sprites['equiped_item' + str(_)].scale = 0.5
                sprites['equiped_item' + str(_)].image = materials.item_image[(59-self.game.player.item_equiped[_].type) * 5 + self.game.player.item_equiped[_].rare_type]
            else:
                sprites['equiped_item' + str(_)].visible = False

        


    def on_key_release(self, key, modifiers):
        # release the key_pressed set
        # be careful that the layer changing when key is be pressed (but not released)
        if self.keys_pressed and key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def draw(self):
        self.image.blit(0, 0)

    def skill_select(self, _player=None, n=None):
        if n is None:
            sprites['skill_select'].visible = False
            labels['skill_description_label'].element.text = ''
        elif n <=3:
            sprites['skill_select'].x = 45 + 45 * n
            sprites['skill_select'].visible = True
            if _player.skill[n]:
                labels['skill_description_label'].element.text = const.SKILL_DATA[_player.skill[n].skill_no]['description']
            else:
                labels['skill_description_label'].element.text = ''

    def skill_choose(self, n=None):
        if n is None:
            sprites['skill_choose'].visible = False
            if self.game.player.skill and self.game.player.skill[self.skill_selected]:
                labels['skill_description_label'].element.text = const.SKILL_DATA[self.game.player.skill[self.skill_selected].skill_no]['description']
        elif n <=14:
            sprites['skill_choose'].x = 48 + 66 * (n % 3)
            sprites['skill_choose'].y = 379 - 45 * (n // 3)
            sprites['skill_choose'].visible = True
            labels['skill_description_label'].element.text = const.SKILL_DATA[n]['description']

    def equiped_item_select(self, _player=None, n=None):
        if n is None:
            sprites['equiped_item_select'].visible = False
        elif n <= 12:
            _start_x = 455
            _start_y = 527
            # main hand
            if n == 0:
                _tx = _start_x - 65
                _ty = _start_y - 291
            # off hand
            elif n == 1:
                _tx = _start_x + 63
                _ty = _start_y - 291
            # head
            elif n == 2:
                _tx = _start_x
                _ty = _start_y
            # shoulder
            elif n == 3:
                _tx = _start_x - 47
                _ty = _start_y - 50
            # necklace
            elif n == 4:
                _tx = _start_x + 53
                _ty = _start_y - 23
            #chest
            elif n == 5:
                _tx = _start_x
                _ty = _start_y - 68
            # wrist
            elif n == 6:
                _tx = _start_x + 53
                _ty = _start_y - 105
            # gloove
            elif n == 7:
                _tx = _start_x - 65
                _ty = _start_y - 145
            # waist    
            elif n == 8:
                _tx = _start_x
                _ty = _start_y - 140
            # leg
            elif n == 9:
                _tx = _start_x + 17
                _ty = _start_y - 215
            # shoe
            elif n == 10:
                _tx = _start_x - 24
                _ty = _start_y - 265
            # ringA
            elif n == 11:
                _tx = _start_x - 64
                _ty = _start_y - 215
            # ringB
            elif n == 12:
                _tx = _start_x + 63
                _ty = _start_y - 215
            
            sprites['equiped_item_select'].x = _tx
            sprites['equiped_item_select'].y = _ty
            sprites['equiped_item_select'].visible = True

        self.show_item(None, self.game.player.item_equiped[self.item_equiped_selected])


