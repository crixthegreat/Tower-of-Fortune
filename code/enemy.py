#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/6/7 13:50:35

import sys
import copy
import random
from code import const, skill
"""the code handling enemys
There are totally 31 types of enemys which has six zone-level each other.
The type no.1 is chief-boss enemy(rank 4)
The type no.2 and no.3 is boss enemy(rank 3)
The left 28 types of enemys are normal enemy (rank 1)
The normal type enemys can also become elites sometimes (rank 2)
The random rate of enemys above is defined by ENEMY_RATE
"""
class Enemy(object):

    def __init__(self):
        self.no = 0
        self.rank = 0
        self.level = 1
        self.skill = []
        self.zone = 0
        self.value = copy.deepcopy(const.ENEMY_AFFIX)
        # enemy has 5 type for ATK, CRIDMG and MAXHP
        # so every single kind of enemy have 125 types!
        # see the const.ENEMY_ATK_NAME,ENEMY_CRIDMG_NAME and ENEMY_MAXHP_NAME
        self.type = [2 ,2, 2]
        self.hp = self.value['max_hp']

def gen_enemy(no=None, rank=None, zone=None, level=None):
    # check the rank of the enemy
    if not rank:
        _r = random.randrange(100)
        if _r <= const.ENEMY_RATE['CHIEF_BOSS']:
            rank = 3
        elif const.ENEMY_RATE['CHIEF_BOSS']< _r <= const.ENEMY_RATE['CHIEF_BOSS'] + const.ENEMY_RATE['BOSS']:
            rank = 2
        elif const.ENEMY_RATE['CHIEF_BOSS'] + const.ENEMY_RATE['BOSS'] < _r <= const.ENEMY_RATE['CHIEF_BOSS'] + const.ENEMY_RATE['BOSS'] + const.ENEMY_RATE['ELITE']:
            rank = 1
        else:
            rank = 0

    if not zone:
        zone = random.randrange(0,6)
    if not level:
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
    # generate a chief-boss enemy!
    if rank == 3:
        no = 0
        _enemy.value['Atk'] = int(level ** 2.5 / 27885 * const.ELITE_ATK) + 100
        _enemy.value['max_hp'] = int(level ** 2.5 / 27885 * const.ELITE_MHP) + 1000
        _enemy.value['CriDmg'] = const.ELITE_CRIDMG
        _enemy.value['Max_Dice'] = 8
        # give the skill to the chief boss
        if zone == 0 or zone == 1:
            # the chief-boss has 2 skill in zone 0,1
            _list = _enemy_skill_no_list[0:2]
        elif zone == 2 or zone == 3:
            # has 3 skills in zone 2,3 and so on
            _list = _enemy_skill_no_list[0:3]
        elif zone == 4 or zone == 5:
            _list = _enemy_skill_no_list[0:4]
    # here come bosses !        
    elif rank == 2:
        no = random.randrange(1,3)
        _enemy.value['Atk'] = int(level ** 2.5 / 27885 * const.ELITE_ATK) + 100
        _enemy.value['max_hp'] = int(level ** 2.5 / 27885 * const.ELITE_MHP) + 800
        _enemy.value['CriDmg'] = const.ELITE_CRIDMG
        _enemy.value['Max_Dice'] = 7
        # give the skill to the boss
        if zone == 0 or zone == 1:
            # the chief-boss has 1 skill in zone 0,1
            _list = _enemy_skill_no_list[0:1]
        elif zone == 2 or zone == 3:
            # has 2 skills in zone 2,3 and so on
            _list = _enemy_skill_no_list[0:2]
        elif zone == 4 or zone == 5:
            _list = _enemy_skill_no_list[0:3]

    # here come elites !        
    elif rank == 1:
        no = random.randrange(3,31)
        _enemy.value['Atk'] = int(level ** 2.5 / 27885 * const.ELITE_ATK) + 100
        _enemy.value['max_hp'] = int(level ** 2.5 / 27885 * const.ELITE_MHP) + 750
        _enemy.value['CriDmg'] = const.ELITE_CRIDMG
        _enemy.value['Max_Dice'] = 7

        # give the skill to the elite
        if zone == 0 or zone == 1:
            # the elite has 1 skill in zone 0,1
            _list = _enemy_skill_no_list[0:1]
        elif zone == 2 or zone == 3:
            # has 2 skills in zone 2,3 and so on
            _list = _enemy_skill_no_list[0:2]
        elif zone == 4 or zone == 5:
            _list = _enemy_skill_no_list[0:3]

    # now comes the normal enemy        
    elif rank == 0:
        no = random.randrange(3,31)
        _enemy.value['Atk'] = int(level ** 2.5 / 27885 * const.NORMAL_ATK) + 30
        _enemy.value['max_hp'] = int(level ** 2.5 / 27885 * const.NORMAL_MHP) + 500
        _enemy.value['CriDmg'] = const.NORMAL_CRIDMG
        _enemy.value['Max_Dice'] = 6
    else:
        print('enemy rank error:', rank)
        sys.exit()
    
    # now set the enemy type and confirm the Atk, CriDmg and Maxhp finally
    # firstly we set the atk
    _ = random.randrange(5)
    _enemy.type[0] = _
    _enemy.value['Atk'] = _enemy.value['Atk'] * const.ENEMY_ATK_AFFIX[_] / 100 
    _enemy.value['Atk'] = _enemy.value['Atk'] * const.ENEMY_DATA[no]['Atk'] / 100 
    # then we set the critical damage
    _ = random.randrange(5)
    _enemy.type[1] = _
    _enemy.value['CriDmg'] = _enemy.value['CriDmg'] * const.ENEMY_CRIDMG_AFFIX[_] / 100 
    _enemy.value['CriDmg'] = _enemy.value['CriDmg'] * const.ENEMY_DATA[no]['CriDmg'] / 100 
    # lastly we set the max hp
    _ = random.randrange(5)
    _enemy.type[2] = _
    _enemy.value['max_hp'] = _enemy.value['max_hp'] * const.ENEMY_MAXHP_AFFIX[_] / 100 
    _enemy.value['max_hp'] = int(_enemy.value['max_hp'] * const.ENEMY_DATA[no]['max_hp'] / 100) 

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
            _enemy.value['Max_Dice'] = int((_enemy.value['Max_Dice'] + _enemy.value['Min_Dice'] + 1) / 2)
            _enemy.value['Min_Dice'] = _enemy.value['Max_Dice']
    _enemy.no = no
    _enemy.hp = _enemy.value['max_hp']
    return _enemy

def show(enemy):
    if not enemy:
        return None
    print(const.ENEMY_ATK_NAME[enemy.type[0]] + const.ENEMY_CRIDMG_NAME[enemy.type[1]] + const.ENEMY_MAXHP_NAME[enemy.type[2]] + '的' + const.ENEMY_RANK_NAME[enemy.rank])
    print ('LEVEL', enemy.level)
    print(const.ENEMY_DATA[enemy.no]['enemy_name'][enemy.zone] + '在' + const.ZONE_NAME[enemy.zone] + '出现了')
    print(enemy.value)
    print('它拥有技能：')
    for _ in enemy.skill:
        print(const.SKILL_DATA[_.skill_no]['name'])
