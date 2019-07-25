#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/6/7 20:01:47

"""handling the skills of player and enemy
"""
import random
from data import const
from materials.front_layer import show_message
class Skill(object):

    def __init__(self,skill_no):

        self.skill_no = skill_no
        self.actived = False
        self.round_last = const.SKILL_DATA[skill_no]['round_last']
        self.round = const.SKILL_DATA[skill_no]['round_last']


    def reset(self):

        self.actived = False
        self.round_last = const.SKILL_DATA[self.skill_no]['round_last']

    def test(self):
        if random.randrange(1,101) <= const.SKILL_DATA[self.skill_no]['rate']:
            return True
        else:
            return False

# when a skill is casted
def casted(skill_no, player=None, enemy=None):
        pass


# display a skill message
def show_skill(skill_no, t=None):

    if skill_no == 0:
        pass
    elif skill_no == 2:
        show_message('你手上的武器泛出绿光...')
    elif skill_no == 3:
        show_message('你大喝一声，敌人的骰子翻滚了一下，变成了：' + str(t))
    elif skill_no == 4:
        show_message('你的盾牌闪闪发光，就像一堵城墙！')
    elif skill_no == 5:
        show_message('你浑身发出神圣的光，敌人的攻击失效了...')
    elif skill_no == 6:
        show_message('你受到攻击，身边发出猛烈的爆炸，怪物受伤了！')
    elif skill_no == 8:
        show_message('你双眼发出复仇的怒火！')
    elif skill_no == 11:
        pass
    elif skill_no == 14:
        pass
    elif skill_no == 15:
        show_message('你四处寻找着你的武器！')
    elif skill_no == 15.5:
        show_message('怪物夺走了你手上的武器！')
    elif skill_no == 16:
        show_message('怪物在你的脚下燃起恐怖的火焰！')
    elif skill_no == 16.5:
        show_message('你站在火焰中，受伤了！')
    elif skill_no == 17:
        show_message('一堵高墙树立在怪物与你之间...')
    elif skill_no == 17.5:
        show_message('敌人召唤了一堵高高的石墙...')
    elif skill_no == 18:
        show_message(t + '让你浑身无力，扔骰子的手抖了')
    elif skill_no == 18.5:
        show_message(t + '施展神秘诅咒，你感到浑身无力...')
    elif skill_no == 19:
        show_message('怪物身上环绕着神奇的光芒...')
    elif skill_no == 20:
        show_message('怪物反弹攻击，造成了伤害，', int(t))
    elif skill_no == 21:
        show_message('你站在毒中，受到了伤害')
    elif skill_no == 21.5:
        show_message('怪物身上弥漫着瘟疫')

    elif skill_no == 90:
        show_message('怪物扔出了一个骰子：' + str(t))
    elif skill_no == 91:
        show_message('你扔出了一个骰子：' + str(t))
    elif skill_no == 92:
        show_message('你恢复了体力：' + str(t))
    
    # 100: when dice equaled for the second time
    elif skill_no == 100:
        show_message('你施展浑身解数，发出致命一击！')
    # 101: when dice equaled for the first time
    elif skill_no == 101:
        show_message('你使出全力，发出奋力一击！')
    # 102: when dice equaled for the third time,explode!
    elif skill_no == 102:
        show_message('一声巨响，骰子爆炸了！')
    elif skill_no == 103:
        show_message('形式千钧一发！')
    elif skill_no == 104:
        show_message('双方四目相对！')
    elif skill_no == 105:
        show_message('你发出了一次暴击！')
    elif skill_no == 106:
        show_message('你施展攻击')
    elif skill_no == 107:
        show_message('怪物发出致命一击！')
    elif skill_no == 108:
        show_message('怪物发出奋力一击！')
    elif skill_no == 109:
        show_message('怪物施展攻击')
    elif skill_no == 110:
        show_message('你的攻击吸收了怪物的体力')
    else:
        pass
        
