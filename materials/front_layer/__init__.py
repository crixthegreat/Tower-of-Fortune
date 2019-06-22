#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/28 17:03:36
"""The front layer definition file
"""
import os
from data import const
import pyglet
import cocos
from cocos.layer import Layer, ScrollingManager, ScrollableLayer
import materials

images = {}

"""
time_label & best_time_label : as the name says
"""

labels = dict(old_msg_box=cocos.text.Label('old message', 
    font_size=12,font_name='Gadugi', 
    bold=False,color=const.DEFAULT_COLOR, x=530, y=100, width= 250, multiline=True), 
    msg_box=cocos.text.Label('message here', 
        font_size=14,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=530, y=10))

labels['zone_label'] = cocos.text.Label('',
        font_size=14,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=350, y=555, width=100, align='center')

labels['level_label'] = cocos.text.Label('',
        font_size=10,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=40, y=560)
labels['gold_label'] = cocos.text.Label('',
        font_size=10,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=40, y=545)
labels['hp_label'] = cocos.text.Label('', 
        font_size=10,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=115, y=565)
labels['exp_label'] = cocos.text.Label('Exp:', 
        font_size=10,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=115, y=545)
labels['player_skill_label'] = cocos.text.Label('', 
        font_size=10,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=30, y=515)

labels['enemy_name_label'] = cocos.text.Label('Name:', 
        font_size=10,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=610, y=560)
labels['enemy_level_label'] = cocos.text.Label('',
        font_size=14,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=640, y=540)
labels['enemy_hp_label'] = cocos.text.Label('', 
        font_size=10,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=700, y=540)
labels['enemy_skill_label'] = cocos.text.Label('', 
        font_size=10,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=620, y=515)

labels['player_hp_change_label'] = cocos.text.Label('', 
        font_size=12,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=200, y=220)
labels['enemy_hp_change_label'] = cocos.text.Label('', 
        font_size=12,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=500, y=220)

sprites = {}

#bg_music = materials.Audio(Const.BG_MUSIC_FILE)

class Front_Layer(Layer):
    def __init__(self):
        super(Front_Layer, self).__init__()
        if hasattr(materials.front_layer, 'labels'):
            for _, _label in materials.front_layer.labels.items():
                self.add(_label)
        
        self.image = materials.images['front_img']
    def draw(self):
        self.image.blit(0, 0)



def show_message(_msg, _type=None):
    _list = materials.front_layer.labels['old_msg_box'].element.text + '\n' + materials.front_layer.labels['msg_box'].element.text
    materials.front_layer.labels['msg_box'].element.text = _msg
    if _list.count('\n') >= 7:
        _list = _list[_list.find('\n') + 1:]
    materials.front_layer.labels['old_msg_box'].element.text = _list
