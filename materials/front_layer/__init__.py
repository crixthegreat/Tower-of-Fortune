#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/28 17:03:36
"""The front layer definition file
"""
import os
import zipfile
from data import const
import pyglet
import cocos
from cocos.layer import Layer, ScrollingManager, ScrollableLayer
import materials

images = {}

"""
time_label & best_time_label : as the name says
"""

labels = dict(msg_box=cocos.text.Label('message', 
    font_size=12,font_name='Gadugi', 
    bold=False,color=const.DEFAULT_COLOR, x=550, y=105, width= 200, multiline=True)) 

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
        font_size=11,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=610, y=580, width=150, multiline=True)
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
        bold=True,color=const.DEFAULT_COLOR, x=200, y=220)
labels['enemy_hp_change_label'] = cocos.text.Label('', 
        font_size=12,font_name='Gadugi', 
        bold=True,color=const.DEFAULT_COLOR, x=500, y=220)

sprites = {}
_file_name = 'number-'
with zipfile.ZipFile(const.MONSTER_ZIP_FILE) as monster_file:
    for _ in range(6):
        monster_file_data = monster_file.open(_file_name + str(_ + 1) + '.png')
        _number_file_image =  pyglet.image.load('', file=monster_file_data) 
        sprites['number' + str(_+ 1)] = cocos.sprite.Sprite(_number_file_image, position =(10,10))
sprites['number1'].scale = 0.35
sprites['number2'].scale = 0.35
sprites['number3'].scale = 0.35
sprites['number4'].scale = 0.35
sprites['number5'].scale = 0.35
sprites['number6'].scale = 0.35

sprites['number1'].position = 160, 100
sprites['number2'].position = 50, 150
sprites['number3'].position = 25, 75
sprites['number4'].position = 100, 60
sprites['number5'].position = 140, 160
sprites['number6'].position = 200, 160

sprites['number1'].visible = False
sprites['number2'].visible = False
sprites['number3'].visible = False
sprites['number4'].visible = False
sprites['number5'].visible = False
sprites['number6'].visible = False


_anime = pyglet.image.load_animation(const.MAP_SELECT_IMG_FILE)
_bin = pyglet.image.atlas.TextureBin()
_anime.add_to_texture_bin(_bin)
sprites['map_select'] = cocos.sprite.Sprite(_anime, position=(30,30))
sprites['map_select'].scale = 0.35

#bg_music = materials.Audio(Const.BG_MUSIC_FILE)

class Front_Layer(Layer):
    def __init__(self):
        super(Front_Layer, self).__init__()
        if hasattr(materials.front_layer, 'labels'):
            for _, _label in materials.front_layer.labels.items():
                self.add(_label)
        if hasattr(materials.front_layer, 'sprites'):
            for _, _sprite in materials.front_layer.sprites.items():
                self.add(_sprite)
        
        self.image = materials.images['front_img']
    def draw(self):
        self.image.blit(0, 5)



def show_message(_msg, _type=None):
    _list = materials.front_layer.labels['msg_box'].element.text + '\n' + _msg
    #materials.front_layer.labels['msg_box'].element.text = _msg
    if _list.count('\n') >= 5:
        _list = _list[_list.find('\n') + 1:]
    materials.front_layer.labels['msg_box'].element.text = _list
