#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/6/7 22:59:49

import random
import time
from data import const, player, item, enemy, skill
import materials
from materials.front_layer import show_message
from cocos import actions

def check_style(_player, attack_style):
    """calculate the attack style
    """
    battle_value = dict()

    # set the dice range
    _min_dice = _player.value['MinDice']
    _max_dice = _player.value['MaxDice']
    # check the attack styles
    _atk = _player.value['Atk'] * (1 + 
            const.ATTACK_STYLE_DATA[attack_style]['Atk'] / 100)
    _def = _player.value['Def'] * (1 + 
            const.ATTACK_STYLE_DATA[attack_style]['Def'] / 100)
    _luc = _player.value['Luc'] * (1 + 
            const.ATTACK_STYLE_DATA[attack_style]['Luc'] / 100)

    _cri_dmg = _player.value['CriDmg']
    _block_value = _player.value['BlockValue']
    _regen = _player.value['HpRegen']
    _debuff_round_minus = _player.value['DebuffRoundMinus']

    # special handling for '神鬼奇谋'
    if attack_style == 9 and _max_dice < 9:
        _max_dice += 1

    battle_value = {"atk":_atk,
            "def":_def,
            "luc":_luc, 
            "cri_dmg":_cri_dmg, 
            "block_value":_block_value, 
            "regen":_regen, 
            "min_dice":_min_dice, 
            "max_dice":_max_dice, 
            "debuff_round_minus":_debuff_round_minus
            }

    return battle_value

def show_buff(player, skill_no, buff_name, enemy=False):
    if enemy:
        start_pos = 600
        pos_y = 240
    else:
        start_pos = 50
        pos_y = 210
    if not(skill_no in player.actived_buff):
        player.actived_buff.append(skill_no)
        materials.main_scr.sprites[buff_name].position = start_pos + len(player.actived_buff) * 30, pos_y
        materials.main_scr.sprites[buff_name].visible = True



