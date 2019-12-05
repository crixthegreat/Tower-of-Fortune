#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/6/5 12:10:57
import os
import string
import copy
import zipfile
import pyglet


# The globel variables
GAME_TITLE = 'MY GAME'
# not used
PLAYER_NAME = 'crix'
VERSION = 'beta 0.93'
ZONE_NAME = ['平静的森林', '漆黑的地牢', '远方的孤岛', '精灵的国度', 
        '奇妙的幻境', '地狱的试炼']

# game status
# 
GAME_STATUS = dict(END='END', 
        STARTED='STARTED', 
        LOOT='LOOT', 
        CORPSE='CORPSE', 
        CAMP='CAMP',
        BATTLE_END='BATTLE_END',
        GAME_OVER='GAME_OVER'
        )

# not used
MAX_LEN = 20
DEFAULT_COLOR = (0, 0, 0, 255)
GREEN_COLOR = (0,200,30,255)
ORANGE_COLOR = (230,30,230,255)
# RED color
HIGHLIGHT_COLOR = (200, 30, 30, 255)
# the probablity of tent(camp)-event and corpse-event (in percent)
TENT_RATE = 5
CORPSE_RATE = 2

# used for items
MAX_ITEM_BOX = 130
LEGEND_DROP_RATE = 2
# set items is not added yet
SET_DROP_RATE = 2
RARE_DROP_RATE = 100
MAGIC_DROP_RATE = 1500
SPECIAL_AFFIX_RATE = 20  #spcial condition for dice_max and dice_min affix

RARE_TYPE_NORMAL = 0
RARE_TYPE_MAGIC = 1
RARE_TYPE_RARE = 2
RARE_TYPE_LEGEND = 3

# ITEM_AFFIX_COUNT is to define the quantity of affixes which a item can has 
ITEM_AFFIX_COUNT = {}
ITEM_AFFIX_COUNT = {
        # rate is in %
        RARE_TYPE_NORMAL:{'min':2, 'max':2, 'rate':50},
        RARE_TYPE_MAGIC:{'min':3, 'max':4, 'rate':40},
        RARE_TYPE_RARE:{'min':5, 'max':6, 'rate':40},
        RARE_TYPE_LEGEND:{'min':7, 'max':8, 'rate':30}}
# the divinity items is not added yet
RARE_TYPE_DIVINITY = 4
RARE_TYPE_NAME = ['普通', '魔法', '稀有' ,'传说', '神圣']
MAIN_TYPE_NAME = ['单手武器', '双手武器', '副手武器', '头', '肩', '颈', 
        '胸', '手腕', '手', '腰', '腿', '脚', '手指']

AFFIX_MAX_NO = 22 # there are 22 affixes for items
AFFIX_MAX_USED_NO = 20 # but 20 used by now

# The data files
ITEM_DATA_FILE = './data/item.csv'
SKILL_DATA_FILE = './data/skill.csv'
ENEMY_DATA_FILE = './data/enemy.csv'
ATTACK_STYLE_FILE = './data/attack_style.csv'
# the game save file
SAVE_FILE = './data/save.tof'

# The image files are dealt(import to image object) by image_from_file method
# there files was packed into monster.zip and gui.zip
# the image file can be static images(jpg/png files) or animations(gif files)
# which are identified and handled automatically
# the extention name of the file need not be specified
# Though the merged png files to be cut into grids are dealt one by one
BACKGROUND_IMG_FILE = 'bg'
FRONT_IMG_FILE = 'front'
INFO_LAYER_IMG_FILE = 'info_layer'
STRIKE_IMG_FILE = 'strike'
CRITICAL_STRIKE_IMG_FILE = 'critical_strike'
SUPER_STRIKE_IMG_FILE = 'super_strike'
EXPLODE_IMG_FILE = 'explode'
PLAYER_IMG_FILE = 'player_s'
ENEMY_IMG_FILE = 'monster-30-1'
MAP_FILE = './materials/background/map.tmx'
RIP_IMG_FILE = 'rip'
ICON_SELECT_IMG_FILE = 'icon_select'
ITEM_SELECT_IMG_FILE = 'item_select'
SKILL_SELECT_IMG_FILE = 'skill_select'
ITEM_BOX_IMG_FILE = 'item_box'
SINGLE_ITEM_BOX_IMG_FILE = 'single_item_box'
SINGLE_EQUIPED_ITEM_BOX_IMG_FILE = 'single_equiped_item_box'
ATTACK_IMG_FILE = 'attack'
DEFEND_IMG_FILE = 'defend'
LUCK_IMG_FILE = 'luck'
SAVE_LOAD_BG_IMG_FILE = 'save_load_layer_bg'
SELECT_BAR_IMG_FILE = 'select_bar'
MAP_SELECT_IMG_FILE = 'map_select'
# empty save slot ( a cross char)
EMPTY_IMG_FILE = 'empty'
MESSAGE_BOX_IMG_FILE = 'message_box'
# sprites for control indications of different events
BATTLE_CONTROL_IMG_FILE = 'battle_control'
LOOT_CONTROL_IMG_FILE = 'loot_control'
CORPSE_CONTROL_IMG_FILE = 'corpse_control'
MAIN_CONTROL_IMG_FILE = 'main_control'
CAMP_CONTROL_IMG_FILE = 'camp_control'
DEFAULT_MONSTER_IMG_FILE = 'monster-30-0'
#  file for CORPSE-loot event
CORPSE_EVENT_IMG_FILE = 'corpse'
# file for campfire event
CAMP_EVENT_IMG_FILES = ['campfire-0', 'campfire-1', 'campfire-2', 
        'campfire-3', 'campfire-4', 'campfire-5']
