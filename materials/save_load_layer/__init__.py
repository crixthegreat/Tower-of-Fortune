#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/28 17:03:36
"""The save & load layer definition file
"""
import sys
import os
import copy
import json
from data import const, skill, item, player
import pyglet
import cocos
from cocos.layer import Layer, ScrollingManager, ScrollableLayer
import materials


images = {}

save_load_bg_image = pyglet.image.load(os.path.abspath(const.SAVE_LOAD_BG_IMG_FILE)) 
select_bar_image = pyglet.image.load(os.path.abspath(const.SELECT_BAR_IMG_FILE)) 
"""
time_label & best_time_label : as the name says
"""

labels = {}
sprites = {}

sprites['select_bar'] = cocos.sprite.Sprite(select_bar_image, position=(150, 425))

for _ in range(9):
    sprites['player_sprite' + str(_)] = cocos.sprite.Sprite(materials.main_scr.player_image, position=(150+ _* 20, 425))
    sprites['player_sprite' + str(_)].scale = 0.3

    """
    labels['player_item_affix'] = cocos.text.Label('',font_size=9,
            font_name = 'Gadugi',
            bold=False,
            color=const.DEFAULT_COLOR, 
            x=648, y=480, width=200, multiline=True)
    """

"""
# sprites of equiped items
for n in range(13):
    sprites['equiped_item' + str(n)] = cocos.sprite.Sprite(materials.item_image[0], position=(0,0))
#bg_music = materials.Audio(Const.BG_MUSIC_FILE)
"""

class Save_Load_Layer(Layer):
    """the player information screen
    """

    is_event_handler = True

    def __init__(self, game):
        super(Save_Load_Layer, self).__init__()

        self.keys_pressed = set()


        if hasattr(materials.save_load_layer, 'sprites'):
            for _, _sprite in materials.save_load_layer.sprites.items():
                self.add(_sprite)
                #_sprite.visible = False

        if hasattr(materials.save_load_layer, 'labels'):
            for _, _label in materials.save_load_layer.labels.items():
                self.add(_label)
                _label.visible = False


        self.game = game
        self.image = save_load_bg_image
        self.status = 'view'
        self.slot_selected = 0


        #self.save_data = self.load_save_slot()

    def on_key_press(self, key, modifiers):
        """key press handler for info class
        """
        self.keys_pressed.add(key)
        key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]
        
        if 'SPACE' in key_names:
            pass

        if self.status == 'view':
            # confirm the selected slot to:
            # - continue with the saved game if the player is not dead
            if 'ENTER' in key_names:
                # load a game
                if ('slot' + str(self.slot_selected)) in self.save_data:
                    if self.save_data['slot' + str(self.slot_selected)]['alive']:
                        self.game.player = self.game.load(self.slot_selected)
                        self.game.player.show_player()
                        self.game.start_game()
                    else:
                        print('the player is dead')
                        sys.exit()
                else:
                    # start a new game
                    self.game.player = player.gen_player(1)
                    self.game.player.save_slot =  self.slot_selected
                    self.game.player.show_player()
                    self.game.player.zone = 1
                    self.game.start_game()
            elif 'UP' in key_names:
                self.slot_selected -= 3
                if self.slot_selected < 0:
                    self.slot_selected += 8
                self.slot_select()
            elif 'DOWN' in key_names:
                self.slot_selected += 3
                if self.slot_selected > 8:
                    self.slot_selected -= 9
                self.slot_select()
            elif 'LEFT' in key_names:
                self.slot_selected -= 1
                if self.slot_selected < 0:
                    self.slot_selected = 8
                self.slot_select()
            elif 'RIGHT' in key_names:
                self.slot_selected += 1
                if self.slot_selected > 8:
                    self.slot_selected = 0
                self.slot_select()


    def on_key_release(self, key, modifiers):
        # release the key_pressed set
        # be careful that the layer changing when key is be pressed (but not released)
        if self.keys_pressed and key in self.keys_pressed:
            self.keys_pressed.remove(key)

    # when the image has not been defined , there is no need to use this method
    def draw(self):
        self.image.blit(0, 0)

    # load the save files to show the 9 save slot
    # display the grave stone or the player sprites and some informations
    def load_save_slot(self):
        # load the exist player data
        if os.path.isfile(const.SAVE_FILE):
            with open(const.SAVE_FILE) as _file:
                #try:
                    # return save_data
                self.save_data = json.load(_file)
                #except:
                    #print('open file failed')

    # locate the select bar
    def slot_select(self):
        # - show the equiped item icons when a save slot is selected
        print(self.slot_selected, 'is selected')
        #sprites['select_bar'].position = 0, 0



