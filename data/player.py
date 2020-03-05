#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/6/4 16:05:50
"""A module of TOF(tower of fortune)
"""
import copy
import random
from cocos import actions
from data import const, item, skill, battle, enemy
import materials
from materials.front_layer import show_message

class Player(object):
    """class player
    """
    def __init__(self, sprite=None):
        """generate a blank player with nothing 
        """
        self.name = 'judy'
        self.level = 1
        self.hp = 100
        self.sprite = sprite 
        self.vx = 0
        self.vy = 0
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
        # born with nothing equiped
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
        # 0 - not occur, 1 - occured once, 2 - occured twice, 
        # 3 - occured third times(dice explodes)
        self.cri_dice = 0
        self.loot = []
        self.save_slot = 0
        self.alive = True

        self.actived_buff = []
        
    # the read-only property .value is calculated from all the items 
    # which the player equiped and passive skills
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
            if _ is None:
                continue
            if _.skill_no == 9:
                _v['Atk'] += _v['Def'] / 2
            elif _.skill_no == 10:
                _v['Def'] += _v['Atk'] / 2
            elif _.skill_no == 11:
                _v['MinDice'] += 1
                if _v['MinDice'] > _v['MaxDice']:
                    _v['MinDice'] = _v['MaxDice']
            elif _.skill_no == 12:
                # if dual-swing
                if (self.item_equiped[0].main_type == 0 
                        and self.item_equiped[1].main_type == 0):
                    _v['BlockValue'] += 10
            elif _.skill_no == 13:
                # if double-handed
                if self.item_equiped[0].main_type == 1:
                    _v['CriDmg'] *= 2
            elif _.skill_no == 14:
                # if a single-weapon and a shield
                if (self.item_equiped[0].main_type == 0 
                        and self.item_equiped[1].main_type == 2):
                    _v['HpRegen'] += self.level * 20 + 100
        return _v

    # the read-only property max_hp is calculated from Vit and HpBonusRate
    @property
    def max_hp(self):
        return int(self.value['Vit'] * 35 * (1 + self.value['HpBonusRate'] / 100))

    # the read-only property skill_quantity is decided by the player's level
    # you get n skills when your level is:
    # n=1, lv 1-9
    # n=2, lv 10-30
    # n=3, lv 31-50
    # n=4, lv 51-60
    @property
    def skill_quantity(self):
        _lv = self.level
        for _, _item in const.SKILL_COUNT_BY_LEVEL.items():
            if  _[0] <= _lv <= _[1]:
                return _item
        raise ValueError('unexpected player level: ', _lv)

    def equip_item(self, item):
        """equip a item to the player, and move the corresponding item 
        to the item box
        """
        # main_type of the items, means the position of the item
        # 0 - single hand
        # 1 - double hand
        # 2 - off hand
        _main_type = const.ITEMS_DATA[item.type]['main_type']
        
        # when a single hand weapon equiped, the off hand item is moved 
        # into the item box
        if _main_type == 0:
            _pos = 0
            if self.item_equiped[0]:
                if const.ITEMS_DATA[self.item_equiped[0].type]['main_type'] == 1:
                    self.add_to_item_box(self.item_equiped[0])
                else:
                    self.add_to_item_box(self.item_equiped[1])
                    self.item_equiped[1] = copy.deepcopy(self.item_equiped[0])
        # deals with the double-hand weapons 
        elif _main_type == 1:
            _pos = 0
            self.add_to_item_box(self.item_equiped[0])
            self.add_to_item_box(self.item_equiped[1])
            self.item_equiped[1] = None
        # deals with the shiled
        elif _main_type == 2:
            _pos = 1
            self.add_to_item_box(self.item_equiped[1])
            if self.item_equiped[0].main_type == 1:
                self.add_to_item_box(self.item_equiped[0])
                self.item_equiped[0] = None
        # deals with the others
        elif  3 <= _main_type  <= 11:
            _pos = item.equiped_pos
            self.add_to_item_box(self.item_equiped[_pos])
        # deals with the rings
        elif _main_type == 12:
            _pos = 11
            self.add_to_item_box(self.item_equiped[12])
            self.item_equiped[12] = copy.deepcopy(self.item_equiped[11])
        # now equip the item
        self.item_equiped[_pos] = item

    def add_to_item_box(self, item):
        """as the name says
        if the item box is full, the item disappear
        """
        if item and len(self.item_box) < const.MAX_ITEM_BOX:
            self.item_box.append(item)
            return True
        else:
            return False

    def equip_skill(self, *_skill):
        '''equip a skill (list)
        '''
        for _ in _skill:
            self.skill.append(skill.Skill(_))

    def show_dice(self, _dice, enemy=False):
        '''show the dice sprites
        '''
        if enemy:
            _sprite_name = 'enemy_dice_' + str(self.cri_dice)
        else:
            _sprite_name = 'player_dice_' + str(self.cri_dice)
        _sprite = materials.main_scr.sprites[_sprite_name]
        _sprite.image = materials.dice_image[_dice - 1]
        _sprite.visible = True

        if self.cri_dice == 0:
            if enemy:
                materials.main_scr.sprites['enemy_dice_1'].visible = False
                materials.main_scr.sprites['enemy_dice_2'].visible = False
            else:
                materials.main_scr.sprites['player_dice_1'].visible = False
                materials.main_scr.sprites['player_dice_2'].visible = False
        elif self.cri_dice == 1:
            if enemy:
                materials.main_scr.sprites['enemy_dice_2'].visible = False
            else:
                materials.main_scr.sprites['player_dice_2'].visible = False
         

    def show_player(self):
        '''show the core data and skills of the player
        '''
        _labels = materials.front_layer.labels
        _labels['level_label'].element.text = str(self.level)
        _labels['hp_label'].element.text = (str(int(self.hp)) + '/' + 
                str(self.max_hp))
        _labels['exp_label'].element.text = (str(int(self.exp)) + '/' + 
                str(int(self.level ** 3.5) + 300))
        _labels['gold_label'].element.text = str(int(self.gold))
        _str = ''
        for _ in range(self.skill_quantity):
            if self.skill[_]:
                _str += const.SKILL_DATA[self.skill[_].skill_no]['name']
            else:
                _str += '未定'
            _str += ' ' * 4
        _labels['player_skill_label'].element.text = _str

    def show_attack(self):
        '''show the attack action of the player
        '''
        _action = actions.MoveBy((20,0), 0.1) + actions.MoveBy((-20,0), 0.1)
        self.sprite.do(_action)

    def show_under_attack(self, cri_dice):
        '''show the action and the sprites when the player is attacked
        '''
        _action = actions.RotateBy(15, 0.1) + actions.RotateBy(-15, 0.1)
        self.sprite.do(_action)
        _sprite = materials.sprites['strike']
        _sprite.visible = True
        _sprite.position = 200,340
        if cri_dice==1:
            _sprite.image = const.image_from_file(const.CRITICAL_STRIKE_IMG_FILE, 
                    const.GUI_ZIP_FILE)
            _sprite.do(actions.FadeOut(1.5))
        elif cri_dice==0:
            _sprite.image = const.image_from_file(const.STRIKE_IMG_FILE, 
                    const.GUI_ZIP_FILE)
            _sprite.do(actions.FadeOut(1))
        elif cri_dice==2:
            _sprite.image = const.image_from_file(const.SUPER_STRIKE_IMG_FILE, 
                    const.GUI_ZIP_FILE)
            _sprite.do(actions.FadeOut(2.5))

    def sell_item(self, _item):
        # the price of a item is:
        # level * 10 * (rare_type + 1)
        _price = _item.level * (_item.rare_type + 1) * 10
        self.gold += _price
        materials.front_layer.labels['gold_label'].element.text = (
                str(int(self.gold)))
    
    # add None to the unsettled skill slot 
    def update_skill(self):
        _no = len(self.skill)
        print('now add NONE for ', self.skill_quantity - _no)
        for _ in range(self.skill_quantity - _no):
            self.skill.append(None)

    def player_to_dict(self):
        """Turn the player object into a dictionary for game saving 
        """
        # turn the player's attribution into a dict
        _data = dict()
        _item_equiped_list = []
        _item_box_list = []
        _skill_list = []
        # use the item_to_dict function to turn a item object into a dictionary
        for _ in self.item_equiped:
            # the off-hand item can be nothing
            if _:
                _item_equiped_list.append(_.item_to_dict())
            else:
                _item_equiped_list.append(None)
        for _ in self.item_box:
            _item_box_list.append(_.item_to_dict())
        # for skills, just store the Number of the skills
        for _ in self.skill:
            # the player's skill list can also contains None 
            # (when the skill is not assigned)
            if _:
                _skill_list.append(_.skill_no)
            else:
                _skill_list.append(None)

        # the KEY of the save_data dictionary is the 'slotX' (X is 0 ~ 8)
        return dict(
                player_level=self.level, 
                hp=self.hp, 
                item_equiped=_item_equiped_list, 
                gold=self.gold, 
                exp=self.exp, 
                zone=self.zone, 
                alive=self.alive, 
                epitaph=self.epitaph, 
                item_box=_item_box_list, 
                skill=_skill_list
                )

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
    _player.level = level
    _player.sprite = materials.main_scr.sprites['player_sprite']
    _player.exp = 0

    _player.update_skill()
    # add 54 random items to player's item box for test
    #for _ in range(54):
    #    _player.item_box.append(item.gen_random_item())

    return _player

