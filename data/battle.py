#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/6/7 22:59:49

import sys
import random
from data import const, player, item, enemy, skill
import materials
from materials.front_layer import show_message
from cocos import actions


def player_attack(_player, _enemy, attack_style):
    """calculate the attack action
    attack_style = [0,8] means the 9 kind of attack styles
    """
    #for _ in range(3):
    #    materials.main_scr.sprites['player_dice_' + str(_)].visible = False
    #    materials.main_scr.sprites['enemy_dice_' + str(_)].visible = False

    # firstly let's check the attack style
    if materials.sprites['strike'].are_actions_running():
        #print(materials.sprites['strike'].are_actions_running())
        return True
    #show_message(const.ATTACK_STYLE_DATA[attack_style]['name'])
    _min_dice = _player.value['MinDice']
    _max_dice = _player.value['MaxDice']
    _atk = _player.value['Atk'] * (1 + const.ATTACK_STYLE_DATA[attack_style]['Atk'] / 100)
    _def = _player.value['Def'] * (1 + const.ATTACK_STYLE_DATA[attack_style]['Def'] / 100)
    _luc = _player.value['Luc'] * (1 + const.ATTACK_STYLE_DATA[attack_style]['Luc'] / 100)

    _cri_dmg = _player.value['CriDmg']
    _block_value = _player.value['BlockValue']
    _regen = _player.value['HpRegen']

    # special handling for '神鬼奇谋'
    if attack_style == 8 and _max_dice < 9:
        _max_dice += 1
    
    # The skill has 3 types:
    # type 1: get when be born,trigger at a rate, see the details in the player.py (Player Class - def value()) and the enemy.py
    # type 2: get when attack the enemy at a rate, last for [round_last] rounds
    # type 3: get when attacked by the enemy at a rate, last for [round_last] rounds

    # check the enemy's skill list before attack
    # when casted , use the method skill.casted too
    for _ in _enemy.skill:
        # skill 18: make the player max_dice half
        if _.skill_no == 18 and _.actived:
            if (_max_dice % 2):
                _max_dice = (_max_dice + 1) / 2
            else:
                _max_dice = _max_dice / 2
            _max_dice = int(_max_dice)
            if _max_dice < _min_dice:
                _max_dice = _min_dice
            skill.show_skill(_.skill_no, const.ENEMY_DATA[_enemy.no]['enemy_name'][_enemy.zone])        
            _.round_last -= 1
            if _.round_last == 0:
                _.reset()
    # hp regen
    if _regen:
        _player.hp += _regen
        skill.show_skill(92, int(_regen))
        if _player.hp > _player.max_hp:
            _player.hp = _player.max_hp
    # now throw the dice
    _player_dice = player.ran_dice(_min_dice, _max_dice, _luc, _player.level)
    _player.show_dice(_player_dice)
    _enemy_dice =  player.ran_dice(_enemy.value['Min_Dice'], _enemy.value['Max_Dice'], _enemy.value['Luc'], _enemy.level, 1)
    _player.show_dice(_enemy_dice,True)

    # now check the skill 0: throw the dice again
    if _player_dice < _enemy_dice:
        for _ in _player.skill:
            if _.skill_no == 0:
                if _.actived:
                    skill.show_skill(_.skill_no)
                    _player_dice = player.ran_dice(_min_dice, _max_dice, _luc, _player.level)
                    _enemy_dice =  player.ran_dice(_enemy.value['Min_Dice'], _enemy.value['Max_Dice'], _enemy.value['Luc'], _enemy.level, 1)
                    _.round_last -= 1
                    if _.round_last == 0:
                        _.reset()
                else:
                    if _.test():
                        _.actived = True
            
    # now check:
    # the skill 3: war cry to make enemy take the min dice!        
    # the skill 7,  
    for _ in _player.skill:
        if _.skill_no == 3:
            if not(_.actived) and _.test():
                _.actived = True
            if _.actived:
                _enemy_dice = _enemy.value['Min_Dice']
                skill.show_skill(_.skill_no, _enemy_dice)
                _.round_last -= 1
                if _.round_last == 0:
                    _.reset()
        elif _.skill_no == 7:
            if not(_.actived) and _.test():
                _.actived = True
            if _.actived:
                _cri_dmg = _cri_dmg * (2 - _player.hp / _player.max_hp)
                _.round_last -= 1
                if _.round_last == 0:
                    _.reset()

    # check the skill 17: the big wall
    _big_wall = False
    for _ in _enemy.skill:
        if _.skill_no == 17 and _.actived:
            skill.show_skill(_.skill_no)
            _.round_last -= 1
            _big_wall = True
            if _.round_last == 0:
                _.reset()

    # now check the dice value between each other at last!
    if _player_dice == _enemy_dice:
        player.dice_equal(_player, _enemy)
    
        _dmg = 0
    # now attempt to start the attack actions!
    else:
        if not _big_wall:
            if _player_dice > _enemy_dice:
                # the normal attack damage value
                _player.show_attack()
                _dmg = _atk * (1 - _enemy.value['Def'] / (_enemy.value['Def'] + 1500)) * (1 + (_player_dice - _enemy_dice) * 0.1)
                for _ in _player.skill:
                    # check the skill 2: poison weapon!
                    if _.skill_no == 2:
                        if not _.actived and _.test():
                            _.actived = True
                        if _.actived:
                            skill.show_skill(_.skill_no)
                            _dmg = _dmg * 1.5
                            _.round_last -= 1
                            if _.round_last == 0:
                                _.reset()
                        # check the skill 8: revenge attack!
                    elif _.skill_no == 8 and _.actived:
                        skill.show_skill(_.skill_no)
                        _dmg = _dmg * 2
                        _.round_last -= 1
                        if _.round_last == 0:
                            _.reset()

                if _player.cri_dice == 2:
                    skill.show_skill(100)
                    # the critical and doubled attack !
                    _dmg = _dmg * (1+ _cri_dmg / 100) * 2
                elif _player.cri_dice == 1:
                    skill.show_skill(101)
                    # the critical attack
                    _dmg = _dmg * (1 + _cri_dmg / 100)
                else:
                    for _ in _player.skill:
                        # skill 1: you can do critical attacks
                        if _.skill_no == 1:
                            if not(_.actived):
                                if _.test() and random.randrange(1,101) <= (_luc / 100 + 5):
                                    _.actived = True
                            if _.actived:
                                skill.show_skill(105)
                                _dmg = _dmg * (1 + _cri_dmg / 100)
                                _.round_last -= 1
                                if _.round_last == 0:
                                    _.reset()
                            else:
                                skill.show_skill(106)

                for _ in _enemy.skill:
                    # check the skill 15: no weapon!
                    if _.skill_no == 15 and _.actived:
                        skill.show_skill(_.skill_no)
                        _dmg = 0
                    # skill 19: the shield
                    if _.skill_no == 19:
                        if not _.actived and _.test():
                            _.actived = True
                        if _.actived:
                            skill.show_skill(_.skill_no)
                            _dmg = 0
                    # skill 20: the bounce back attack
                    if _.skill_no == 20:
                        if not _.actived and _.test():
                            _.actived = True
                        if _.actived:
                            _back_dmg = _dmg / 2.5 * (1 - _def / (_def + 1500))
                            skill.show_skill(_.skill_no, _back_dmg)
                            _player.hp -= _back_dmg
                    # skill 21: the plague
                    if _.skill_no == 21:
                        if not _.actived and _.test():
                            _.actived = True
                            skill.show_skill(21.5)

                if _player.hp <= 0:
                    return battle_result(_player, _enemy, 2)
                # check the Elite Damage affix
                _dmg = _dmg * (1 + _player.value['EliteDamage'] / 100)

                _enemy.hp -= _dmg
                if _dmg:
                    show_message('怪物失去了体力：' + str(int(_dmg)))
                    #def show_hp_change(_player=None, _enemy=None, cri_dice=0, _player_dmg=0, _enemy_dmg=0):
                    show_hp_change(None, _enemy, _player.cri_dice, 0, (0-int(_dmg)))
                    materials.front_layer.labels['enemy_hp_label'].element.text = str(int(_enemy.hp)) + ' / ' + str(int(_enemy.value['max_hp']))
                    _enemy.show_under_attack(_player.cri_dice)
                if _enemy.hp <= 0:
                    return battle_result(_player, _enemy, 1)
                
                if (_player.value['HpHit'] or _player.value['HpAbsorb']) and _dmg:
                    _player.hp += _player.value['HpHit']
                    _player.hp += _player.value['HpAbsorb'] / 100 * _dmg
                    skill.show_skill(110)
                    if _player.hp > _player.max_hp:
                        _player.hp = _player.max_hp
            # the enemy attack!
            else:
                _enemy.show_attack()
                _dmg = _enemy.value['Atk'] * (1 - _def / (_def + 1500) * (1 + (_enemy_dice - _player_dice) * 0.1)) * (1 - _player.value['ShortDistanceAtkDecreaseRate'] / 100)
                if _player.cri_dice == 2:
                    skill.show_skill(107)
                    # the critical and doubled attack !
                    _dmg = _dmg * 2
                    # check the skill 8 when the player got a critical attack!
                    for _ in _player.skill:
                        if _.skill_no == 8 and _.test():
                            _.actived = True
                elif _player.cri_dice == 1:
                    skill.show_skill(108)
                    # the critical attack
                    _dmg = _dmg * 1.5
                    # check the skill 8 when the player got a critical attack!
                    for _ in _player.skill:
                        if _.skill_no == 8 and _.test():
                            _.actived = True
                else:
                    skill.show_skill(109)
                
                _shield_wall = False
                for _ in _enemy.skill:
                    # check the skill 4: the shield wall
                    if _.skill_no == 4:
                        if not(_.actived) and _.test():
                            _.actived = True
                        if _.actived:
                            _block_value = _block_value * 2
                            skill.show_skill(_.skill_no)
                            if random.randrange(1,101) <= _block_value:
                                _dmg = _dmg / 4
                                _shield_wall = True
                            _.round_last -= 1
                            if _.round_last == 0:
                                _.reset()
                if not _shield_wall and _block_value and random.randrange(1,101) <= _block_value:
                    _dmg = _dmg / 2


                if _player.hp <= _dmg:
                    for _ in _player.skill:
                        # check the skill 5, divine shield
                        if _.skill_no == 5:
                            if not(_.actived) and _.test():
                                _.actived = True
                            if _.actived:
                                _dmg = 0
                                skill.show_skill(_.skill_no)
                                _.round_last -= 1
                                if _.round_last == 0:
                                    _.reset()
                        # check the skill 6, sparking bullet
                        if _.skill_no == 6:
                            if not(_.actived) and _.test():
                                _.actived = True
                            if _.actived:
                                _enemy.hp -= _player.hp / 4
                                skill.show_skill(_.skill_no)
                                _.round_last -= 1
                                if _.round_last == 0:
                                    _.reset()

                # check the skill 15: rob the weapon!
                # check the skill 16: set fire!
                # check the skill 17: set wall!
                # check the skill 18: diable you!
                for _ in _enemy.skill:
                    if _.skill_no == 15 and (not _.actived) and _.test():
                        skill.show_skill(15.5)
                        _.actived = True
                    if _.skill_no == 16 and (not _.actived) and _.test():
                        skill.show_skill(_.skill_no)
                        _.actived = True
                    if _.skill_no == 17 and (not _.actived) and _.test():
                        skill.show_skill(17.5)
                        _.actived = True
                    if _.skill_no == 18 and (not _.actived) and _.test():
                        skill.show_skill(18.5, const.ENEMY_DATA[_enemy.no]['enemy_name'][_enemy.zone])
                        _.actived = True
                        

                if _dmg:
                    _player.hp -= _dmg
                    _player.show_under_attack(_player.cri_dice)
                    #def show_hp_change(_player=None, _enemy=None, cri_dice=0, _player_dmg=0, _enemy_dmg=0):
                    show_hp_change(_player, None, _player.cri_dice, (0-int(_dmg)))
                    show_message('你失去了体力：' +str(int(_dmg)))

        _player.cri_dice = 0
    
    # check the skill 15, 16, 19, 20, 21 let  the round_last + 1 
    for _ in _enemy.skill:
        if _.skill_no == 16 and _.actived:
            skill.show_skill(16.5)
            _player.hp -= _.round_last * 0.5 * _enemy.value['Atk'] * ( 1 - _def / (_def + 1500))
            _.round_last -= 1
            if _.round_last == 0:
                _.reset()

        if _.skill_no == 15 and _.actived:
            _.round_last -= 1
            if _.round_last == 0:
                _.reset()

        if _.skill_no == 19 and _.actived:
            _.round_last -= 1
            if _.round_last == 0:
                _.reset()

        if _.skill_no == 20 and _.actived:
            _.round_last -= 1
            if _.round_last == 0:
                _.reset()

        if _.skill_no == 21 and _.actived:
            skill.show_skill(_.skill_no)
            _player.hp -= 0.2 * _enemy.value['Atk'] * (1 - _def / (_def + 1500))
            _.round_last -= 1
            if _.round_last == 0:
                _.reset()

    if _player.hp <= 0:
        return battle_result(_player, _enemy, 2)
    if _enemy.hp <= 0:
        return battle_result(_player, _enemy, 1)

    #show_message('player:' + str(int(_player.hp)) + '/' + str(_player.max_hp) + const.ENEMY_DATA[_enemy.no]['enemy_name'][_enemy.zone] + str(int(_enemy.hp)) + '/'+ str(_enemy.value['max_hp']))
    
    _player.show_player()

    
    return True