def player_attack(_player, _enemy, attack_style):
    """the core method of the battle which
    deals with the attack action
    attack_style means the 10 kind of attack styles
    """
    
    # check the attack style
    battle_value = check_style(_player, attack_style)
    
    # The skill has 3 types:
    # type 1: 
    # passive skills, triggers at a rate, see the details in the 
    # player.py (Player Class - def value()) and the enemy.py
    # type 2: 
    # active when attacking the enemy at a rate, last for [round_last] rounds
    # type 3: 
    # active when attacked by the enemy at a rate, last for [round_last] rounds

    # check the enemy's skill list before attack
    # when casted , use the method skill.casted too
    
    debuff_end_round = battle_value["debuff_round_minus"]

    for _ in _enemy.skill:
        # skill 18: make the player max_dice half
        if _.skill_no == 18 and _.actived:
            #show_buff(_player, 18, 'buff_cripple')
            if (battle_value["max_dice"] % 2):
                battle_value["max_dice"] = (battle_value["max_dice"] + 1) / 2
            else:
                battle_value["max_dice"] /= 2
            battle_value["max_dice"] = int(battle_value["max_dice"])
            if battle_value["max_dice"] < battle_value["min_dice"]:
                battle_value["max_dice"] = battle_value["min_dice"]
            show_message(const.BATTLE_MESSAGE['PlayerCripple'].format( 
                    const.ENEMY_DATA[_enemy.no]['enemy_name'][_enemy.zone])) 
            _.check_buff(debuff_end_round)
    # hp regen
    if battle_value["regen"]:
        _player.hp += battle_value["regen"]
        show_message(const.BATTLE_MESSAGE['Regen'].format(int(battle_value["regen"])))
        show_hp_increase(_player, battle_value["regen"], 0)
        if _player.hp > _player.max_hp:
            _player.hp = _player.max_hp

    # now throw the dice
    _player_dice = player.ran_dice(battle_value["min_dice"], 
            battle_value["max_dice"], battle_value["luc"], _player.level)
    _player.show_dice(_player_dice)
    _enemy_dice = player.ran_dice(_enemy.value['Min_Dice'], 
            _enemy.value['Max_Dice'], _enemy.value['Luc'], _enemy.level)
    _player.show_dice(_enemy_dice, True)

    # now check the skill 0: EARTHQUAKE :throw the dice again
    if _player_dice < _enemy_dice:
        for _ in _player.skill:
            if _ is None:
                continue
            if _.skill_no == 0:
                if not(_.actived) and _.test():
                    _.active()
                if _.actived:
                    _enemy_sprite = 'enemy_dice_' + str(_player.cri_dice)
                    _player_sprite = 'player_dice_' + str(_player.cri_dice)
                    materials.main_scr.sprites[_enemy_sprite].do(actions.Blink(4, 1))
                    materials.main_scr.sprites[_player_sprite].do(actions.Blink(4, 1))
                
                    _.check_buff()
                    return True
            
    # now check:
    # the skill 3: war cry to make enemy take the min dice!        
    # the skill 7,  
    for _ in _player.skill:
        if _:
            if _.skill_no == 3:
                if not(_.actived) and _.test():
                    _.active()
                if _.actived:
                    _enemy_dice = _enemy.value['Min_Dice']
                    _player.show_dice(_enemy_dice, True)
                    show_message(const.BATTLE_MESSAGE['Warcry'])
                    _.check_buff()
            elif _.skill_no == 7:
                if not(_.actived) and _.test():
                    _.active()
                if _.actived:
                    battle_value["cri_dmg"] = (battle_value["cri_dmg"] * 
                            (2 - _player.hp / _player.max_hp))
                    _.check_buff()

    # check the skill 17: the big wall
    _big_wall = False
    for _ in _enemy.skill:
        if _.skill_no == 17 and _.actived:
            show_message(const.BATTLE_MESSAGE['Wall'])
            #show_buff(_enemy, 17, 'buff_wall', True)

            _big_wall = True
            _.check_buff(debuff_end_round)

    # now check the dice value between each other at last!
    if _player_dice == _enemy_dice:
        player.dice_equal(_player, _enemy)
        _dmg = 0
    # now attempt to start the attack actions!
    else:
        if _player_dice > _enemy_dice and (not _big_wall):
            # the normal attack damage value
            _player.show_attack()
            _dmg = (battle_value["atk"] * 
                    (1 - _enemy.value['Def'] / (_enemy.value['Def'] + 1500)) * 
                    (1 + (_player_dice - _enemy_dice) * 0.1))
            for _ in _player.skill:
                if _ is None:
                    continue
                # check the skill 2: poison weapon!
                if _.skill_no == 2:
                    if not _.actived and _.test() and random.randrange(1,101) <= (battle_value["luc"] / 20 + 5):
                        _.active()
                    if _.actived:
                        _dmg = _dmg * 1.5
                        _.check_buff()
                # check the skill 8: revenge attack!
                elif _.skill_no == 8 and _.actived:
                    _dmg = _dmg * 2
                    _.check_buff()

            if _player.cri_dice == 2:
                show_message(const.BATTLE_MESSAGE['PlayerThirdCritical'])
                # the critical and doubled attack !
                _dmg = _dmg * (1+ battle_value["cri_dmg"] / 100) * 2
            elif _player.cri_dice == 1:
                show_message(const.BATTLE_MESSAGE['PlayerDoubleCritical'])
                # the critical attack
                _dmg = _dmg * (1 + battle_value["cri_dmg"] / 100)
            else:
                for _ in _player.skill:
                    if _ is None:
                        continue
                    # skill 1: you can do critical attacks
                    if _.skill_no == 1:
                        if not(_.actived):
                            if _.test() and random.randrange(1,101) <= (battle_value["luc"] / 30 + 5):
                                _.active()
                        if _.actived:
                            _dmg = _dmg * (1 + battle_value["cri_dmg"] / 100)
                            _.check_buff()
                        else:
                            show_message(const.BATTLE_MESSAGE['PlayerAttack'])

            for _ in _enemy.skill:
                # check the skill 15: no weapon!
                if _.skill_no == 15 and _.actived:
                    show_message(const.BATTLE_MESSAGE['PlayerDisarmed'])
                    _dmg = 0
                # skill 19: the shield
                if _.skill_no == 19:
                    if not _.actived and _.test():
                        _.active()
                    if _.actived:
                        _dmg = 0
                # skill 20: the bounce back attack
                if _.skill_no == 20:
                    if not _.actived and _.test():
                        _.active()
                    if _.actived and _dmg:
                        _back_dmg = (_dmg / 2.5 * 
                                (1 - battle_value["def"] / (battle_value["def"] + 1500)))
                        show_message(const.BATTLE_MESSAGE['EnemyBounceAtk'].format(int(_back_dmg)))
                        show_hp_change(_player, None, _player.cri_dice, (0-int(_back_dmg)))
                        _player.hp -= _back_dmg
                # skill 21: the plague
                if _.skill_no == 21 and not _.actived and _.test():
                    _.active()

            if _player.hp <= 0:
                return battle_result(_player, _enemy, 2)
            # check the Elite Damage affix
            _dmg = _dmg * (1 + _player.value['EliteDamage'] / 100)

            if _enemy.hp - _dmg <=0:
                _dmg = _enemy.hp
            _enemy.hp -= _dmg
            if _dmg:
                show_hp_change(None, _enemy, _player.cri_dice, 0, (0-int(_dmg)))
                _str = str(int(_enemy.hp)) +' / ' + str(int(_enemy.value['max_hp']))
                materials.front_layer.labels['enemy_hp_label'].element.text = _str
                _enemy.show_under_attack(_player.cri_dice)

            if (_player.value['HpHit'] or _player.value['HpAbsorb']) and _dmg:
                _ =  _player.value['HpHit'] + _player.value['HpAbsorb'] / 100 * _dmg
                _player.hp += _
                show_message(const.BATTLE_MESSAGE['HpAbsorb'])
                show_hp_increase(_player, 0, _)
                if _player.hp > _player.max_hp:
                    _player.hp = _player.max_hp

            if _enemy.hp <= 0:
                return battle_result(_player, _enemy, 1)
            

        # the enemy attack!
        elif  _player_dice < _enemy_dice and (not _big_wall):
            _enemy.show_attack()
            _dmg = (_enemy.value['Atk'] * 
                    (1 - battle_value["def"] / (battle_value["def"] + 1500)) * 
                    (1 + (_enemy_dice - _player_dice) * 0.1) * 
                    (1 - _player.value['ShortDistanceAtkDecreaseRate'] / 100))
            if _player.cri_dice == 2:
                show_message(const.BATTLE_MESSAGE['EnemyCritical'])
                # the critical and doubled attack !
                _dmg = _dmg * 2
                # check the skill 8 when the player got a critical attack!
                for _ in _player.skill:
                    if _ is None:
                        continue
                    if _.skill_no == 8 and _.test():
                        _.active()
            elif _player.cri_dice == 1:
                show_message(const.BATTLE_MESSAGE['EnemyDoubleCritical'])
                # the critical attack
                _dmg = _dmg * 1.5
                # check the skill 8 when the player got a critical attack!
                for _ in _player.skill:
                    if _ is None:
                        continue
                    if _.skill_no == 8 and _.test():
                        _.active()
            else:
                show_message(const.BATTLE_MESSAGE['EnemyAttack'])
            
            _shield_wall = False
            for _ in _enemy.skill:
                # check the skill 4: the shield wall
                if _.skill_no == 4:
                    if not(_.actived) and _.test():
                        _.active()
                    if _.actived:
                        battle_value["block_value"] *= 2
                        if random.randrange(1,101) <= battle_value["block_value"]:
                            _dmg = _dmg / 4
                            _shield_wall = True
                        _.check_buff()
            if (not _shield_wall and battle_value["block_value"] 
                    and random.randrange(1,101) <= battle_value["block_value"]):
                _dmg = _dmg / 2


            if _player.hp <= _dmg:
                for _ in _player.skill:
                    if _ is None:
                        continue
                    # check the skill 5, divine shield
                    if _.skill_no == 5:
                        if not(_.actived) and _.test():
                            _.active()
                        if _.actived:
                            _dmg = 0
                            #show_buff(_player, 5, 'buff_divine_shield')
                            _.check_buff()
                    # check the skill 6, sparking bullet
                    if _.skill_no == 6:
                        if not(_.actived) and _.test():
                            _.active()
                        if _.actived:
                            _enemy.hp -= _player.hp / 4
                            show_message(const.BATTLE_MESSAGE['PlayerExplode'])
                            _.check_buff()

            # check the skill 15: rob the weapon!
            # check the skill 16: set fire!
            # check the skill 17: set wall!
            # check the skill 18: diable you!
            for _ in _enemy.skill:
                if (not _.actived) and _.test():
                    if _.skill_no in [15,16,17]:
                        _.active()
                    elif _.skill_no == 18:
                        _str = const.ENEMY_DATA[_enemy.no]['enemy_name'][_enemy.zone]
                        show_message(const.BATTLE_MESSAGE[const.SKILL_NAME[_.skill_no]].format(_str))
                        _.active()

            if _dmg:
                _player.hp -= _dmg
                _player.show_under_attack(_player.cri_dice)
                show_hp_change(_player, None, _player.cri_dice, (0-int(_dmg)))

        _player.cri_dice = 0
    
    # check the skill 15, 16, 19, 20, 21 let  the round_last + 1 
    for _ in _enemy.skill:
        if _.skill_no == 16 and _.actived:
            show_message(const.BATTLE_MESSAGE['PlayerInFire'])
            #show_buff(_player, 16, 'buff_fire')
            _skill_dmg = ((_.round - _.round_last) * 0.4 * _enemy.value['Atk'] 
                    * ( 1 - battle_value["def"] / (battle_value["def"] + 1500)))
            show_hp_change(_player, None, 0, (0-int(_skill_dmg)))
            _player.hp -= _skill_dmg
            _.check_buff(debuff_end_round)

        if _.actived and _.skill_no in [15, 19, 20]:
            _.check_buff(debuff_end_round)

        if _.skill_no == 21 and _.actived:
            show_message(const.BATTLE_MESSAGE['PlayerInPlague'])
            #show_buff(_player, 21, 'buff_plague')
            _skill_dmg = (0.2 * _enemy.value['Atk'] * 
                    (1 - battle_value["def"] / (battle_value["def"] + 1500)))
            show_hp_change(_player, None, 0, (0-int(_skill_dmg)))
            _player.hp -= _skill_dmg

            _.check_buff(debuff_end_round)

    _player.show_player()

    if _player.hp <= 0:
        return battle_result(_player, _enemy, 2)
    if _enemy.hp <= 0:
        return battle_result(_player, _enemy, 1)

    return True