# file for background image of the zones
# with the size of 800 x 200
ZONE_BACK_IMG_FILES = ['background-0', 'background-1', 'background-2', 
        'background-3', 'background-4', 'background-5']

# monsters' & other's image file
MONSTER_ZIP_FILE = './pic/monster.zip'
GUI_ZIP_FILE = './pic/gui.zip'

# the 4 image files below are merged image file to be cut into grids
# which are dealt one by one without methods
ITEM_IMG_FILE = './pic/item.png'
DICE_IMG_FILE = './pic/dice.png'
ATTACK_STYLE_IMG_FILE = './pic/attack_style.png'
START_ARROW_IMG_FILE = './pic/start.png'

# the music files
TITLE_MUSIC_FILE = './music/title.ogg'
BG_MUSIC_FILE = './music/main.ogg'
HIGHSCORE_MUSIC_FILE = './music/highscore.ogg'

# The player affixes
PLAYER_AFFIX = dict(
        Atk = 0,
        Def = 0,
        Luc = 0,
        Vit = 0,
        CriDmg = 0,
        MaxDice = 6,
        BlockValue = 0,
        ShortDistanceAtkDecreaseRate = 0,
        BrambleDmg = 0,
        HpBonusRate = 0,
        HpRegen = 0,
        HpAbsorb = 0, 
        HpHit = 0,
        MagicFind = 0,
        GoldFind = 0,
        ExpBonus = 0,
        ExpWhenKill = 0,
        MinDice = 1,
        DebuffRoundMinus = 0,
        EliteDamage = 0,
        X4 = 0,
        X5 = 0)

# The skills count of the player
SKILL_COUNT_BY_LEVEL = {}
SKILL_COUNT_BY_LEVEL = {
        (1,9):1,
        (10,30):2,
        (31,49):3,
        (50,60):4}

# Read the data of the items
ITEMS_DATA = []
_line = []
_item = {}
ITEM_AFFIX_BASE_VALUE = []
ITEM_AFFIX_NAME = []
ITEM_AFFIX_CNAME = []
ITEM_TYPE_USED = []
with open(ITEM_DATA_FILE, 'r') as f:
    line = f.readline()
    _ = 0
    while line:
        _ += 1
        _line = line.split(',')
        _item = dict(name=_line[0], 
                name_string=_line[1], 
                affix_value=_line[2:AFFIX_MAX_USED_NO + 2], 
                affix_can_use=_line[24], 
                main_type=_line[25], 
                equiped_pos=_line[26][::-1][1:][::-1])
        #print(_line, _item['main_type'])
        if _ == 1:
            ITEM_AFFIX_CNAME = _line
            ITEM_AFFIX_CNAME = ITEM_AFFIX_CNAME[2:AFFIX_MAX_USED_NO + 2]
        if _ == 2:
            ITEM_AFFIX_BASE_VALUE = _line
            ITEM_AFFIX_BASE_VALUE = ITEM_AFFIX_BASE_VALUE[2:AFFIX_MAX_USED_NO + 2]
            for _i in range(AFFIX_MAX_USED_NO):
                if ITEM_AFFIX_BASE_VALUE[_i]:
                    ITEM_AFFIX_BASE_VALUE[_i] = float(ITEM_AFFIX_BASE_VALUE[_i])
                else:
                    ITEM_AFFIX_BASE_VALUE[_i] = 0
        if _ == 3:
            ITEM_AFFIX_BASE_NAME = _line
            ITEM_AFFIX_BASE_NAME = ITEM_AFFIX_BASE_NAME[2:AFFIX_MAX_USED_NO + 2]
        if 4 <= _ <=63:
            if _item['name'] != '未定':
                ITEM_TYPE_USED.append(_ - 4)
            for _i in range(len(_item['affix_value'])):
                if _item['affix_value'][_i] == '×':
                    _item['affix_value'][_i] = 1
                elif _item['affix_value'][_i] == '△':
                    _item['affix_value'][_i] = 2
                elif _item['affix_value'][_i] == '○':
                    _item['affix_value'][_i] = 3
                elif _item['affix_value'][_i] == '◎':
                    _item['affix_value'][_i] = 4
                else:
                    _item['affix_value'][_i] = 0
                if _item['main_type'] != '':
                    _item['main_type'] = int(_item['main_type'])
                else:
                    _item['main_type'] = -1
                if _item['equiped_pos'] != '':
                    _item['equiped_pos'] = int(_item['equiped_pos'])
                else:
                    _item['equiped_pos'] = -1
            ITEMS_DATA.append(_item)
        line = f.readline()
