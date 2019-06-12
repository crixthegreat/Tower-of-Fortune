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
    font_size=12,font_name='verdana', 
    bold=False,color=const.DEFAULT_COLOR, x=450, y=200, width= 200, multiline=True), 
    msg_box=cocos.text.Label('message here', 
        font_size=14,font_name='verdana', 
        bold=False,color=const.DEFAULT_COLOR, x=450, y=50))

sprites = {}

#bg_music = materials.Audio(Const.BG_MUSIC_FILE)


def show_message(_msg, _type=None):
    _list = materials.front_layer.labels['old_msg_box'].element.text + '\n' + materials.front_layer.labels['msg_box'].element.text
    materials.front_layer.labels['msg_box'].element.text = _msg
    if _list.count('\n') >= 7:
        _list = _list[_list.find('\n') + 1:]
    materials.front_layer.labels['old_msg_box'].element.text = _list
