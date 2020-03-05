#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/29 11:22:10

#import sys
import os
import random
import json
import cocos
from cocos.director import director
from cocos.scene import Scene
from cocos.scenes import FlipY3DTransition
from cocos.layer import Layer, ScrollingManager, ScrollableLayer
import materials 
from data import const, player, skill
"""i-game written by Crix 2019.06 - 2019.06 
I-GAME is a general struction of a python cocos 2d platform game
which has:
    i-game.py -- main program
        /data
            __init__.py
            Const.py -- stores the game CONSTs
            highscore.py -- handler the highscore
            highscore.tp -- the highscore data file
        /materials
            __init__.py -- defines the labels, sprites, imgs to be used globally
            /background
                the background tiled map (.tmx file & tile(.png) files)
            /main_scr
                __init__.py -- defines the labels, sprites, 
                imgs to be used in main game screen
            /front_layer
                __init__.py -- defines the labels, sprites, 
                imgs to be used in front layer
            /menu
                __init__.py -- defines the labels, sprites, 
                imgs to be used in menu layer
        /tool
            file_test.py -- to initialise the high score record file
        /pic
            alpha.png -- the alphabet image file
            bg.png -- the backgroud image file (800 x 600)
            start.png -- the 'start' image file


------------ A new start ---------------------------------
Tower of fortune (pays homage to the following great games:
- Tower of fortune (iOS)
- Diablo
- The Gambling God (FC)
----------------------------------------------------------
"""
from data import const, player, item, enemy, battle, skill