# handling the battle result with _result:
# 1 - player winned
# 2 - enemy winned
def battle_result(_player, _enemy, _result):

    #hide all buff sfx
    materials.main_scr.sprites[const.SKILL_NAME[18]].visible = False
    materials.main_scr.sprites[const.SKILL_NAME[5]].visible = False
    materials.main_scr.sprites[const.SKILL_NAME[19]].visible = False
    materials.main_scr.sprites[const.SKILL_NAME[21]].visible = False
    materials.main_scr.sprites[const.SKILL_NAME[16]].visible = False
    materials.main_scr.sprites[const.SKILL_NAME[15]].visible = False
    materials.main_scr.sprites[const.SKILL_NAME[17]].visible = False


    _loot_mf = _player.value['MagicFind']
    _loot_no = 0
    if _result == 1:
        show_message(const.BATTLE_MESSAGE['BeatEnemy'].format(
                const.ENEMY_DATA[_enemy.no]['enemy_name'][_enemy.zone]))
        materials.main_scr.sprites['enemy_sprite'].do(actions.Blink(5,2))

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
            raise ValueError('enemy rank error in battle.py')
        
        _exp *= (_player.value['ExpBonus'] / 100 + 1)
        
        if _player.level == 60:
            _exp = 0

        _gold *= (_player.value['GoldFind'] / 100 + 1)
        
        _player.gold += _gold
        _player.exp += _exp
        show_message(const.BATTLE_MESSAGE['GetGoldExp'].format(int(_gold), int(_exp)))

        _max_exp = int(_player.level ** 3.5) + 300
        if _player.exp >= _max_exp:
            show_message(const.BATTLE_MESSAGE['LevelUp'])
            _player.level += 1
            _player.exp = 0
            _player.hp = _player.max_hp
            _player.update_skill()
            _player.show_player()

        _loot_list = []
        for _ in range(_loot_no):
            _loot_list.append(item.gen_random_item(None, _enemy.level, _loot_mf))
        
        for _ in _loot_list:
            _player.loot.append(_)
        _player.cri_dice = 0
    elif _result == 2:
        _player.alive = False
        _player.epitaph = ('在' + const.ZONE_NAME[_player.zone] + '中死于' + 
                ' ' + const.ENEMY_RANK_NAME[_enemy.rank] + 
                const.ENEMY_DATA[_enemy.no]['enemy_name'][_enemy.zone] + '之手')
        show_message(const.BATTLE_MESSAGE['PlayerDead'])
    return False

