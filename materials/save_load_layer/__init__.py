#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/28 17:03:36
"""The save & load layer definition file
"""
import os
import json
from data import const, player
import pyglet
import cocos
from cocos.layer import Layer
import materials


images = {}

save_load_bg_image = const.image_from_file(
        const.SAVE_LOAD_BG_IMG_FILE, const.GUI_ZIP_FILE) 
select_bar_image = const.image_from_file(
        const.SELECT_BAR_IMG_FILE, const.GUI_ZIP_FILE) 
empty_image = const.image_from_file(
        const.EMPTY_IMG_FILE, const.GUI_ZIP_FILE) 
message_box_image = const.image_from_file(
        const.MESSAGE_BOX_IMG_FILE, const.GUI_ZIP_FILE) 

"""
time_label & best_time_label : as the name says
"""

labels = {}
sprites = {}

sprites['select_bar'] = cocos.sprite.Sprite(
        select_bar_image, position=(150, 425))

for _ in range(9):
    sprites['slot_sprite' + str(_)] = cocos.sprite.Sprite(
            materials.main_scr.player_image, 
            position=(60 + (_ % 3) * 270, 455 - (_ // 3) * 160))
    sprites['slot_sprite' + str(_)].scale = 0.25

    labels['level_label' + str(_)] = cocos.text.Label('N/A',font_size=12,
        font_name = 'Gadugi',
        bold=False,
        color=const.DEFAULT_COLOR, 
        x=130 + (_ % 3) * 270, y=455 - (_//3) * 155)
    labels['gold_label' + str(_)] = cocos.text.Label('N/A',font_size=12,
        font_name = 'Gadugi',
        bold=False,
        color=const.DEFAULT_COLOR, 
        x=180 + (_ % 3) * 270, y=455 - (_//3) * 155)
    labels['epitaph_label' + str(_)] = cocos.text.Label('N/A',font_size=8,
        font_name = 'Gadugi',
        bold=False,
        color=const.DEFAULT_COLOR, 
        x=130 + (_ % 3) * 270, y=430 - (_//3) * 155, width=150, multiline=True)

for _ in range(9):
    for __ in range(13):
        sprites['item' + str(_) + str(__)] = cocos.sprite.Sprite(
                materials.item_image[0], 
                position=(30 + (_ % 3) * 268 + __ * 17.2,395 - (_ // 3) * 156))
        sprites['item' + str(_) + str(__)].visible = False
        sprites['item' + str(_) + str(__)].scale =  0.20

sprites['message_box'] = cocos.sprite.Sprite(message_box_image, position=(0, 0))
sprites['message_box'].visible = False
labels['message_box'] = cocos.text.Label('N/A',font_size=10,
        font_name = 'Gadugi',
        bold=False,
        color=const.DEFAULT_COLOR, 
        x=0, y=0, width=220, multiline=True)

labels['message_box'].visible = False


class Save_Load_Layer(Layer):
    """the player information screen
    """

    is_event_handler = True

    def __init__(self, game):
        super(Save_Load_Layer, self).__init__()

        self.keys_pressed = set()
        self.game = game
        self.image = save_load_bg_image
        self.status = 'view'
        self.slot_selected = 0
    
        self.key_events = {
                'view':{
                    ('ENTER',):self.select_slot,
                    ('D',):self.try_to_delete_save,
                    ('UP','DOWN','LEFT','RIGHT'):self.move_save_slot_cursor},
                'message_box':{
                    ('ENTER',):self.confirm_message,
                    ('SPACE',):self.hide_message_box},
                'del_save':{
                    ('ENTER',):self.confirm_del_save,
                    ('SPACE',):self.hide_message_box}
                }
    
    # self.save_data stores all the saved game data(9 save slot)
    @property
    def save_data(self):
        # load the exist player data
        if os.path.isfile(const.SAVE_FILE):
            with open(const.SAVE_FILE) as _file:
                try:
                    # return save_data
                    return json.load(_file)
                except:
                    raise IOError(
                            'when loading save_data, failed to open the file')
        else:
            return None

    def confirm_message(self):
        # load a game
        if (self.save_data 
                and ('slot' + str(self.slot_selected)) in self.save_data):
            if self.save_data['slot' + str(self.slot_selected)]['alive']:
                self.game.player = self.game.load(self.slot_selected)
                self.game.player.show_player()
                self.exit_save_load_layer()
                self.game.start_game()
            else:
                #print('the player is dead')
                self.hide_message_box()
        else:
            # start a new game
            self.game.player = player.gen_player(5)
            self.game.player.save_slot =  self.slot_selected
            self.game.player.show_player()
            self.game.player.zone = 0
            self.exit_save_load_layer()
            self.game.start_game()

    def confirm_del_save(self):
        self.del_save(self.slot_selected)
        self.hide_message_box()


    def move_save_slot_cursor(self, key):
        if 'UP' == key:
            self.slot_selected -= 3
            if self.slot_selected < 0:
                self.slot_selected += 8
        elif 'DOWN' == key:
            self.slot_selected += 3
            if self.slot_selected > 8:
                self.slot_selected -= 9
        elif 'LEFT' == key:
            self.slot_selected -= 1
            if self.slot_selected < 0:
                self.slot_selected = 8
        elif 'RIGHT' == key:
            self.slot_selected += 1
            if self.slot_selected > 8:
                self.slot_selected = 0
        self.slot_select()


    def select_slot(self):
        # load a game
        if (self.save_data 
                and ('slot' + str(self.slot_selected)) in self.save_data):
            if self.save_data['slot' + str(self.slot_selected)]['alive']:
                self.show_message_box('Load this player to continue?')
            else:
                self.show_message_box(
                        'This player is dead, loot the body in the game.')
        else:
            # start a new game
            self.show_message_box('Start a new game with this save slot?')
        return 1

    def try_to_delete_save(self):
        # if the save_slot is not empty
        if (self.save_data 
                and ('slot' + str(self.slot_selected)) in self.save_data):
            self.show_message_box('DELETE this SAVE DATA?')
            self.status = 'del_save'


    def on_key_press(self, key, modifiers):
        """key press handler for info class
        """
        self.keys_pressed.add(key)
        key_names = [
                pyglet.window.key.symbol_string(k) for k in self.keys_pressed]

        materials.do_key_events(self, 'GLOBAL', key_names)
        materials.do_key_events(self, self.status, key_names)
        

    def on_key_release(self, key, modifiers):
        # release the key_pressed set
        # be careful that the layer changing when key is be pressed (but not released)
        if self.keys_pressed and key in self.keys_pressed:
            self.keys_pressed.remove(key)

    # when the image has not been defined , there is no need to use this method
    def draw(self):
        self.image.blit(0, 0)

    # display the grave stone or the player sprites and some informations
    def show_save_slot(self):
        if hasattr(materials.save_load_layer, 'sprites'):
            for _, _sprite in materials.save_load_layer.sprites.items():
                self.add(_sprite)
        if hasattr(materials.save_load_layer, 'labels'):
            for _, _label in materials.save_load_layer.labels.items():
                self.add(_label)
        self.slot_select()

        _data = self.save_data
        for _ in range(9):
            # show the slot that has game data
            if _data and ('slot' + str(_)) in _data:
                # show level hp and gold
                labels['level_label' + str(_)].element.text = str(
                        _data['slot' + str(_)]['player_level'])
                labels['gold_label' + str(_)].element.text = str(
                        int(_data['slot' + str(_)]['gold']))
                if _data['slot' + str(_)]['alive']:
                    sprites['slot_sprite' + str(_)].image = (
                            materials.main_scr.player_image)
                else:
                    sprites['slot_sprite' + str(_)].image = (
                            materials.main_scr.images['rip'])
                    labels['epitaph_label' + str(_)].element.text = (
                            _data['slot' + str(_)]['epitaph'])
                
                # show items equiped
                for __ in range(13):
                    _item_data = _data['slot' + str(_)]['item_equiped'][__]
                    if _item_data:
                        _image_no = ((59 - _item_data['item_type']) * 5 + 
                                _item_data['rare_type'])
                        sprites['item' + str(_) + str(__)].image = (
                                materials.item_image[_image_no])
                        sprites['item' + str(_) + str(__)].visible = True
            else:
                # to do:
                # when the body have been bought in game
                # the labels and item sprites shoud be invisible
                sprites['slot_sprite' + str(_)].image = empty_image
                
    def exit_save_load_layer(self):
        if hasattr(materials.save_load_layer, 'sprites'):
            for _, _sprite in materials.save_load_layer.sprites.items():
                self.remove(_sprite)
        if hasattr(materials.save_load_layer, 'labels'):
            for _, _label in materials.save_load_layer.labels.items():
                self.remove(_label)

    # locate the select bar
    def slot_select(self):
        # - show the equiped item icons when a save slot is selected
        _no = self.slot_selected
        sprites['select_bar'].visible = True
        sprites['select_bar'].position = (
                130 + (_no % 3) * 270 , 350 - 155 * (_no // 3))

    def show_message_box(self, message='N/A', x=200, y=200):
        #position=(60 + (_ % 3) * 270, 455 - (_ // 3) * 160))
        _ = self.slot_selected
        _x = 130 + (_ % 3) * 270
        _y = 350 - (_ // 3) * 160
        sprites['message_box'].visible = True
        sprites['message_box'].position = _x, _y
        labels['message_box'].visible = True
        labels['message_box'].element.text = message
        labels['message_box'].position = _x - 110, _y + 5 
        self.status = 'message_box'

    def hide_message_box(self):
        sprites['message_box'].visible = False
        labels['message_box'].visible = False
        self.status = 'view'

    def del_save(self, save_slot):
        _data = self.save_data
        if 'slot' + str(save_slot) in _data:
            del _data['slot' + str(save_slot)]
            with open(const.SAVE_FILE, 'w') as _file:
                try:
                    json.dump(_data, _file)
                except:
                    raise IOError('failed to write-file when deleting a slot')
                sprites['slot_sprite' + str(save_slot)].image = empty_image
                labels['level_label' + str(save_slot)].element.text = 'N/A'
                labels['gold_label' + str(save_slot)].element.text = 'N/A'
                labels['epitaph_label' + str(save_slot)].element.text = 'N/A'
                for __ in range(13):
                    sprites['item' + str(save_slot) + str(__)].visible = False
        else:
            raise IOError('del save error, no such save data in the save file')