# handling the battle result with _result:
# 1 - player winned
# 2 - enemy winned
def battle_result(_player, _enemy, _result):
    _loot_mf = _player.value['MagicFind']
    _loot_no = 0
    if _result == 1:
        show_message('你击败了', const.ENEMY_DATA[_enemy.no]['enemy_name'][_enemy.zone])
        #materials.main_scr.sprites['enemy_sprite'].do(actions.Blink(5,1))
        materials.main_scr.sprites['enemy_sprite'].image = materials.main_scr.images['rip']

        if _player.level - _enemy.level <= 2:
            _exp = 50 + _player.value['ExpWhenKill']
            _gold = 50
        elif _player.level - _enemy.level <= 4:
            _exp = (50 + _player.value['ExpWhenKill']) * 0.75
            _gold = 50 * 0.75
        elif _player.level - _enemy.level <= 7:
            _exp = (50 + _player.value['ExpWhenKill']) * 0.5
            _gold = 50 * 0.5
        elif _player.level - _enemy.level <= 9:
            _exp = (50 + _player.value['ExpWhenKill']) * 0.3
            _gold = 50 * 0.3
        else:
            _exp = 0
            _gold = 2

        if _enemy.rank == 0:
            _loot_no = random.randrange(2)
        elif _enemy.rank == 1:
            _exp *= 2
            _gold *= 2
            _loot_no = random.randrange(2,6)
            _loot_mf *= 2
        elif _enemy.rank == 2:
            _exp *= 2.5
            _gold *= 2.5
            _loot_no = random.randrange(2,6)
            _loot_mf *= 2.5
        elif _enemy.rank == 3:
            _exp *= 3
            _gold *= 3
            _loot_no = random.randrange(3,9)
            _loot_mf *= 2.5
        else:
            show_message('enemy rank error in battle.py')
            sys.exit()
        
        _exp *= (_player.value['ExpBonus'] / 100 + 1)
        
        if _player.level == 60:
            _exp = 0

        _gold *= (_player.value['GoldFind'] / 100 + 1)
        
        _player.gold += _gold
        _player.exp += _exp
        show_message('你获得了金钱 {}，经验 {}'.format(int(_gold), int(_exp)))

        _max_exp = int(_player.level ** 3.5) + 300
        if _player.exp >= _max_exp:
            show_message('你升级了，战斗让你更加强大！')
            _player.level += 1
            _player.exp = 0
            _player.hp = _player.max_hp

        _loot_list = []
        for _ in range(_loot_no):
            _loot_list.append(item.gen_random_item(None, _enemy.level, _loot_mf))
        
        for _ in _loot_list:
            _player.loot.append(_)

        if _loot_no:
            show_message('怪物掉落了些好东西')
            print('equip_pos:',_loot_list[0].equiped_pos)
            item.show(_loot_list[0], _player.item_equiped[_loot_list[0].equiped_pos])



        _player.cri_dice = 0
    elif _result == 2:
        show_message('你死亡了！怪物在你身边发出荡笑...')
    return False

