#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/28 17:03:36
import os
from data import const
import pyglet
import cocos
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer, ScrollingManager, ScrollableLayer
from cocos.scenes import FlipY3DTransition
import materials
import random
from data import player, skill

images = {'t2_anime':[materials.alpha_image[26], materials.alpha_image[53]]}

labels = dict(version_label=cocos.text.Label(const.VERSION, 
    font_size=16,font_name='Verdana', 
    bold=False,color=const.HIGHLIGHT_COLOR, x=0, y=580))
#,
#    level_label=cocos.text.Label('', font_size=20,
#        font_name='Verdana', bold=True,
#        color=const.HIGHLIGHT_COLOR, x=355, y=240))


t2_seq = pyglet.image.Animation.from_image_sequence(images['t2_anime'], 0.5, True)

sprites = {'start_sprite':materials.gen_anime_sprite(const.START_ARROW_IMG_FILE, 3, 1, 0.5, True, 440, 270)}
#'t2_sprite':cocos.sprite.Sprite(t2_seq, position=(650, 400))}

bg_music = materials.Audio(const.TITLE_MUSIC_FILE)

class Menu_Screen(Layer):
    """The menu layer class, where the player starts the game 
    and changes the game level
    """
    is_event_handler = True

    def __init__(self, game):

        super(Menu_Screen, self).__init__()
        
        self.game = game
        self.keys_pressed = set()


        self.image = materials.images['bg_img']

        if hasattr(materials, 'labels'):
            for _, _label in materials.labels.items():
                self.add(_label)
                _label.visible = False
        if hasattr(materials.menu, 'labels'):
            for _, _label in materials.menu.labels.items():
                self.add(_label)
        if hasattr(materials, 'sprites'):
            for _, _sprite in materials.sprites.items():
                self.add(_sprite)
                _sprite.visible = False
        if hasattr(materials.menu, 'sprites'):
            for _, _sprite in materials.menu.sprites.items():
                self.add(_sprite)
        

        self.game_status = 'END'
        #director.replace(FlipY3DTransition(Scene(my_menu)))
        #self.game.show_menu()


    def on_key_press(self, key, modifiers):
        """key press handler for menu class
        """
        self.keys_pressed.add(key)
        key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]
        _enter_list = ['start', 'howtoplay', 'credit']
        _enter = 0
        if 'ENTER' in key_names:
            #Start the game
            self.keys_pressed.clear()
            if self.game.enter == 2:
                return 1
                director.replace(Scene(credit_layer))
            if self.game.enter == 1:
                return 1
                # how to play layer is to be added
                self.game.show_how_to_play
            elif self.game.enter == 0:
                self.game.show_save_load()
                return 1
            else:
                print('game enter error!')
                sys.exit()
            self.game.start_game()
        # use the LEFT or RIGHT to change the game level
        elif 'UP' in key_names:
            if self.game.enter != 0:
                self.game.enter -= 1
                materials.menu.sprites['start_sprite'].y += 55
        elif 'DOWN' in key_names:
            if self.game.enter != 2:
                self.game.enter += 1
                materials.menu.sprites['start_sprite'].y -= 55
        elif 'F12' in key_names:
            pass
            #materials.menu.show_highscore()



    def on_key_release(self, key, modifiers):
        # release the key_pressed set
        # be careful that the layer changing when key is be pressed (but not released)
        if self.keys_pressed and key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def draw(self):
        self.image.blit(0, 0)
    

def show():
    """
    materials.show_alpha('typingpractice', 100, 450)
    for _ in range(6):
        materials.sprites['alpha_str' + str(_)].position = 280 + _ * 50, 500
        materials.sprites['alpha_str' + str(_)].scale = random.randrange(8, 20) / 10
        materials.sprites['alpha_str' + str(_)].rotation = random.randrange(-30, 30)
    for _ in range(8):
        materials.sprites['alpha_str' + str(_ + 6)].position = 230 + _ * 50, 400 
        materials.sprites['alpha_str' + str(_ + 6)].scale = random.randrange(8, 20) / 10
        materials.sprites['alpha_str' + str(_ + 6)].rotation = random.randrange(-30, 30)
    """
    materials.main_scr.bg_music.stop()
    #materials.main_scr.highscore_music.stop()
    bg_music.play(-1)

