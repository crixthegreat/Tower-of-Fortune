#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/8/23 10:12:20

#load the alphabet to alpha_image

import random
import pyglet
import cocos

alpha_image = []
alpha_image = pyglet.image.ImageGrid(pyglet.image.load('./pic/alpha.png'), 2, 27)


class Color_Text(object):
    """Color_Text obejct contains
    a list of sprites, to show a colorful string with MAX_LENGTH of 20
    [usage]

    txt = Color_Text(
        text='', 
        pos_x=0, 
        pos_y=0, 
        size=1, 
        shuffle_size=False, 
        shuffle_angle=False)

    [example]
    1. define the color text string
    
    (layer object).title_text = 
        color_text.Color_Text('Hello', 100, 300, 1.2, True, True)
    
    2. add the sprites to the layer
    
    for _ in self.title_text.sprites:
        self.add(_)

    3.when you need to assign/change the text, just:

    self.title_text.text = '(any text you want)'

    4.you can also change the other attributes of the text:
        pos_x, pos_y, size(scale), shuffle_size, shuffle_angel.
        the text redraws immediately.

    """
    MAX_LEN = 20

    def __init__(self, text='', pos_x=0, pos_y=0, 
            size=1, shuffle_size=False, shuffle_angle=False):

        MAX_LEN = Color_Text.MAX_LEN
        text = text[:MAX_LEN]
        text += ' ' * (MAX_LEN - len(text))
        self._text = text
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._size = size
        self._shuffle_size = shuffle_size
        self._shuffle_angle = shuffle_angle 
        self.sprites = [cocos.sprite.Sprite(self.text_image(text[_:_ + 1]), 
            position=(pos_x, pos_y), scale=size) for _ in range(MAX_LEN)]
        self.show()

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, text):
        self._text = text
        MAX_LEN = Color_Text.MAX_LEN
        text = text[:MAX_LEN]
        text += ' ' * (MAX_LEN - len(text))
        for _, _sprite in enumerate(self.sprites):
            _sprite.image = self.text_image(text[_:_ + 1])
        self.show()
    
    @property
    def pos_x(self):
        return self._pox_x

    @pos_x.setter
    def pos_x(self, pos):
        self._pos_x = pos
        self.show()

    @property
    def pos_y(self):
        return self._pox_y

    @pos_y.setter
    def pos_y(self, pos):
        self._pos_y = pos
        self.show()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, s):
        self._size = s
        self.show()

    @property
    def shuffle_size(self):
        return self._shuffle_size

    @shuffle_size.setter
    def shuffle_size(self, s):
        # s is boolean value
        self._shuffle_size = s
        self.show()

    @property
    def shuffle_angle(self):
        return self._shuffle_angle

    @shuffle_angle.setter
    def shuffle_angle(self, s):
        # s is boolean value
        self._shuffle_angle = s
        self.show()

    def text_image(self, char):
        """
        get the split image of the char
        """
        if char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
            _index = ord(char)
            if _index >= 97:
                _index -= 97
            else:
                _index -= 38
        else:
            _index = 26

        return alpha_image[_index]


    def show(self):
        for _, _sprite in enumerate(self.sprites):
            if  _ >= len(self._text) or self._text[_] == ' ': 
                _sprite.visible = False
            else:
                _sprite.visible = True
            _sprite.scale = self._size
            _sprite.position = (self._pos_x + _ * 50 * (self._size), 
                    self._pos_y)
            if self._shuffle_size:
                _sprite.scale = self._size * (1 + random.randrange(-2, 5) / 10) 
            if self._shuffle_angle:
                _sprite.rotation = random.randrange(-30, 30)

            


    



