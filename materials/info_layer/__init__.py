#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/28 17:03:36
"""The info layer definition file
"""
import os
from data import const, skill
import pyglet
import cocos
from cocos.layer import Layer, ScrollingManager, ScrollableLayer
import materials


images = {}

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


skill_select_image = pyglet.image.load(os.path.abspath(const.SKILL_SELECT_IMG_FILE)) 

sprites = {}

sprites['skill_select'] = cocos.sprite.Sprite(skill_select_image, position=(45, 520))
sprites['skill_choose'] = cocos.sprite.Sprite(skill_select_image, position=(45, 400))
#bg_music = materials.Audio(Const.BG_MUSIC_FILE)

class Info_Layer(Layer):
    """the player information screen
    """

    is_event_handler = True

    def __init__(self, game):
        super(Info_Layer, self).__init__()

        self.keys_pressed = set()
        
        if hasattr(materials.info_layer, 'labels'):
            for _, _label in materials.info_layer.labels.items():
                self.add(_label)
        self.add(materials.front_layer.labels['level_label'])
        self.add(materials.front_layer.labels['gold_label'])
        self.add(materials.front_layer.labels['hp_label'])
        self.add(materials.front_layer.labels['exp_label'])
        self.add(materials.front_layer.labels['player_skill_label'])

        if hasattr(materials.info_layer, 'sprites'):
            for _, _sprite in materials.info_layer.sprites.items():
                self.add(_sprite)
                _sprite.visible = False

        materials.info_layer.sprites['skill_select'].scale = 0.4
        materials.info_layer.sprites['skill_choose'].scale = 0.4

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
            materials.info_layer.skill_select()
            materials.info_layer.skill_choose()
            self.status == 'view'
            self.game.show_game()

        if self.status == 'view':

            if 'ENTER' in key_names:
                pass
            elif 'UP' in key_names:
                pass
            elif 'DOWN' in key_names:
                pass
            # set skill
            elif 'S' in key_names and self.game.game_status == 'END':
                self.skill_selected = 0
                materials.info_layer.skill_select(self.game.player, 0)
                self.status = 'skill'

        elif self.status == 'skill':
            # you get n skills when your level is:
            # n=1, lv 1-9
            # n=2, lv 10-20
            # n=3, lv 21-40
            # n=4, lv 41-60
            _skill_no = 0
            _lv = self.game.player.level
            if _lv < 10:
                _skill_no = 1
            elif 10 <= _lv <= 20:
                _skill_no = 2
            elif 21 <= _lv <=40:
                _skill_no = 3
            elif 41 <= _lv:
                _skill_no = 4
            if 'LEFT' in key_names:
                if self.skill_selected > 0:
                    self.skill_selected -= 1
                else:
                    self.skill_selected = _skill_no -1
                materials.info_layer.skill_select(self.game.player, self.skill_selected)
            elif 'RIGHT' in key_names:
                if self.skill_selected < _skill_no -1:
                    self.skill_selected += 1
                else:
                    self.skill_selected = 0
                materials.info_layer.skill_select(self.game.player, self.skill_selected)
            elif 'UP' in key_names or 'SPACE' in key_names:
                materials.info_layer.skill_select()
                self.status = 'view'
            elif 'DOWN' in key_names or 'ENTER' in key_names:
                self.status = 'skill_choose'
                self.skill_chosen = 0
                materials.info_layer.skill_choose(0)
        elif self.status == 'skill_choose':
            if 'LEFT' in key_names:
                if self.skill_chosen > 0:
                    self.skill_chosen -= 1
                else:
                    self.skill_chosen = 14
                materials.info_layer.skill_choose(self.skill_chosen)
            elif 'RIGHT' in key_names:
                if self.skill_chosen < 14:
                    self.skill_chosen += 1
                else:
                    self.skill_chosen = 0
                materials.info_layer.skill_choose(self.skill_chosen)
            elif 'UP' in key_names:
                if self.skill_chosen > 2:
                    self.skill_chosen -= 3
                else:
                    self.skill_chosen += 12
                materials.info_layer.skill_choose(self.skill_chosen)
            elif 'DOWN' in key_names:
                if self.skill_chosen < 12:
                    self.skill_chosen += 3
                else:
                    self.skill_chosen -= 12
                materials.info_layer.skill_choose(self.skill_chosen)
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
                    if _.skill_no == self.skill_chosen:
                        _skill = None
                        break

                if _skill:
                    self.game.player.skill[self.skill_selected] = _skill
                    materials.info_layer.skill_choose()
                    materials.info_layer.skill_select(self.game.player, self.skill_selected)
                    self.status = 'skill'
                    self.game.refresh_info()

            elif 'SPACE' in key_names:
                materials.info_layer.skill_choose()
                self.status = 'skill'




    def on_key_release(self, key, modifiers):
        # release the key_pressed set
        # be careful that the layer changing when key is be pressed (but not released)
        if self.keys_pressed and key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def draw(self):
        self.image.blit(0, 0)

def skill_select(_player=None, n=None):
    if n is None:
        sprites['skill_select'].visible = False
    elif n <=3:
        sprites['skill_select'].x = 45 + 45 * n
        sprites['skill_select'].visible = True
        labels['skill_description_label'].element.text = const.SKILL_DATA[_player.skill[n].skill_no]['description']

def skill_choose(n=None):
    if n is None:
        sprites['skill_choose'].visible = False
    elif n <=14:
        sprites['skill_choose'].x = 48 + 66 * (n % 3)
        sprites['skill_choose'].y = 379 - 45 * (n // 3)
        sprites['skill_choose'].visible = True
        labels['skill_description_label'].element.text = const.SKILL_DATA[n]['description']
