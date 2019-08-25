#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/28 17:03:36
from data import const
import pyglet
import cocos
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer
#from cocos.scenes import FlipY3DTransition
import materials
import random
#from materials import color_text

images = {}
# not used in this game
#images = {'t2_anime':[materials.alpha_image[26], materials.alpha_image[53]]}

labels = dict(version_label=cocos.text.Label(const.VERSION, 
    font_size=16,font_name='Verdana', 
    bold=False,color=const.HIGHLIGHT_COLOR, x=0, y=580))
#,
#    level_label=cocos.text.Label('', font_size=20,
#        font_name='Verdana', bold=True,
#        color=const.HIGHLIGHT_COLOR, x=355, y=240))

# not used in this game
#t2_seq = pyglet.image.Animation.from_image_sequence(
#        images['t2_anime'], 0.5, True)

sprites = {'start_sprite':materials.gen_anime_sprite(
    const.START_ARROW_IMG_FILE, 3, 1, 0.5, True, 440, 270)}
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
        
        self.key_events = {
                "GLOBAL":{
                    ('ENTER',):self.start_game,
                    ('UP','DOWN','LEFT','RIGHT'):self.menu_select}
                }

        self.game_status = 'END'
        #director.replace(FlipY3DTransition(Scene(my_menu)))
        #self.game.show_menu()

        # for the test of Color_Text object
        #self.title_text = color_text.Color_Text('HELLO', 100, 300, 1.2, True, True)
        #for _ in self.title_text.sprites:
        #    self.add(_)


    def start_game(self):
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
            raise ValueError('game enter index error!')

    def menu_select(self, key):
        # use the UP or DOWN to change the entry
        #
        _entry_count = 3
        if 'UP'==key or 'LEFT'==key:
            if self.game.enter > 0:
                self.game.enter -= 1
                sprites['start_sprite'].y += 55
            else:
                self.game.enter = _entry_count - 1
                sprites['start_sprite'].y -= 55 * (_entry_count - 1)

        if 'DOWN'==key or 'RIGHT'==key:
            if self.game.enter < (_entry_count - 1):
                self.game.enter += 1
                sprites['start_sprite'].y -= 55
            else:
                self.game.enter = 0
                sprites['start_sprite'].y += 55 * (_entry_count - 1)

        # for the test of the Color_Text object
        #menu_list = ['start game', 'how to', 'credit']
        #self.title_text.text = menu_list[self.game.enter]


    def on_key_press(self, key, modifiers):
        """key press handler for menu class
        """
        self.keys_pressed.add(key)
        key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]
        materials.do_key_events(self, 'GLOBAL', key_names)
        

    def on_key_release(self, key, modifiers):
        # release the key_pressed set
        # be careful that the layer changing when key is be pressed (but not released)
        if self.keys_pressed and key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def draw(self):
        self.image.blit(0, 0)
    

def show():
    materials.main_scr.bg_music.stop()
    #materials.main_scr.highscore_music.stop()
    bg_music.play(-1)

