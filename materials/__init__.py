#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/28 17:03:36
"""THE GOLABEL MATERIALS DEFINITION FILE
"""
import os
from data import const
import pyglet
import cocos
import random
from cocos.audio.pygame.mixer import Sound
from cocos.audio.pygame import mixer

"""materials define all the images, labels, sprites
and also define the methods handling them
"""
class Audio(Sound):
    """The standard class for Audio
    """
    def __ini__(self, file_name):
        super(Audio, self).__init__(file_name)



def time_format(t):
    _ = '{:>2}:{:>2}'.format(str(int(t // 60)), str(int(t % 60))) 
    return _


def gen_anime_sprite(img, grid_x, grid_y, delay, loop, pos_x, pos_y):

    _image = pyglet.image.load(img)
    _anime = pyglet.image.ImageGrid(_image, grid_x, grid_y)
    _seq = pyglet.image.Animation.from_image_sequence(_anime, delay, loop)
    return cocos.sprite.Sprite(_seq, position=(pos_x, pos_y))

def alpha_sprite(t):
    return materials.sprites['alpha_str' + str(t)]

def show_alpha(_str, pos_x=100, pos_y=400):
    """The KEY method of this game
    to display a string 
    """

    if len(_str) > const.MAX_LEN:
        _str = _str[:const.MAX_LEN]
    #print('show alpha:', _str)

    for _ in range(const.MAX_LEN):
        sprites['alpha_str' + str(_)].position = 0, 0

    for _ in range(len(_str)):
        if _str[_] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
            _str_index = ord(_str[_])
            if _str_index >= 97:
                _str_index -= 97
            else:
                _str_index -= 38
        else:
            _str_index = 26

        alpha_sprite(_).visible = True
        alpha_sprite(_).image = alpha_image[_str_index]
        alpha_sprite(_).position = pos_x + _ * 50, pos_y
        alpha_sprite(_).scale = random.randrange(8, 20) / 10
        alpha_sprite(_).rotation = random.randrange(-30, 30)


mixer.init()
cocos.director.director.init(width=800, height=600, caption=const.GAME_TITLE)

bg_file = os.path.abspath(const.BACKGROUND_IMG_FILE)
bg_img = pyglet.image.load(bg_file) 

#load the alphabet to alpha_image
alpha_image = []
alpha_image = pyglet.image.ImageGrid(pyglet.image.load('./pic/alpha.png'), 2, 27)

item_image = pyglet.image.ImageGrid(pyglet.image.load(const.ITEM_IMG_FILE), 60, 5)
dice_image = pyglet.image.ImageGrid(pyglet.image.load(const.DICE_IMG_FILE), 5, 2)
front_image = pyglet.image.load(const.FRONT_IMG_FILE) 

images = {'alpha_image':alpha_image, 'bg_img':bg_img, 'item_image':item_image, 'dice_image':dice_image, 'front_img':front_image}




def gif_to_anime(_file):
    _anime = pyglet.image.load_animation(_file)
    _bin = pyglet.image.atlas.TextureBin()
    _anime.add_to_texture_bin(_bin)
    return _anime

def gif_to_sprite(_file, _scale=1):
    _anime = gif_to_anime(_file)
    return cocos.sprite.Sprite(_anime, position =(600,300), scale = _scale)


strike_anime = pyglet.image.load_animation(const.STRIKE_IMG_FILE)
strike_bin = pyglet.image.atlas.TextureBin()
strike_anime.add_to_texture_bin(strike_bin)
strike_anime = pyglet.image.load_animation(const.STRIKE_IMG_FILE)
strike_bin = pyglet.image.atlas.TextureBin()
strike_anime.add_to_texture_bin(strike_bin)

#sprites = {'alpha_str' + str(_):cocos.sprite.Sprite(alpha_image[_], position=(0, 0)) for _ in range(const.MAX_LEN)}
sprites = {}
sprites['item'] = cocos.sprite.Sprite(item_image[0], position = (400,335))
sprites['player_item'] = cocos.sprite.Sprite(item_image[0], position = (220,315))
sprites['strike'] = gif_to_sprite(const.STRIKE_IMG_FILE, 0.7)
sprites['explode'] = gif_to_sprite(const.EXPLODE_IMG_FILE, 2)


import materials.background
import materials.main_scr
import materials.front_layer
import materials.menu