def ran_dice(min_dice, max_dice, luc, level):
    """the most funny and mystical part of this game
    To get a dice number, the ran_dice method does with following steps:
    1. get the dice faces (dice_no = max - min + 1)
    2. get the every generating rate of the dice faces 
       dice_rate: [dice_rate[0], dice_rate[1],...,dice_rate[dice_no - 1]]
    3. generate every dice-zones as described below:
        [dice_rate[0], dice_rate[0]+dice_rate[1], 
        dice_rate[0]+dice_rate[1]+dice_rate[2],
        ...,
        dice_rate[0]+dice_rate[1]+...+[dice_rate[dice_no -1]]]
    4. throw a dice of 10000
    5. return the ran_dice value , depending on where the dice locates 
    6. the key parts is how to calculte the dice_rate for every numbers 
        using the lucky value 'luc'
    7. here is the formula:
        (1) dice_rate[_] = base_rate[_] * 
            (1 + luc /  max_luc * ((dice_no - _ - 1) * 0.4 + 0.6))
        (2) the _ is counted from the big number to the small one
        (3) so, basically, the dice_rate of a number becomes bigger 
            when your 'luc' value is bigger.
            if you got the maxism lucky value ('max_luc'), 
            the biggest number's rate becomes 1.5 times of base_rate, 
            the second biggest number's rate becomes 1.7 times of base_rate, 
            and so on.
        (4) when the dice_rate accumlated is bigger than 10000, 
            the left numbers' rate becomes 0, which means you won't get these 
            small numbers
    """
    # dice_no is the faces of the dice
    dice_no = max_dice - min_dice + 1
    # acc_rate is the accumlation of the 'dice_rate's
    acc_rate = 0
    # max_luc is the largest value you can get when you are in level 'level'
    # the number 13 means that you can equip 13 items which have the luc affix
    # the formula below is the same as the one in the skill.py where the items are defined
    max_luc =  int(level ** 3 /1500 + 10 + level) * 13

    # when the luc is 0, this is a normal dice, every number has the same base rate
    base_rate = [10000 / dice_no  for _ in range(dice_no)]
    dice_rate = [0 for _ in range(dice_no)]

    # now change the every number's rate from the big number to the small number
    for _ in range(dice_no-1, -1, -1):
        dice_rate[_] = base_rate[_] * (1 + luc /  max_luc * ((dice_no - _ - 1) * 0.2 + 0.5))
        if acc_rate + dice_rate[_] >= 10000:
            dice_rate[_] = 10000 - acc_rate
            break
        else:
            acc_rate += dice_rate[_]

    for _ in range(1,dice_no):
        dice_rate[_] += dice_rate[_ -1]

    #print(dice_rate)
    r = random.randrange(1,10000)
    #print('raw r is:', r)
    for _ in range(dice_no):
        if  r < dice_rate[_]:
            return min_dice + _

    raise ValueError('ran dice error!')