def show_hp_change(_player=None, _enemy=None, cri_dice=0, _player_dmg=0, _enemy_dmg=0):
    if _player:
        if cri_dice==1:
            materials.front_layer.labels['player_hp_change_label'].element.font_size = 30
            materials.front_layer.labels['player_hp_change_label'].element.color = const.ORANGE_COLOR
            materials.front_layer.labels['player_hp_change_label'].element.text = str(_player_dmg)
            materials.front_layer.labels['player_hp_change_label'].element.x = 150
            materials.front_layer.labels['player_hp_change_label'].element.y = 320
            materials.front_layer.labels['player_hp_change_label'].visible = True
            if not materials.front_layer.labels['player_hp_change_label'].are_actions_running():
                materials.front_layer.labels['player_hp_change_label'].do(actions.MoveBy((-100,0),0.3) + actions.FadeOut(0.3) + actions.MoveBy((100,0),0.3))
            else:
                materials.front_layer.labels['player_hp_change_label'].visible = False

        elif cri_dice==0:
            materials.front_layer.labels['player_hp_change_label'].element.font_size = 26
            materials.front_layer.labels['player_hp_change_label'].element.color = const.DEFAULT_COLOR
            materials.front_layer.labels['player_hp_change_label'].element.text = str(_player_dmg)
            materials.front_layer.labels['player_hp_change_label'].element.x = 150
            materials.front_layer.labels['player_hp_change_label'].element.y = 320
            materials.front_layer.labels['player_hp_change_label'].visible = True
            if not materials.front_layer.labels['player_hp_change_label'].are_actions_running():
                materials.front_layer.labels['player_hp_change_label'].do(actions.MoveBy((-80,0),0.3) + actions.FadeOut(0.3) + actions.MoveBy((80,0),0.3))
            else:
                materials.front_layer.labels['player_hp_change_label'].visible = False
        elif cri_dice==2:
            materials.front_layer.labels['player_hp_change_label'].element.font_size = 36
            materials.front_layer.labels['player_hp_change_label'].element.color = const.HIGHLIGHT_COLOR
            materials.front_layer.labels['player_hp_change_label'].element.text = str(_player_dmg)
            materials.front_layer.labels['player_hp_change_label'].element.x = 150
            materials.front_layer.labels['player_hp_change_label'].element.y = 320
            materials.front_layer.labels['player_hp_change_label'].visible = True
            if not materials.front_layer.labels['player_hp_change_label'].are_actions_running():
                materials.front_layer.labels['player_hp_change_label'].do(actions.MoveBy((-100,0),0.3) + actions.FadeOut(0.3) + actions.MoveBy((100,0),0.3))
            else:
                materials.front_layer.labels['player_hp_change_label'].visible = False
    if _enemy:
        if cri_dice==1:
            materials.front_layer.labels['enemy_hp_change_label'].element.font_size = 30
            materials.front_layer.labels['enemy_hp_change_label'].element.color = const.ORANGE_COLOR
            materials.front_layer.labels['enemy_hp_change_label'].element.text = str(_enemy_dmg)
            materials.front_layer.labels['enemy_hp_change_label'].element.x = 600
            materials.front_layer.labels['enemy_hp_change_label'].element.y = 320
            materials.front_layer.labels['enemy_hp_change_label'].visible = True
            if not materials.front_layer.labels['enemy_hp_change_label'].are_actions_running():
                materials.front_layer.labels['enemy_hp_change_label'].do(actions.MoveBy((100,0),0.3) + actions.FadeOut(0.3) + actions.MoveBy((-100,0),0.3))
            else:
                materials.front_layer.labels['enemy_hp_change_label'].visible = False
        elif cri_dice==0:
            materials.front_layer.labels['enemy_hp_change_label'].element.font_size = 26
            materials.front_layer.labels['enemy_hp_change_label'].element.color = const.DEFAULT_COLOR
            materials.front_layer.labels['enemy_hp_change_label'].element.text = str(_enemy_dmg)
            materials.front_layer.labels['enemy_hp_change_label'].element.x = 600
            materials.front_layer.labels['enemy_hp_change_label'].element.y = 320
            materials.front_layer.labels['enemy_hp_change_label'].visible = True
            if not materials.front_layer.labels['enemy_hp_change_label'].are_actions_running():
                materials.front_layer.labels['enemy_hp_change_label'].do(actions.MoveBy((80,0),0.3) + actions.FadeOut(0.3) + actions.MoveBy((-80,0),0.3))
            else:
                materials.front_layer.labels['enemy_hp_change_label'].visible = False
        elif cri_dice==2:
            materials.front_layer.labels['enemy_hp_change_label'].element.font_size = 36
            materials.front_layer.labels['enemy_hp_change_label'].element.color = const.HIGHLIGHT_COLOR
            materials.front_layer.labels['enemy_hp_change_label'].element.text = str(_enemy_dmg)
            materials.front_layer.labels['enemy_hp_change_label'].element.x = 600
            materials.front_layer.labels['enemy_hp_change_label'].element.y = 320
            materials.front_layer.labels['enemy_hp_change_label'].visible = True
            if not materials.front_layer.labels['enemy_hp_change_label'].are_actions_running():
                materials.front_layer.labels['enemy_hp_change_label'].do(actions.MoveBy((100,0),0.3) + actions.FadeOut(0.3) + actions.MoveBy((-100,0),0.3))
            else:
                materials.front_layer.labels['enemy_hp_change_label'].visible = False



    return None
