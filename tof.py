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


""" THE DICE TEST
_list =[0, 0, 0, 0, 0, 0]

for _ in range(100000):
    t = player.ran_dice(1,6,250,30)
    _list[t -1] += 1

print(_list)

"""
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

#for _ in iplayer.item_equiped:
#    item.show(_)
x = int(input('the attack style:'))
if x<0 or x>8:
    x = 0
while battle.player_attack(iplayer, ienemy, x):
    x = int(input('the attack style:'))
    if x<0 or x>8:
        x = 0