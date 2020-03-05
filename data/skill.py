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
import materials.main_scr

class Skill(object):

    def __init__(self,skill_no):

        self.skill_no = skill_no
        self.actived = False
        self.round_last = const.SKILL_DATA[skill_no]['round_last']
        self.round = const.SKILL_DATA[skill_no]['round_last']


    def active(self):
        self.actived = True
        
        if self.skill_no in [0, 1, 2, 4, 5, 8, 15, 16, 17, 19, 21]:
            show_message(const.BATTLE_MESSAGE[const.SKILL_NAME[self.skill_no]])

        if self.skill_no in [5, 15, 16, 17, 18, 19, 21]:
            materials.main_scr.sprites[const.SKILL_NAME[self.skill_no]].visible = True

    def check_buff(self, debuff_end_round=0):
        self.round_last -= 1
        if self.round_last <debuff_end_round:
            self.reset()

    def reset(self):

        self.actived = False
        self.round_last = const.SKILL_DATA[self.skill_no]['round_last']
        if self.skill_no in [5, 15, 16, 17, 18, 19, 21]:
            materials.main_scr.sprites[const.SKILL_NAME[self.skill_no]].visible = False

    def test(self):
        if random.randrange(1,101) <= const.SKILL_DATA[self.skill_no]['rate']:
            return True
        else:
            return False
    @property
    def description(self):
        # description strings of the skill
        return const.SKILL_DATA[self.skill_no]['description']

# when a skill is casted
def casted(skill_no, player=None, enemy=None):
        pass

