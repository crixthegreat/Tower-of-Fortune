#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/6/4 16:05:50
"""A module of TOF(tower of fortune)
"""
import copy
import random
from code import const, item, skill

class Player(object):
    """class player
    """
    def __init__(self):
        """generate a blank player with nothing 
        """
        self.name = ''
        self.level = 1
        self.hp = 100
        # item_equiped[pos]
        # 0 - main hand
        # 1 - off hand
        # 2 - head
        # 3 - shoulder
        # 4 - necklace
        # 5 - chest
        # 6 - wrist
        # 7 - glove
        # 8 - waist
        # 9 - leg
        # 10 - shoe
        # 11 - ringA
        # 12 - ringB

        # nothing equiped
        self.item_equiped = [None for _ in range(13)]
        self.gold = 1000
        self.exp = 0
        self.zone = 0
        self.status = 0
        self.epitaph = ''
        self.item_box = []
        self.game_status = 0
        self.point = 0
        self.skill = []
        # cri_dice means that the equal dice occurs
        # 0 - not occur, 1 - occured once, 2 - occured twice, 3 - occured third times(dice explode)
        self.cri_dice = 0
        self.x2 = 0
        self.x3 = 0
        self.x4 =0
        
    # the read-only property .value is calculated from all the items the player equiped    
    @property
    def value(self):
        # use the deep copy to initialise a temp value called _v
        _v = copy.deepcopy(const.PLAYER_AFFIX)
        for _ in self.item_equiped:
            if _ == None:
                continue
            _v['Atk'] += _.affix[0]
            _v['Def'] += _.affix[1]
            _v['Luc'] += _.affix[2]
            _v['Vit'] += _.affix[3]
            _v['CriDmg'] += _.affix[4]
            _v['MaxDice'] += _.affix[5]
            _v['BlockValue'] += _.affix[6]
            _v['ShortDistanceAtkDecreaseRate'] += _.affix[7]
            _v['BrambleDmg'] += _.affix[8]
            _v['HpBonusRate'] += _.affix[9]
            _v['HpRegen'] += _.affix[10]
            _v['HpAbsorb'] += _.affix[11]
            _v['HpHit'] += _.affix[12]
            _v['MagicFind'] += _.affix[13]
            _v['GoldFind'] += _.affix[14]
            _v['ExpBonus'] += _.affix[15]
            _v['ExpWhenKill'] += _.affix[16]
            _v['MinDice'] += _.affix[17]
            _v['DebuffRoundMinus'] += _.affix[18]
            _v['EliteDamage'] += _.affix[19]
        # player has a base value of 50 for the critical damage
        _v['CriDmg'] += 50

        # equiped skills of the player is stored in player.skill[]
        # the skill type details can be checked in the battle.py
        # the list .skill[] is a list of skill No.'s, start with 0
        # let's do the passive skills here
        # it's skill: 9, 10, 11, 12, 13, 14 
        # 9 - bet for life; 10 - the turtle god 
        # 11 - the dice god; 12 - dual swing; 13 - mighty hit 
        # 14 - stantard style
        for _ in self.skill:
            if _ == 9:
                _v['Atk'] += _v['Def'] / 2
            elif _ == 10:
                _v['Def'] += _v['Atk'] / 2
            elif _ == 11:
                _v['MinDice'] += 1
                if _v['MinDice'] > _v['MaxDice']:
                    _v['MinDice'] = _v['MaxDice']
            elif _ == 12:
                if self.item_equiped[0].main_type == 0 and self.item_equiped[1].main_type == 0:
                    _v['BlockValue'] += 10
            elif _ == 13:
                if self.item_equiped[0].main_type == 1:
                    _v['CriDmg'] *= 2
            elif _ == 14:
                if self.item_equiped[0].main_type == 0 and self.item_equiped[1].main_type == 2:
                    _v['HpRegen'] += self.level * 20 + 100
        return _v

    # the read-only property max_hp is calculated from Vit and HpBonusRate
    @property
    def max_hp(self):
        return int(self.value['Vit'] * 35 * (1 + self.value['HpBonusRate'] / 100))

    def equip_item(self, item):
        """equip a item to the player, and if the player has a item equiped already, add it to the item box
        """
        # main_type of the items, means the position of the item
        # 0 - single hand
        # 1 - double hand
        # 2 - off hand
        _main_type = const.ITEMS_DATA[item.type]['main_type']
        
        
        if _main_type == 0:
            _pos = 0
            self.add_to_item_box(self.item_equiped[0])
        elif _main_type == 1:
            _pos = 0
            # if occupied, add it to the item box
            self.add_to_item_box(self.item_equiped[0])
            self.add_to_item_box(self.item_equiped[1])
        elif _main_type == 2:
            _pos = 1
            if self.item_equiped[0].main_type == 1:
                self.add_to_item_box(self.item_equiped[0])
        elif  3 <= _main_type  <= 11:
            _pos = _main_type - 1
            self.add_to_item_box(self.item_equiped[_pos])
        elif _main_type == 12:
            if self.item_equiped[11]:
                if self.item_equiped[12]:
                    self.add_to_item_box(self.item_equiped[11])
                    _pos = 11
                else:
                    _pos = 12
            else:
                _pos = 11
        self.item_equiped[_pos] = item

    def add_to_item_box(self, item):
        if item:
            self.item_box.append(item)

    def equip_skill(self, *_skill):
        for _ in _skill:
            self.skill.append(skill.Skill(_))


