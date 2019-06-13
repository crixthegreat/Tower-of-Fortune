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
import materials

images = {}

"""
time_label & best_time_label : as the name says
"""

labels = dict(old_msg_box=cocos.text.Label('old message', 
    font_size=12,font_name='Gadugi', 
    bold=False,color=const.DEFAULT_COLOR, x=500, y=200, width= 250, multiline=True), 
    msg_box=cocos.text.Label('message here', 
        font_size=14,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=500, y=50))

labels['level_label'] = cocos.text.Label('Lv:',
        font_size=14,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=10, y=580)
labels['hp_label'] = cocos.text.Label('Hp:', 
        font_size=14,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=100, y=580)
labels['exp_label'] = cocos.text.Label('Exp:', 
        font_size=14,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=10, y=550)
labels['enemy_name_label'] = cocos.text.Label('Name:', 
        font_size=14,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=600, y=580)
labels['enemy_level_label'] = cocos.text.Label('Lv:',
        font_size=14,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=600, y=550)
labels['enemy_hp_label'] = cocos.text.Label('Hp:', 
        font_size=14,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=700, y=550)
labels['enemy_skill_label'] = cocos.text.Label('Skill:', 
        font_size=14,font_name='Gadugi', 
        bold=False,color=const.DEFAULT_COLOR, x=700, y=520, width=100, multiline=True)


sprites = {}

#bg_music = materials.Audio(Const.BG_MUSIC_FILE)


def show_message(_msg, _type=None):
    _list = materials.front_layer.labels['old_msg_box'].element.text + '\n' + materials.front_layer.labels['msg_box'].element.text
    materials.front_layer.labels['msg_box'].element.text = _msg
    if _list.count('\n') >= 7:
        _list = _list[_list.find('\n') + 1:]
    materials.front_layer.labels['old_msg_box'].element.text = _list
