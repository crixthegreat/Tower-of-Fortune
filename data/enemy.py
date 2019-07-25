#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/6/7 13:50:35

import time
import copy
import random
import zipfile
import pyglet
from cocos import actions
from data import const, skill
import materials
"""the code handling enemys
There are totally 31 types of enemys which has six zone-level each other.
The type no.1 is chief-boss enemy(rank 4)
The type no.2 and no.3 is boss enemy(rank 3)
The left 28 types of enemys are normal enemy (rank 1)
The normal type enemys can also become elites sometimes (rank 2)
The random rate of enemys above is defined by ENEMY_RATE
"""
class Enemy(object):
    """The Enemy Class
    """

    def __init__(self, sprite=None):
        self.no = 0
        self.rank = 0
        self.level = 1
        self.skill = []
        self.zone = 0
        self.sprite = sprite
        self.value = copy.deepcopy(const.ENEMY_AFFIX)
        # enemy has 5 type for ATK, CRIDMG and MAXHP
        # so every single kind of enemy have 125 types!
        # see the const.ENEMY_ATK_NAME,ENEMY_CRIDMG_NAME and ENEMY_MAXHP_NAME
        self.type = [2 ,2, 2]
        self.hp = self.value['max_hp']

    def show_attack(self):
        '''Show the action of enemy's attack (moves left and goes back)
        '''
        _action = actions.MoveBy((-20,0), 0.1) + actions.MoveBy((20,0), 0.1)
        self.sprite.do(_action)

    def show_under_attack(self, cri_dice=False):
        '''Show the action of enemy when attacked (shake)
        and the corresponding strike-sprite
        '''
        _action = actions.RotateBy(-15, 0.1) + actions.RotateBy(15, 0.1)
        self.sprite.do(_action)
        _sprite = materials.sprites['strike'] 
        _sprite.visible = True
        _sprite.position = 650,340
        if cri_dice==1:
            _sprite.image = const.image_from_file(
                    const.CRITICAL_STRIKE_IMG_FILE, const.GUI_ZIP_FILE)
            _sprite.do(actions.FadeOut(1.5))
        elif cri_dice==0:
            _sprite.image = const.image_from_file(
                    const.STRIKE_IMG_FILE, const.GUI_ZIP_FILE)
            _sprite.do(actions.FadeOut(1))
        elif cri_dice==2:
            _sprite.image = const.image_from_file(
                    const.SUPER_STRIKE_IMG_FILE, const.GUI_ZIP_FILE)
            _sprite.do(actions.FadeOut(2.5))
        

