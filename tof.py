#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/6/4 16:00:51
"""A new start
Tower of fortune (indicate to the great game Tower of fortune in iOS)
"""
import random
from code import const, player, item, enemy, battle, skill



ienemy = enemy.gen_enemy()
enemy.show(ienemy)
iplayer = player.gen_player(40)
_skill = [_ for _ in range(15)]
random.shuffle(_skill)
_skill = _skill[:4]

iplayer.equip_skill(*_skill)
print('玩家出现了！')
print(iplayer.value)
print('你拥有技能：')
for _ in iplayer.skill:
    print(const.SKILL_DATA[_.skill_no]['name'])

while iplayer.hp >0 and ienemy.hp >0:
    x = int(input('the attack style:'))
    if  0 <= x <= 8:
        battle.player_attack(iplayer, ienemy, x)
    
