#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/6/5 12:10:57
import os
import string
import copy
# The globel variables
GAME_TITLE = 'MY GAME'
PLAYER_NAME = 'crix'
VERSION = 'alpha 0.01'
ZONE_NAME = ['普通的森林', '中等的丛林', '困难的地牢', '噩梦的幻境', '地狱的试炼', '炼狱的折磨']
MAX_LEN = 20
DEFAULT_COLOR = (0, 0, 0, 255)
GREEN_COLOR = (0,200,30,255)
ORANGE_COLOR = (230,30,230,255)
HIGHLIGHT_COLOR = (200, 30, 30, 255)

# used for items
LEGEND_DROP_RATE = 2
SET_DROP_RATE = 2
RARE_DROP_RATE = 100
MAGIC_DROP_RATE = 1500
SPECIAL_AFFIX_RATE = 20  #spcial condition for dice_max and dice_min affix

RARE_TYPE_NORMAL = 0
RARE_TYPE_MAGIC = 1
RARE_TYPE_RARE = 2
RARE_TYPE_LEGEND = 3
RARE_TYPE_DIVINITY = 4
RARE_TYPE_NAME = ['普通', '魔法', '稀有' ,'传说', '神圣']
MAIN_TYPE_NAME = ['单手武器', '双手武器', '副手武器', '头', '肩', '颈', '胸', '手腕', '手', '腰', '腿', '脚', '手指']

AFFIX_MAX_NO = 22 # there are 22 affixes for items
AFFIX_MAX_USED_NO = 20 # but 20 used by now

# The data files
ITEM_DATA_FILE = './data/item.csv'
SKILL_DATA_FILE = './data/skill.csv'
ENEMY_DATA_FILE = './data/enemy.csv'
ATTACK_STYLE_FILE = './data/attack_style.csv'
SAVE_FILE = './data/save.tof'

BACKGROUND_IMG_FILE = './pic/bg.png'
FRONT_IMG_FILE = './pic/front.png'
STRIKE_IMG_FILE = './pic/strike.gif'
CRITICAL_STRIKE_IMG_FILE = './pic/critical_strike.gif'
SUPER_STRIKE_IMG_FILE = './pic/super_strike.gif'
EXPLODE_IMG_FILE = './pic/explode.gif'
PLAYER_IMG_FILE = './pic/player_s.png'
ENEMY_IMG_FILE = './pic/monster-30-1_s.png'
TITLE_MUSIC_FILE = './music/title.ogg'
BG_MUSIC_FILE = './music/main.ogg'
HIGHSCORE_MUSIC_FILE = './music/highscore.ogg'
MAP_FILE = './materials/background/map.tmx'
ITEM_IMG_FILE = './pic/item.png'
DICE_IMG_FILE = './pic/dice.png'
RIP_IMG_FILE = './pic/rip.png'
ICON_SELECT_IMG_FILE = './pic/icon_select.png'
ITEM_BOX_IMG_FILE = './pic/item_box.png'
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


# Read item data
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
ELITE_ATK = 15000
NORMAL_ATK = 5000
ELITE_MHP = 20000
NORMAL_MHP = 8500
ELITE_CRIDMG = 50
NORMAL_CRIDMG = 0

# Read item data
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
if __name__ == '__main__':
    for _ in ATTACK_STYLE_DATA:
        print (_)