def gen_enemy(no=None, rank=None, zone=None, level=None):
    '''Generate a specific enemy
    '''
    # check the rank of the enemy
    if rank is None:
        _r = random.randrange(100)
        if _r <= const.ENEMY_RATE['CHIEF_BOSS']:
            rank = 3
        elif (const.ENEMY_RATE['CHIEF_BOSS']< _r 
                <= const.ENEMY_RATE['CHIEF_BOSS'] + const.ENEMY_RATE['BOSS']):
            rank = 2
        elif (const.ENEMY_RATE['CHIEF_BOSS'] + const.ENEMY_RATE['BOSS'] < 
                _r <= const.ENEMY_RATE['CHIEF_BOSS']
                + const.ENEMY_RATE['BOSS'] + const.ENEMY_RATE['ELITE']):
            rank = 1
        else:
            rank = 0

    if zone is None:
        zone = random.randrange(0,6)
    if level is None:
        level = random.randrange(1,61)

    #start to generate a enemy
    _enemy = Enemy()
    _enemy.rank = rank
    _enemy.level = level
    _enemy.zone = zone
    _enemy.value['Min_Dice'] = 1
    # get a list of enemy skills 
    _enemy_skill_no_list = []
    for _ in range(len(const.SKILL_DATA)):
        if const.SKILL_DATA[_]['owner'] == 2:
            _enemy_skill_no_list.append(_)
    # shuffle the list        
    random.shuffle(_enemy_skill_no_list)
    _list = []

    _para = const.ENEMY_PARAMETER[str(rank)]
    _enemy.value['Atk'] = int(level ** 2.5 / 27885 * _para['ATK']) + _para['ATK0']
    _enemy.value['max_hp'] = int(level ** 2.5 / 27885 * _para['MHP']) + _para['MHP0']
    _enemy.value['CriDmg'] = _para['CRIDMG']
    _enemy.value['Max_Dice'] = _para['MAX_DICE']

    _list = _enemy_skill_no_list[0:_para['SKILL_COUNT_BY_ZONE'][zone]]
    # generate a chief-boss enemy!
    if rank == 3:
        no = 0
    # here come bosses !        
    elif rank == 2:
        no = random.randrange(1,3)
    # here come elites !        
    elif rank == 1:
        no = random.randrange(3,31)
    # now comes the normal enemy        
    elif rank == 0:
        no = random.randrange(3,31)
    else:
        raise ValueError('enemy rank error:', rank)
    
    # set no for test
    #no = 29

    # now set the enemy type and confirm the Atk, CriDmg and Maxhp finally
    # firstly we set the atk
    _ = random.randrange(5)
    _enemy.type[0] = _
    _enemy.value['Atk'] *= const.ENEMY_ATK_AFFIX[_] / 100 
    _enemy.value['Atk'] *= const.ENEMY_DATA[no]['Atk'] / 100 
    # then we set the critical damage
    _ = random.randrange(5)
    _enemy.type[1] = _
    _enemy.value['CriDmg'] *= const.ENEMY_CRIDMG_AFFIX[_] / 100 
    _enemy.value['CriDmg'] *= const.ENEMY_DATA[no]['CriDmg'] / 100 
    # lastly we set the max hp
    _ = random.randrange(5)
    _enemy.type[2] = _
    _enemy.value['max_hp'] *= const.ENEMY_MAXHP_AFFIX[_] / 100 
    _enemy.value['max_hp'] *= const.ENEMY_DATA[no]['max_hp'] / 100 
    _enemy.value['max_hp'] = int(_enemy.value['max_hp']) 

    # check the enemy's passive(type 1) skills
    # other skills can be see in the battle.py
    for _ in _list:
        _enemy.skill.append(skill.Skill(_))
        # add the enemy's passive skills
        # the skill 22: strong life
        if _ == 22:
            _enemy.value['max_hp'] *= 1.5
        # the skill 23: stubborn, always have the same dice 
        if _ == 23:
            _enemy.value['Max_Dice'] = int((_enemy.value['Max_Dice'] + 1) / 2)
            _enemy.value['Min_Dice'] = _enemy.value['Max_Dice']
    _enemy.no = no
    _enemy.hp = _enemy.value['max_hp']
    materials.main_scr.sprites['enemy_sprite'].visible = True
    _enemy.sprite = materials.main_scr.sprites['enemy_sprite']
    

    # Now, get the sprite image of the enemy from the zip file
    _enemy_img_file = 'monster-' + str(_enemy.no) + '-' + str(_enemy.zone)
    #print('the enemy is', _enemy_img_file)
    # if the monster's image file is included in the zip file
    if _enemy_img_file in const.FILE_TYPE.keys():
        _enemy.sprite.image = const.image_from_file(_enemy_img_file)
    # if there is no corresponding sprite image file
    else:
        _enemy.sprite.image = const.image_from_file(
                const.DEFAULT_MONSTER_IMG_FILE)

    _enemy.sprite.anchor=_enemy.sprite.width / 2, 0

    return _enemy

def show_enemy(enemy):
    '''show the core information and skills's name of the enemy to front_layer
    '''
    if not enemy:
        return None
    materials.front_layer.labels['enemy_name_label'].element.text = (
            const.ENEMY_ATK_NAME[enemy.type[0]] + 
            const.ENEMY_CRIDMG_NAME[enemy.type[1]] + 
            const.ENEMY_MAXHP_NAME[enemy.type[2]] + '的' + 
            const.ENEMY_RANK_NAME[enemy.rank] + 
            ' ' + 
            const.ENEMY_DATA[enemy.no]['enemy_name'][enemy.zone])
    # change the color of the name label depending on the rank of the enemy
    materials.front_layer.labels['enemy_level_label'].element.text = ('LV.' + 
            ' ' + str(enemy.level))
    materials.front_layer.labels['enemy_hp_label'].element.text = (
            str(int(enemy.hp)) + '/' + str(int(enemy.value['max_hp'])))
    _str = ''
    for _ in enemy.skill:
        _str += (const.SKILL_DATA[_.skill_no]['name'] + ' ' * 4)
    materials.front_layer.labels['enemy_skill_label'].element.text = _str
