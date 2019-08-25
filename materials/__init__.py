#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/28 17:03:36
"""THE GOLABEL MATERIALS DEFINITION FILE
"""
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

#def time_format(t):
#    _ = '{:>2}:{:>2}'.format(str(int(t // 60)), str(int(t % 60))) 
#    return _


def gen_anime_sprite(img, grid_x, grid_y, delay, loop, pos_x, pos_y):

    _image = pyglet.image.load(img)
    _anime = pyglet.image.ImageGrid(_image, grid_x, grid_y)
    _seq = pyglet.image.Animation.from_image_sequence(_anime, delay, loop)
    return cocos.sprite.Sprite(_seq, position=(pos_x, pos_y))



mixer.init()
cocos.director.director.init(width=800, height=600, caption=const.GAME_TITLE)

bg_img = const.image_from_file(const.BACKGROUND_IMG_FILE, const.GUI_ZIP_FILE)


item_image = pyglet.image.ImageGrid(
        pyglet.image.load(const.ITEM_IMG_FILE), 60, 5)
dice_image = pyglet.image.ImageGrid(
        pyglet.image.load(const.DICE_IMG_FILE), 5, 2)
front_image = const.image_from_file(const.FRONT_IMG_FILE, const.GUI_ZIP_FILE) 
info_layer_image = const.image_from_file(
        const.INFO_LAYER_IMG_FILE, const.GUI_ZIP_FILE) 

images = {'bg_img':bg_img, 'item_image':item_image, 
        'dice_image':dice_image, 'front_img':front_image, 
        'info_layer_img':info_layer_image}

sprites = {}
sprites['item'] = cocos.sprite.Sprite(item_image[0], position = (400,335))
sprites['player_item'] = cocos.sprite.Sprite(
        item_image[0], position = (220,315))
sprites['strike'] = cocos.sprite.Sprite(
        const.image_from_file(const.STRIKE_IMG_FILE, const.GUI_ZIP_FILE), 
        position=(600,300), scale=0.7)
sprites['explode'] =  cocos.sprite.Sprite(
        const.image_from_file(const.EXPLODE_IMG_FILE, const.GUI_ZIP_FILE), 
        position=(600,300), scale=2)

def do_key_events(_layer, status, key_names):
    """do the key events of the _layers
    """
    # not all game status need handle key events
    if not(status in _layer.key_events.keys()):
        return None
    # get the key tuplets of the specified status 
    for _keys in _layer.key_events[status].keys():
        # _keys is a tuplet
        for _key in _keys:
            # _key is a key-name
            if _key in key_names:
                # here gets the count of argument of the method
                _n = _layer.key_events[status][_keys].__code__.co_argcount
                if _n>1:
                    # transfer the _key(a key-name) into the method
                    _layer.key_events[status][_keys](_key)
                else:
                    # the method without argument is called directly
                    _layer.key_events[status][_keys]()
                break


import materials.background
import materials.main_scr
import materials.front_layer
import materials.menu
import materials.info_layer
import materials.save_load_layer
import materials.color_text