def gen_player(level):
    """generate a player who has full-set equipment 
    """
    _player = Player()
    _player.equip_item(item.gen_random_item(0, level, 500))
    _player.equip_item(item.gen_random_item(30, level, 500))
    _player.equip_item(item.gen_random_item(40, level, 500))
    _player.equip_item(item.gen_random_item(42, level, 500))
    _player.equip_item(item.gen_random_item(43, level, 500))
    _player.equip_item(item.gen_random_item(44, level, 500))
    _player.equip_item(item.gen_random_item(46, level, 500))
    _player.equip_item(item.gen_random_item(47, level, 500))
    _player.equip_item(item.gen_random_item(48, level, 500))
    _player.equip_item(item.gen_random_item(50, level, 500))
    _player.equip_item(item.gen_random_item(51, level, 500))
    _player.equip_item(item.gen_random_item(52, level, 500))
    _player.equip_item(item.gen_random_item(52, level, 500))

    _player.hp = _player.max_hp
    return _player

def ran_dice(min_dice, max_dice, luc, level, enemy=None):
    """the most funny and mystical part of this game
    To get a dice number, the ran_dice method does with following steps:
    1. get the dice faces (dice_no = max - min + 1)
    2. get the every generating rate of the dice faces (dice_rate)
    3. generate several zones as described below:

      1,...,max_rate(0),min_rate(1),...,max_rate(1),min_rate(2),...,max_rate(2),min_rate(3),...,...,10000
    4. the span of every zones, which can even be 0, depends on the value of luc
    5. generate a random number r, if r in range(min_rate(n), max_rate(n)), the dice is min_dice + n
    the following code is written with VBA originally, so it's VB-style,
    """
    dice_no = max_dice - min_dice + 1
    # I forgot what this means
    acc_rate = 0
    # I forgot the max_luc formula..., but I still know this means the max lucky value you can get in the level
    max_luc = int(level * level / 1.8 + 1)


    dice_rate = [0 for _ in range(dice_no)]
    for _ in range(1, dice_no):
        if luc / max_luc / 2 * (_ - (max_dice + min_dice) / 2) + dice_no < 0:
            dice_rate[_ - 1] = 0
        else:
            dice_rate[_ - 1] = luc / max_luc / 2 * (_ -(max_dice + min_dice) / 2) + dice_no
        acc_rate += dice_rate[_ - 1]

    dice_rate[dice_no - 1] = dice_no * dice_no - acc_rate

    min_rate = [0 for _ in range(dice_no)]
    max_rate = [0 for _ in range(dice_no)]

    for _ in range(dice_no):
        dice_rate[_] = dice_rate[_] / dice_no / dice_no * 10000
        for _i in range(_ + 1):
            max_rate[_] += dice_rate[_i]
        for _i in range(_):
            min_rate[_] += dice_rate[_i]
        min_rate[_] += 1
        min_rate[_] = int(min_rate[_])
        max_rate[_] = int(max_rate[_])

    r = random.randrange(1,10000)
    if r > max_rate[dice_no - 1]:
        r = max_rate[dice_no -1]
    #print(dice_rate)
    #print(min_rate)
    #print(max_rate)
    for _ in range(dice_no):
        if  min_rate[_] <= r <= max_rate[_]:
            if enemy:
                skill.show_skill(90, min_dice + _)
            else:
                skill.show_skill(91, min_dice + _)

            return min_dice + _
# player function dice explode, when equal dice happened for the third time
def dice_equal(player, enemy):
    if player.cri_dice == 2:
        skill.show_skill(102)
        player.cri_dice = 0
        player.hp = player.hp / 2
        enemy.hp = enemy .hp / 2
        if player.hp < 1:
            player.hp = 1
        if enemy.hp < 1:
            enemy.hp =1
    elif player.cri_dice == 1:
        skill.show_skill(103)
    elif player.cri_dice == 0:
        skill.show_skill(104)
    
    player.cri_dice += 1

    
