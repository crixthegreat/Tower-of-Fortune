#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/28 17:03:36
"""The info layer definition file
"""
import copy
from data import const, skill, item
import pyglet
import cocos
from cocos.layer import Layer
import materials


images = {}

single_item_box_image = const.image_from_file(
        const.SINGLE_ITEM_BOX_IMG_FILE, const.GUI_ZIP_FILE) 
single_equiped_item_box_image = const.image_from_file(
        const.SINGLE_EQUIPED_ITEM_BOX_IMG_FILE, const.GUI_ZIP_FILE) 

labels = {}

labels['skill_description_label'] = cocos.text.Label('', 
        font_size=10,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, 
        x=35, y=435, width = 10, multiline=True)
labels['player_value_label'] = cocos.text.Label('', 
        font_size=12.5,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, 
        x=295, y=562, width = 10, multiline=True)
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


skill_select_image = const.image_from_file(
        const.SKILL_SELECT_IMG_FILE, const.GUI_ZIP_FILE) 
item_select_image =  const.image_from_file(
        const.ITEM_SELECT_IMG_FILE, const.GUI_ZIP_FILE) 

sprites = {}

sprites['skill_select'] = cocos.sprite.Sprite(
        skill_select_image, position=(45, 520))
sprites['skill_choose'] = cocos.sprite.Sprite(
        skill_select_image, position=(45, 400))
sprites['single_item_box'] = cocos.sprite.Sprite(
        single_item_box_image, position=(670, 260))
sprites['single_item_box'].scale = 0.45
sprites['single_equiped_item_box'] = cocos.sprite.Sprite(
        single_equiped_item_box_image, position=(670, 485))
sprites['single_equiped_item_box'].scale = 0.45
sprites['item'] = cocos.sprite.Sprite(
        materials.item_image[0], position = (620,285))
sprites['item'].scale = 0.6
sprites['player_item'] = cocos.sprite.Sprite(
        materials.item_image[0], position = (620,515))
sprites['player_item'].scale = 0.6

# sprites of equiped items
_start_x = 455
_start_y = 527
_pos_offset = {
        # main hand
        0:(-66, -291),
        # off hand
        1:(63, -291),
        # head
        2:(0, 0),
        # shoulder
        3:(-50, -50),
        # necklace
        4:(53, -23),
        #chest
        5:(0, -68),
        # wrist
        6:(53, -105),
        # gloove
        7:(-66, -145),
        # waist    
        8:(0, -140),
        # leg
        9:(17, -215),
        # shoe
        10:(-26, -265),
        # ringA
        11:(-64, -215),
        # ringB
        12:(63, -215)}

for n in range(13):
    sprites['equiped_item' + str(n)] = cocos.sprite.Sprite(
            materials.item_image[0], position=(0,0))
    sprites['equiped_item' + str(n)].position = (
            _start_x + _pos_offset[n][0],
            _start_y + _pos_offset[n][1])

# sprites of current page of the item box
for _ in range(13):
    sprites['item_box' + str(_)] = cocos.sprite.Sprite(
            materials.item_image[0], position=(47 + 59 * _, 79))
    sprites['item_box' + str(_)].scale = 0.6


sprites['equiped_item_select'] = cocos.sprite.Sprite(
        item_select_image, position=(350, 400))