#print(ITEM_TYPE_USED)

# get the monster files name from monster.zip
with zipfile.ZipFile(MONSTER_ZIP_FILE) as _file:
    MONSTER_FILE_LIST = _file.namelist()
# get the gui files name from gui.zip
with zipfile.ZipFile(GUI_ZIP_FILE) as _file:
    GUI_FILE_LIST = _file.namelist()

# make a dict to store the monster name and 
# the file type of the monster files(png or gif)
FILE_TYPE = dict()
for _ in range(len(MONSTER_FILE_LIST)):
    FILE_TYPE[MONSTER_FILE_LIST[_][::-1][4:][::-1]] = (
            MONSTER_FILE_LIST[_][::-1][:3][::-1])
# and the GUI file
for _ in range(len(GUI_FILE_LIST)):
    FILE_TYPE[GUI_FILE_LIST[_][::-1][4:][::-1]] = (
            GUI_FILE_LIST[_][::-1][:3][::-1])

# the enemy affix
ENEMY_RANK_NAME = ['喽啰', '精英', '头目', '首领']
ENEMY_AFFIX = dict(
        hp = 100, 
        max_hp = 100, 
        Atk = 1,
        Def = 1, 
        Luc = 1,
        CriDmg = 1,
        Max_Dice = 6,
        Min_Dice = 1)
ENEMY_RATE = dict(
        CHIEF_BOSS = 3, 
        BOSS = 5, 
        ELITE = 12)
ENEMY_PARAMETER = dict()
ENEMY_PARAMETER['3'] = dict(ATK=15000, MHP=20000, CRIDMG=50, MAX_DICE=8, 
        ATK0=100, MHP0=1000, SKILL_COUNT_BY_ZONE=[2, 2, 3, 3, 4, 4])
ENEMY_PARAMETER['2'] = dict(ATK=15000, MHP=20000, CRIDMG=50, MAX_DICE=7, 
        ATK0=100, MHP0=800, SKILL_COUNT_BY_ZONE=[1, 1, 2, 2, 3, 3])
ENEMY_PARAMETER['1'] = dict(ATK=15000, MHP=20000, CRIDMG=50, MAX_DICE=6, 
        ATK0=100, MHP0=750, SKILL_COUNT_BY_ZONE=[1, 1, 2, 2, 3, 3])
ENEMY_PARAMETER['0'] = dict(ATK=5000, MHP=8500, CRIDMG=0, MAX_DICE=6, 
        ATK0=30, MHP0=500, SKILL_COUNT_BY_ZONE=[0, 0, 0, 0, 0, 1])


# Read enemy data
ENEMY_DATA = []
_line = []
_enemy = {'enemy_name':[], 'Atk':0, 'CriDmg':0, 'max_hp':0}
ENEMY_ATK_AFFIX = []
ENEMY_CRIDMG_AFFIX = []
ENEMY_MAXHP_AFFIX = []
ENEMY_ATK_NAME = []
ENEMY_CRIDMG_NAME = []
ENEMY_MAXHP_NAME = []