def show_hp_increase(_player, _regen=0, _absorb=0):
    # the hp regen/absorb visual effect
    if _regen:
        _label = materials.front_layer.labels['player_hp_regen_label']
        _label.element.color = const.GREEN_COLOR
        _label.element.text = '+ ' + str(_regen)
        _label.visible = True
        _label.do(actions.MoveBy((0, 60), 0.5) + actions.FadeOut(0.3) 
                + actions.MoveBy((0, -60), 0.2))
        return None

    if _absorb:
        _label = materials.front_layer.labels['player_hp_absorb_label']
        _label.element.color = const.GREEN_COLOR
        _label.element.text = '+ ' + str(int(_absorb))
        _label.visible = True
        _label.do(actions.JumpBy((50,30),35,1,0.7) + 
                actions.FadeOut(0.3) + actions.MoveBy((-50,-30),0.3))
        return None



def show_hp_change(_player=None, _enemy=None, cri_dice=0, _player_dmg=0, _enemy_dmg=0):
    if _player:
        _label = materials.front_layer.labels['player_hp_change_label']
        if cri_dice==1:
            _label.element.font_size = 30
            _label.element.color = const.ORANGE_COLOR
            _label.element.text = str(_player_dmg)
            _label.element.x = 150
            _label.element.y = 320
            _label.visible = True
            _label.do(actions.MoveBy((-100,0),0.3) + actions.FadeOut(0.3) 
                    + actions.MoveBy((100,0),0.3))

        elif cri_dice==0:
            _label.element.font_size = 26
            _label.element.color = const.DEFAULT_COLOR
            _label.element.text = str(_player_dmg)
            _label.element.x = 150
            _label.element.y = 320
            _label.visible = True
            _label.do(actions.JumpBy((-80,10),35,1,0.7) + 
                    actions.FadeOut(0.3) + actions.MoveBy((80,-10),0.3))
        elif cri_dice==2:
            _label.element.font_size = 36
            _label.element.color = const.HIGHLIGHT_COLOR
            _label.element.text = str(_player_dmg)
            _label.element.x = 150
            _label.element.y = 320
            _label.visible = True
            _label.do(actions.MoveBy((-100,0),0.3) + actions.FadeOut(0.3) 
                    + actions.MoveBy((100,0),0.3))
    if _enemy:
        _label = materials.front_layer.labels['enemy_hp_change_label']
        if cri_dice==1:
            _label.element.font_size = 30
            _label.element.color = const.ORANGE_COLOR
            _label.element.text = str(_enemy_dmg)
            _label.element.x = 600
            _label.element.y = 320
            _label.visible = True
            _label.do(actions.MoveBy((100,0),0.3) + actions.FadeOut(0.3) 
                    + actions.MoveBy((-100,0),0.3))
        elif cri_dice==0:
            _label.element.font_size = 26
            _label.element.color = const.DEFAULT_COLOR
            _label.element.text = str(_enemy_dmg)
            _label.element.x = 600
            _label.element.y = 320
            _label.visible = True
            _label.do(actions.JumpBy((80,10),35,1,0.7) + 
                    actions.FadeOut(0.3) + actions.MoveBy((-80,-10),0.3))
        elif cri_dice==2:
            _label.element.font_size = 36
            _label.element.color = const.HIGHLIGHT_COLOR
            _label.element.text = str(_enemy_dmg)
            _label.element.x = 600
            _label.element.y = 320
            _label.visible = True
            _label.do(actions.MoveBy((100,0),0.3) + actions.FadeOut(0.3) + 
                    actions.MoveBy((-100,0),0.3))

    return None