sprites['item_box_select'] = cocos.sprite.Sprite(
        item_select_image, position=(46, 80))
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
        
        # map the keys to methods of every status
        # the keys in GLOBAL status take effects always
        self.key_events = {
                "GLOBAL":{
                    ("I",):self.return_to_game},
                "view":{
                    ("E",):self.check_equipment, 
                    ("S",):self.check_skill, 
                    ("B",):self.check_item_box},
                "item_box":{
                    ("LEFT","RIGHT","UP","DOWN"):self.move_item_box_cursor,
                    ("S",):self.sell_item,
                    ("SPACE",):self.close_item_box,
                    ("ENTER",):self.equip_item},
                "equiped_item_select":{
                    ("LEFT","RIGHT"):self.equiped_item_select_cursor,
                    ("SPACE",):self.equiped_item_unselect},
                "skill":{
                    ("LEFT","RIGHT"):self.skill_slot_select,
                    ("UP","SPACE"):self.skill_slot_unselect,
                    ("DOWN","ENTER"):self.skill_slot_selected
                    },
                "skill_choose":{
                    ("LEFT","RIGHT","UP","DOWN"):self.move_skill_cursor,
                    ("SPACE",):self.skill_unselect,
                    ("ENTER",):self.skill_set
                    }
                }

    def skill_set(self):
        #set the selected skill to the selected skill slot
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


    def skill_unselect(self):
        # quit the skill selection
        self.skill_choose()
        self.status = 'skill'

    def move_skill_cursor(self, _direc):
        if _direc == 'LEFT':
            if self.skill_chosen > 0:
                self.skill_chosen -= 1
            else:
                self.skill_chosen = 14
        elif _direc == 'RIGHT':
            if self.skill_chosen < 14:
                self.skill_chosen += 1
            else:
                self.skill_chosen = 0
        elif _direc == 'UP':
            if self.skill_chosen > 2:
                self.skill_chosen -= 3
            else:
                self.skill_chosen += 12
        elif _direc == 'DOWN':
            if self.skill_chosen < 12:
                self.skill_chosen += 3
            else:
                self.skill_chosen -= 12
        else:
            raise ValueError('wrong direction when move the skill cursor')
        self.skill_choose(self.skill_chosen)

    def skill_slot_selected(self):
        # enter the skill selection
        self.status = 'skill_choose'
        self.skill_chosen = 0
        self.skill_choose(0)

    def skill_slot_unselect(self):
        # exit the skill slot
        self.skill_select()
        self.status = 'view'

    def skill_slot_select(self, _direc):
        _skill_no = self.game.player.skill_quantity
        if _direc == 'LEFT':
            if self.skill_selected > 0:
                self.skill_selected -= 1
            else:
                self.skill_selected = _skill_no -1
        elif _direc == 'RIGHT':
            if self.skill_selected < _skill_no -1:
                self.skill_selected += 1
            else:
                self.skill_selected = 0
        else:
            raise ValueError('wrong direction when move skill slot cursor')
        self.skill_select(self.game.player, self.skill_selected)

    def equiped_item_unselect(self):
        # exit the equiped item check
        self.equiped_item_select()
        self.hide_item()
        self.status = 'view'

    def equiped_item_select_cursor(self, _direc):

        if _direc == 'LEFT':
            if self.item_equiped_selected > 0:
                self.item_equiped_selected -= 1
                self.equiped_item_select(
                        self.game.player, self.item_equiped_selected)
            else:
                self.item_equiped_selected = 12
                self.equiped_item_select(
                        self.game.player, self.item_equiped_selected)
        elif _direc == 'RIGHT':
            if self.item_equiped_selected < 12:
                self.item_equiped_selected += 1
                self.equiped_item_select(
                        self.game.player, self.item_equiped_selected)
            else:
                self.item_equiped_selected = 0
                self.equiped_item_select(
                        self.game.player, self.item_equiped_selected)
        else:
            raise ValueError(
                    'wrong direction when move the equiped item cursor')


    def equip_item(self):
        """Equip item from the item box
        """
        self.game.player.equip_item(
                self.game.player.item_box.pop(self.item_box_selected))
        self.show_item_box()
        self.show_player_item()
        self.item_box_select()
        self.show_player_value()
        if self.game.player.hp > self.game.player.max_hp:
            self.game.player.hp = self.game.player.max_hp
        self.game.player.show_player()
        self.game.save()
                
    def close_item_box(self):
        self.item_box_select(clear=True)
        self.hide_item()
        self.status = 'view'

    def sell_item(self):
        """Sell the item in the item box
        """
        self.game.player.sell_item(
                self.game.player.item_box.pop(self.item_box_selected))
        if self.game.player.item_box:
            if self.item_box_selected >= len(self.game.player.item_box):
                self.item_box_selected = len(self.game.player.item_box) - 1
            self.item_box_select()
        # if sold out
        else:
            self.item_box_select('clear')
        self.show_item_box()
        self.game.save()


    def return_to_game(self):
        """close the info layer
        """
        self.skill_choose()
        self.skill_select()
        self.equiped_item_select()
        self.item_box_select('clear')
        self.status == 'view'
        self.game.show_game()
        self.game.save()
        
    def check_equipment(self):
        self.item_equiped_selected = 0
        self.status = 'equiped_item_select'
        self.equiped_item_select(self.game.player, 0)

    def check_skill(self):
        if self.game.game_status != 'END':
            return None
        self.skill_selected = 0
        self.skill_select(self.game.player, 0)
        self.status = 'skill'

    def check_item_box(self):
        if self.game.game_status != 'END' or (not(self.game.player.item_box)):
            return None
        self.status = 'item_box'
        self.item_box_selected = 0
        self.item_box_select()

    def move_item_box_cursor(self, _direc):
        if _direc == 'UP':
            if self.item_box_selected > 12:
                self.item_box_selected -= 12
            elif len(self.game.player.item_box) > 13:
                self.item_box_selected = (
                        (len(self.game.player.item_box) - 1) // 13 * 13)
            self.show_item_box()
        elif _direc == 'DOWN':
            # the _pos is the first position of next page
            _pos = self.item_box_selected // 13 * 13 + 13
            if _pos <= len(self.game.player.item_box) - 1:
                self.item_box_selected = _pos
            else:
                self.item_box_selected = 0
            self.show_item_box()
        elif _direc == 'LEFT':
            _pos = self.item_box_selected % 13
            if _pos > 0:
                self.item_box_selected -= 1
            else:
                _pos = self.item_box_selected // 13 * 13 + 12
                if _pos > (len(self.game.player.item_box) - 1):
                    self.item_box_selected = len(self.game.player.item_box) - 1
                else:
                    self.item_box_selected = _pos
        elif _direc == 'RIGHT':
            if (self.item_box_selected >= len(self.game.player.item_box) - 1 
                    or (self.item_box_selected % 13) == 12):
                self.item_box_selected = self.item_box_selected // 13 * 13
            else:
                self.item_box_selected += 1
        self.item_box_select()



    def on_key_press(self, key, modifiers):
        """key press handler for info class
        """
        self.keys_pressed.add(key)
        key_names = [
                pyglet.window.key.symbol_string(k) for k in self.keys_pressed]
        
        # firstly do the GLOBAL key events
        materials.do_key_events(self, 'GLOBAL', key_names)
        # then do the key events of current status
        materials.do_key_events(self, self.status, key_names)

    def show_item_box(self):
        if self.game.player.item_box:
            _page = self.item_box_selected // 13
            for _ in range(13):
                _item_no = _page * 13 + _
                if _item_no >= len(self.game.player.item_box):
                    sprites['item_box' + str(_)].visible = False
                else:
                    sprites['item_box' + str(_)].visible = True
                    sprites['item_box' + str(_)].image = materials.item_image[
                            self.game.player.item_box[_item_no].image_no]
            labels['item_box_page'].element.text = (
                    str((self.item_box_selected // 13) + 1) + '/' 
                    + str(len(self.game.player.item_box) // 13 + 1))
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
                _item = self.game.player.item_box[self.item_box_selected] 
                self.show_item(_item,
                        self.game.player.item_equiped[_item.equiped_pos])

    # show the item for the info_layer
    def show_item(self, item, player_item):

        if item:
            item.show(sprites['item'],
                    sprites['single_item_box'],
                    labels['item_name'],
                    labels['item_type'],
                    labels['item_main_affix'],
                    labels['item_affix'])

        if player_item:
            player_item.show(sprites['player_item'], 
                    sprites['single_equiped_item_box'],
                    labels['player_item_name'],
                    labels['player_item_type'],
                    labels['player_item_main_affix'],
                    labels['player_item_affix'])
            

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
        _value = self.game.player.value
        _value_string = ''
        _value_string += str(int(_value['Atk'])) + ' '
        _value_string += str(int(_value['Def'])) + ' '
        _value_string += str(int(_value['Luc'])) + ' '
        _value_string += str(int(_value['Vit'])) + ' '
        _value_string += str(int(_value['CriDmg'])) + ' '
        _value_string += str(int(_value['BlockValue'])) + '%' + ' '
        _value_string += (
                str(int(_value['ShortDistanceAtkDecreaseRate'])) + '%' + ' ')
        _value_string += str(int(_value['BrambleDmg'])) + ' '
        _value_string += str(int(_value['HpBonusRate'])) + '%' + ' '
        _value_string += str(int(_value['HpRegen'])) + ' '
        _value_string += str(int(_value['HpAbsorb'])) + '%' + ' '
        _value_string += str(int(_value['HpHit'])) + ' '
        _value_string += str(int(_value['MagicFind'])) + ' '
        _value_string += str(int(_value['GoldFind'])) + ' '
        _value_string += str(int(_value['ExpBonus'])) + '%' + ' '
        _value_string += str(int(_value['ExpWhenKill'])) + ' '
        _value_string += str(int(_value['MaxDice'])) + ' '
        _value_string += str(int(_value['MinDice'])) + ' '
        _value_string += str(int(_value['DebuffRoundMinus'])) + ' '
        _value_string += str(int(_value['EliteDamage'])) + '%' + ' '
        labels['player_value_label'].element.text = _value_string

    def show_player_item(self):
        for _ in range(13):
            if self.game.player.item_equiped[_]:
                sprites['equiped_item' + str(_)].visible = True
                sprites['equiped_item' + str(_)].scale = 0.5
                sprites['equiped_item' + str(_)].image = materials.item_image[
                        self.game.player.item_equiped[_].image_no]
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
                labels['skill_description_label'].element.text = (
                        _player.skill[n].description)
            else:
                labels['skill_description_label'].element.text = ''

    def skill_choose(self, n=None):
        if n is None:
            sprites['skill_choose'].visible = False
            if self.game.player.skill and self.game.player.skill[self.skill_selected]:
                labels['skill_description_label'].element.text = (
                        self.game.player.skill[self.skill_selected].description)
        elif n <=14:
            sprites['skill_choose'].x = 48 + 66 * (n % 3)
            sprites['skill_choose'].y = 379 - 45 * (n // 3)
            sprites['skill_choose'].visible = True
            labels['skill_description_label'].element.text = (
                    const.SKILL_DATA[n]['description'])

    def equiped_item_select(self, _player=None, n=None):
        if n is None:
            sprites['equiped_item_select'].visible = False
        elif n <= 12:
            # sprites of equiped-items-selection-box
            _start_x = 455
            _start_y = 527
            _pos_offset = {
                    # main hand
                    0:(-65, -291),
                    # off hand
                    1:(63, -291),
                    # head
                    2:(0, 0),
                    # shoulder
                    3:(-47, -50),
                    # necklace
                    4:(53, -23),
                    #chest
                    5:(0, -68),
                    # wrist
                    6:(53, -105),
                    # gloove
                    7:(-65, -145),
                    # waist    
                    8:(0, -140),
                    # leg
                    9:(17, -215),
                    # shoe
                    10:(-24, -265),
                    # ringA
                    11:(-64, -215),
                    # ringB
                    12:(63, -215)}
            
            sprites['equiped_item_select'].position = (
                    _start_x + _pos_offset[n][0],
                    _start_y + _pos_offset[n][1])
            sprites['equiped_item_select'].visible = True

        self.show_item(None, 
                self.game.player.item_equiped[self.item_equiped_selected])