# player function dice explode, when equal dice happened for the third time
def dice_equal(player, _enemy):
    if player.cri_dice == 2:
        show_message(const.BATTLE_MESSAGE['DiceDueceThirdTime'])
        player.cri_dice = 0
        player.hp = player.hp / 2
        _enemy.hp = _enemy .hp / 2
        if player.hp < 1:
            player.hp = 1
        if _enemy.hp < 1:
            _enemy.hp =1
        materials.sprites['strike'].visible = True
        materials.sprites['strike'].position = 400,234
        materials.sprites['strike'].image = (
                const.image_from_file(const.EXPLODE_IMG_FILE, 
                    const.GUI_ZIP_FILE))
        materials.sprites['strike'].do(
                actions.MoveBy((0,100),1.3) + 
                actions.MoveBy((0,-100),1.3) + 
                actions.FadeOut(0.5))
        battle.show_hp_change(player, _enemy, 2, 0-int(player.hp/2), 
                0-int(_enemy.hp/2))
        enemy.show_enemy(_enemy)
    elif player.cri_dice == 1:
        show_message(const.BATTLE_MESSAGE['DiceDueceTwice'])
    elif player.cri_dice == 0:
        show_message(const.BATTLE_MESSAGE['DiceDuece'])
    
    player.cri_dice += 1


def dict_to_player(_data):
    """Turn a dict data to a player object for game loading
    """
    _player = Player(materials.main_scr.sprites['player_sprite'])
    # load the property
    _player.level = _data['player_level']
    _player.hp = _data['hp']
    _player.gold = _data['gold']
    _player.exp = _data['exp']
    _player.zone = _data['zone']
    _player.alive = _data['alive']
    _player.epitaph = _data['epitaph']
    # load the skills ('s number)
    _player.skill = []
    for _ in _data['skill']:
        if _ is None:
            _player.skill.append(None)
        else:
            _player.skill.append(skill.Skill(_))
    # load the items with item.dict_to_item() method
    _player.item_equiped = []
    for _ in _data['item_equiped']:
        if _:
            _player.item_equiped.append(item.dict_to_item(_))
        else:
            _player.item_equiped.append(None)

    _player.item_box = []
    for _ in _data['item_box']:
        _player.item_box.append(item.dict_to_item(_))

    return _player



