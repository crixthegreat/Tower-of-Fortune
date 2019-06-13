#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/6/5 19:41:18
import sys
import random
from data import const
import materials

class Item(object):
    """Item Class
    """
    # item_type = [0, 59]
    def __init__(self, item_type):

        self.type = item_type
        # AFFIX_MAX_USED_NO = 20
        self.affix = [0 for _ in range(const.AFFIX_MAX_USED_NO)]
        # main_type means the equiped position of the item
        self.main_type = const.ITEMS_DATA[self.type]['main_type']
        self.level = 0
        self.name = const.ITEMS_DATA[self.type]['name']
        # rare_type = [1, 5]
        self.rare_type = 1

def gen_random_item(item_type=None, level=None, mf=None):
    """Generate a random item with item_type, level, and mf
    """
    # not all types of the items have been used
    _list = const.ITEM_TYPE_USED
    if item_type == None:
        random.shuffle(_list)
        # get the random type of the items that are used
        item_type = _list[0]
    if level == None:
        # level is [1, 60]
        level = random.randrange(1,61)
    if mf == None:
        mf = random.randrange(0,1000)
    _item = Item(item_type)
    _item.level = level
    
    # [0,1,...,seg_a,seg_a+1,...,seg_a+seg_b,seg_a+seg_b+1,...,seg_a+seg_b+seg_c,...]
    seg_a = int((const.LEGEND_DROP_RATE + const.SET_DROP_RATE) * (1 + mf / 100))
    seg_b = int(const.RARE_DROP_RATE * (1 + mf / 100))
    seg_c = int(const.MAGIC_DROP_RATE * (1 + mf / 100))
    _r = random.randrange(1,10000)

    if _r <= seg_a:
        rare_value = const.RARE_TYPE_LEGEND
    elif seg_a < _r < seg_a + seg_b:
        rare_value = const.RARE_TYPE_RARE
    elif seg_a + seg_b <= _r < seg_a + seg_b + seg_c:
        rare_value = const.RARE_TYPE_MAGIC
    elif _r >= seg_a + seg_b + seg_c:
        rare_value = const.RARE_TYPE_NORMAL
    else:
        print('rare_type error')
        sys.exit()
    # rare_value = [0,1,2,3]
    _item.rare_type = rare_value
    _r = random.randrange(10)
    # affix_no defines how many affix the item has
    if rare_value == const.RARE_TYPE_LEGEND:
        if _r < 3:
            affix_no = 8
        else:
            affix_no = 7
    elif rare_value == const.RARE_TYPE_RARE:
        if _r < 4:
            affix_no = 6
        else:
            affix_no = 5
    elif rare_value == const.RARE_TYPE_MAGIC:
        if _r < 4:
            affix_no = 4
        else:
            affix_no = 3
    elif rare_value == const.RARE_TYPE_NORMAL:
        affix_no = 2
    else:
        print('rare_value error')
        sys.exit()

    # _list is used to determine the affix to be used in the item
    _list = []

    for _ in range(const.AFFIX_MAX_USED_NO):
        # ['affix_value'] is a list whose value is [0,1,2,3,4]
        # 1 = '×'
        # 2 = '△' and so on
        if const.ITEMS_DATA[item_type]['affix_value'][_] != 0 and const.ITEMS_DATA[item_type]['affix_value'][_] != 1:
            # now _list has all the affix index([0,19]) that can use
            _list.append(_)
    # the affix index 5 and 17 are the 'max_dice' and 'min_dice'
    if 5 in _list or 17 in _list:
        # you can't have the dice-affix in normal and magic items
        # you can't have it when you're unlucky either
        if rare_value == const.RARE_TYPE_NORMAL or rare_value == const.RARE_TYPE_MAGIC or random.randrange(100) > const.SPECIAL_AFFIX_RATE:
            if 5 in _list:
                _list.remove(5)
            if 17 in _list:
                _list.remove(17)
    # shuffle the _list to trim later
    random.shuffle(_list)
    # let the item always have affix whose def-value is 4 and 3
    for _ in _list:
        if const.ITEMS_DATA[item_type]['affix_value'][_] == 3:
            _list.remove(_)
            _list = [_] + _list
    for _ in _list:
        if const.ITEMS_DATA[item_type]['affix_value'][_] == 4:
            _list.remove(_)
            _list = [_] + _list
    # trim the _list to affix_no(the number of affixes that the item can have)
    _list = _list[:affix_no]
    #print(_list)
    for _ in _list:
        #print(const.ITEM_AFFIX_BASE_VALUE[_], get_affix_value(60))
        if _ in [6,7,9,11,13,14,15,19]:
            # the affix that have fixed value
            _item.affix[_] = const.ITEM_AFFIX_BASE_VALUE[_] * get_affix_value(60)
        else:
            _item.affix[_] = const.ITEM_AFFIX_BASE_VALUE[_] * get_affix_value(level)
            # it's odd for having a affix equals 0
            if _item.affix[_] < 1:
                _item.affix[_] = 1
        # make the item's main affix value bigger
        if const.ITEMS_DATA[item_type]['affix_value'][_] == 4:
            _item.affix[_] = _item.affix[_] * 1.8

        _item.affix[_] = int(_item.affix[_])
    
    #print(_item.affix)
    return _item

# calculate the value with level
# I forgot how I got the formula
def get_affix_value(level):
    max_value = int(level ** 3 /1500 + 10 + level)
    _ = int(random.randrange(int(max_value * 3 / 4)) + max_value / 4)
    if _ == 0:
        _ == 1
    return _

# show the item
# a lot of things to be done 
def show(item):

    if item == None:
        print('无')
        return None

    materials.sprites['item'].visible = True
    materials.sprites['item'].image = materials.item_image[(59-item.type) * 5 + item.rare_type]
    materials.labels['item_name'].element.text = item.name
    materials.labels['item_type'].element.text = 'Lv ' + str(item.level) + ' ' + const.RARE_TYPE_NAME[item.rare_type] + ' ' + const.MAIN_TYPE_NAME[item.main_type]
    _list = []
    for _ in range(const.AFFIX_MAX_USED_NO):
        if item.affix[_]:
            _list.append(_)
    # move the affix whose def-value is 4 and 3 to front
    for _ in _list:
        if const.ITEMS_DATA[item.type]['affix_value'][_] == 3:
            _list.remove(_)
            _list = [_] + _list
    for _ in _list:
        if const.ITEMS_DATA[item.type]['affix_value'][_] == 4:
            _list.remove(_)
            _list = [_] + _list
    materials.labels['item_main_affix'].element.text = const.ITEM_AFFIX_CNAME[_list[0]] + str(item.affix[_list[0]])
    _str = ''
    for _ in range(1, len(_list)):
        _str +=  (const.ITEM_AFFIX_CNAME[_list[_]] + str(item.affix[_list[_]]) + '\n')
    materials.labels['item_affix'].element.text = _str
    print(item.name, item.level, const.RARE_TYPE_NAME[item.rare_type], const.MAIN_TYPE_NAME[item.main_type])
    
    for _ in range(const.AFFIX_MAX_USED_NO):
        if item.affix[_]:
            print(const.ITEM_AFFIX_CNAME[_], item.affix[_])