class Game(object):
    """main game class
    """
    def __init__(self, _player):
        self.player = _player
        self.enemy = None
        # The game has many status: 
        # END - the battle ended, ready to move on  
        # STARTED - battle started
        # LOOT - battle ended with something dropped
        # CAMP - moved to a camp
        # CORPSE - moved to a corpse of dead player
        self.game_status = const.GAME_STATUS['END']
        # not used ??
        self.enter = 0
        # not used ??
        self.msg = []
        self.zone = 0
        # the attack style 
        self.style = [0, 0, 0]
        self.loot_selected = 0
        # stores the dead player's SAVE SLOT number
        self.corpse = None

    @property
    def max_stage(self):
        """self.max_stage =
            the most difficult stage where the player can go to
            namely 0, 1, 2, 3, 4, 5
        """
        _stage = self.player.level // 10
        return _stage if _stage<6 else 5 

    @property
    def game_status(self):
        return self._game_status

    @game_status.setter
    def game_status(self, status):
        """game_status setter method
        to set the control-direction-sprites depending on the game status
        """
        self._game_status = status
        _para = materials.main_scr.CONTROL_PARA
        # set the parameter of indicator sprites(position, image and scales)
        _sprite = materials.main_scr.sprites['control'] 
        for _, __ in _para.items():
            if _ == status:
                _sprite.anchor = 0, 0
                _sprite.position = _para[status]['position']
                _sprite.image = _para[status]['image']
                _sprite.scale = _para[status]['scale']
                break


    def start_game(self):
        """start the game screen and initial the game
        """
        #for _ in range(3):
        #    materials.main_scr.sprites['player_dice_' + str(_)].visible = False
        #    materials.main_scr.sprites['enemy_dice_' + str(_)].visible = False

        for _, sprite in materials.main_scr.sprites.items():
            sprite.visible = False
        
        materials.main_scr.sprites['control'].visible = True
        self.player.sprite.visible = True
        self.player.sprite.image = materials.main_scr.player_image
        self.set_stage(self.player.zone)
        director.replace(Scene(game_screen, front_layer))

    def show_game(self):
        """method to return to the game screen
        """
        director.replace(Scene(game_screen, front_layer))
        self.player.show_player()

    def show_loot(self):
        """show the items dropped by the enemy
        """
        item.hide()
        _sprites = materials.main_scr.sprites 
        _sprites['icon_select'].visible = False
        for _ in range(8):
            _sprites['loot' + str(_)].visible = False

        if self.player.loot:
            _loot = self.player.loot
            for _ in range(len(_loot)):
                _sprites['loot' + str(_)].visible = True
                _sprites['loot' + str(_)].image = materials.item_image[
                        (59-_loot[_].type) * 5 + _loot[_].rare_type]
            _sprites['icon_select'].visible = True
            _sprites['icon_select'].x = 562 + (30 * self.loot_selected)
            # use the item box to show the item dropped and 
            # comparing the corresponding item equipped 
            item.show(self.player.loot[self.loot_selected], 
                    self.player.item_equiped[
                        self.player.loot[self.loot_selected].equiped_pos])

    def show_info(self):
        """display the screen of player information
        (where you check the skills, item equipped and the item-box)
        """
        my_info.status = 'view'
        director.replace(Scene(my_info))
        self.refresh_info()

    def refresh_info(self):
        """update all the data of the info layer 
        """
        # the info layer and the main_scr share the same labels of the player's
        # data so the method player.show_player affects both layer 
        self.player.show_player()
        # show the value of the player
        my_info.show_player_value()

        # show the equiped items of the player
        my_info.show_player_item()
        # show the items in the player's item box
        my_info.show_item_box()

    #def screen_set_focus(self, x, y):
    #    """not used in this game
    #    """
    #    game_screen.set_focus(self.player.sprite.x, self.player.sprite.y)
    
    def show_menu(self):
        """as the name says
        """
        self.game_status = 'END'
        director.replace(FlipY3DTransition(Scene(my_menu)))

    def show_save_load(self):
        """as the name says
        """
        director.replace(FlipY3DTransition(Scene(my_save_load_layer)))
        my_save_load_layer.show_save_slot()
    

    def save(self):
        """save the game(player)
        """
        # turn the player's attribution into a dict
        save_data = dict()

        # load the exist player data
        if os.path.isfile(const.SAVE_FILE):
            with open(const.SAVE_FILE) as _file:
                try:
                    save_data = json.load(_file)
                except:
                    raise IOError(
                            'open file failed when tring to get the save data')
        
        # the KEY of the save_data dictionary is the 'slotX' (X is 0 ~ 8)
        # get the dict-format of player's data
        save_data['slot' + str(self.player.save_slot)] = (
                self.player.player_to_dict())

        # Update the current player's data
        with open(const.SAVE_FILE, 'w') as _file:
            try:
                json.dump(save_data, _file)
            except:
                raise IOError('write file failed when saveing the game')

    def load(self, save_slot):
        """Load the game
        from the specific save slot
        """
        # read the save file
        with open(const.SAVE_FILE) as _file:
            try:
                save_data = json.load(_file)
            except:
                raise IOError('read save file failed when loading the game')
        # get the player's data
        _data = save_data['slot' + str(save_slot)]
        
        # turn to a Player object
        _player = player.dict_to_player(_data)
        _player.save_slot = save_slot

        return _player
    
    def game_over(self):
        """as the names says
        """
        self.game_status = 'GAME_OVER'
        self.player.sprite.image = materials.main_scr.images['rip']

    def show_corpse(self):
        """the event CORPSE, 
        where the player can pay some money to loot the corpse 
        """
        _no_corpse = True
        with open(const.SAVE_FILE) as _file:
            try:
                save_data = json.load(_file)
            except:
                raise IOError(
                        'failed to read save file when checking whether there is corpses in the zone')
        # check whether there is corpses in the zone
        for _, _data in save_data.items():
            if _data['zone']== self.player.zone and (not(_data['alive'])):
                _no_corpse = False
                # e.g self.corpse = 'slot1'
                self.corpse = _
                break
        if _no_corpse:
            self.show_battle()
            return 1

        #print('game changes into CORPSE status')
        #print('the COPRSE slot is ', self.corpse)
        self.game_status = 'CORPSE'
        materials.main_scr.sprites['enemy_sprite'].image = (
                const.image_from_file(
                    const.CORPSE_EVENT_IMG_FILE, const.GUI_ZIP_FILE))
        materials.main_scr.sprites['enemy_sprite'].visible = True
    
    def show_camp(self):
        """ the event CAMP, when the player can pay some money to recover 
        the HP and Enchant the item(not implemented)
        """
        # if the HP is full, generating a enemy insteadly
        if self.player.hp >= self.player.max_hp:
            self.show_battle()
            return 1
        self.game_status = 'CAMP'
        materials.main_scr.sprites['enemy_sprite'].image = (
                const.image_from_file(const.CAMP_EVENT_IMG_FILES[self.player.zone], 
                    const.GUI_ZIP_FILE))
        materials.main_scr.sprites['enemy_sprite'].visible = True

    def show_battle(self):
        """start the battle with enemy
        """
        _level = random.randrange(self.zone * 10 + 1, (self.zone + 1) * 10)
        self.enemy = enemy.gen_enemy(None, None, self.player.zone, _level)
        if self.enemy:
            self.game_status = 'STARTED'
            enemy.show_enemy(self.enemy)
            self.player.loot = []

    def move_on(self):
        ''' the player moves to the next location 
        '''
        self.save()
        _r = random.randrange(1,100)
        if 1<= _r <= const.CORPSE_RATE:
            #print('now game is going to show the corpse')
            self.show_corpse()
        elif const.CORPSE_RATE < _r <= const.CORPSE_RATE + const.TENT_RATE:
            self.show_camp()
        else:
            self.show_battle()

    def set_stage(self, no):
        '''set the current stage
        '''
        self.player.zone = no
        self.zone = no
        materials.front_layer.labels['zone_label'].element.text = (
                const.ZONE_NAME[no])
        my_main.image = const.image_from_file(
                const.ZONE_BACK_IMG_FILES[no], const.GUI_ZIP_FILE)

        # display the stage numbers of the zones where the player can access
        materials.front_layer.show_map_selector(self.max_stage, no)

if __name__ == '__main__':
    msg = []
    # change the working dir to the exe temp dir 
    # when you use pyinstaller to make a one-file exe package, you need this:

    #if getattr(sys, 'frozen', False):
    #    os.chdir(sys._MEIPASS)

    my_game = Game(player.Player())
    game_screen = ScrollingManager()
    # the tile map 'map.tmx' which has a layer called 'start'
    # use the editor software called 'Tiled' to make a tile map 
    front_layer = materials.front_layer.Front_Layer()
    map_layer = cocos.tiles.load('./materials/background/map.tmx')['start']
    my_info = materials.info_layer.Info_Layer(my_game)
    my_save_load_layer = materials.save_load_layer.Save_Load_Layer(my_game)
    my_menu = materials.menu.Menu_Screen(my_game)
    my_main = materials.main_scr.Main_Screen(my_game)
    # the order of the 'add' makes sense!
    game_screen.add(map_layer)
    game_screen.add(my_main)
    #game_screen.add(front_layer)
    main_scene = Scene(my_menu)
    #print ('game initialised')
    director.run(main_scene)
    #print('game end')