with open(ENEMY_DATA_FILE, 'r') as f:
    line = f.readline()
    _ = 0
    while line:
        _ += 1
        _line = line.split(',')
        _line = _line[::-1][1:][::-1]
        #print(_, _line)
        if _ == 1:
            ENEMY_ATK_AFFIX = _line[1:6]
            #print(ENEMY_ATK_AFFIX)
            for _i in range(len(ENEMY_ATK_AFFIX)):
                ENEMY_ATK_AFFIX[_i] = int(ENEMY_ATK_AFFIX[_i])
        elif _ == 2:
            ENEMY_CRIDMG_AFFIX = _line[1:6]
            for _i in range(len(ENEMY_CRIDMG_AFFIX)):
                ENEMY_CRIDMG_AFFIX[_i] = int(ENEMY_CRIDMG_AFFIX[_i])
        elif _ == 3:
            ENEMY_MAXHP_AFFIX = _line[1:6]
            for _i in range(len(ENEMY_MAXHP_AFFIX)):
                ENEMY_MAXHP_AFFIX[_i] = int(ENEMY_MAXHP_AFFIX[_i])
        elif _ == 4:
            ENEMY_ATK_NAME = _line[1:6]
        elif _ == 5:
            ENEMY_CRIDMG_NAME = _line[1:6]
        elif _ == 6:
            ENEMY_MAXHP_NAME = _line[1:6]
        elif 9 <= _ <=39:
            _enemy['enemy_name'] = _line[0:6]
            _enemy['Atk'] = int(_line[6])
            _enemy['CriDmg'] = int(_line[7])
            _enemy['max_hp'] = int(_line[8])
            ENEMY_DATA.append(copy.deepcopy(_enemy))
            
        line = f.readline()



# handling the skill
# read the skill data
SKILL_MAX_NO = 24
SKILL_DATA = []
_skill = {}
with open(SKILL_DATA_FILE, 'r') as f:
    line = f.readline()
    _ = 0
    while line:
        _ += 1
        _line = line.split(',')
        _line = _line[::-1][1:][::-1]
        if _ == 1:
            pass
        elif 2 <= _ <= 25:
            _skill['name'] = _line[0]
            _skill['description'] = _line[1]
            _skill['rate'] = int(_line[2])
            _skill['type'] = int(_line[3])
            _skill['owner'] = int(_line[4])
            _skill['round_last'] = int(_line[5])
            SKILL_DATA.append(copy.deepcopy(_skill))
        line = f.readline()

# read attack style file
_style = {}
_style = dict(attack=[], 
        name = '', 
        description = '', 
        Atk = 0,
        Def = 0, 
        Luc = 0)
ATTACK_STYLE_DATA = []
_ = 0
with open(ATTACK_STYLE_FILE, 'r') as f:
    line = f.readline()
    while line:
        _line = line.split(',')
        _style['attack'] = _line[0:3]
        _style['name'] = _line[3]
        _style['description'] = _line[4]
        _style['Atk'] = int(_line[5])
        _style['Def'] = int(_line[6])
        _style['Luc'] = int(_line[7])
        ATTACK_STYLE_DATA.append(copy.deepcopy(_style))
        line = f.readline()
    #print(ITEM_TYPE_USED)

# attack styles by the three cards
STYLE_VALUE = {
        (0,0,3):9,
        (0,1,2):6,
        (0,2,1):7,
        (0,3,0):8,
        (1,0,2):5,
        (1,1,1):4,
        (1,2,0):3,
        (2,0,1):2,
        (2,1,0):1,
        (3,0,0):0}


def image_from_file(_file, image_file=MONSTER_ZIP_FILE):
    """get a image object from a zip file
    By now, there are two image-file package: MONSTER_ZIP_FILE and GUI_ZIP_FILE
    _file is the main name of image file, NO extentions
    """
    # read a single file from the zip file
    with zipfile.ZipFile(image_file) as _image_file:
        image_file_data = _image_file.open(_file + '.' + FILE_TYPE[_file])
    # check the file is whether a gif file or not    
    if FILE_TYPE[_file]=='gif':
        # the standard gif handling process
        # the '1.gif' or '1.jpg' '1.png' are hint which:
        # helps the module locate an appropriate decoder to use 
        # based on the file extension (help message from pyglet.image.load())
        _anime = pyglet.image.load_animation('1.gif', file=image_file_data)
        _bin = pyglet.image.atlas.TextureBin()
        _anime.add_to_texture_bin(_bin)
        return _anime 
    elif FILE_TYPE[_file]=='png' or FILE_TYPE[_file]=='jpg':
        return  pyglet.image.load('1.' + FILE_TYPE[_file], file=image_file_data) 
    else:
        # By now, only gif, png and jpg files can be read
        raise ValueError('when get image from file, UNKNOWN file type for ', FILE_TYPE[image_file])

# for test    
if __name__ == '__main__':
    for _ in ATTACK_STYLE_DATA:
        print (_)
