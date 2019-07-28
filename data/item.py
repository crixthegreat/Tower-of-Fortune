#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/6/5 19:41:18
import random
from data import const
import materials

class Item(object):
    """Item Class
    This is a mimic version of diablo-equipment-system.
    The structure of a item is defined by item.csv
    """
    # item_type = [0, 59]
    def __init__(self, item_type):

        # .type means the item's type 
        self.type = item_type
        # AFFIX_MAX_USED_NO = 20 in this game by now
        # set all the affix 0
        # a item is initialised as a dummy item without any affix
        self.affix = [0 for _ in range(const.AFFIX_MAX_USED_NO)]
        self.level = 0
        # rare_type = [1, 5]
        self.rare_type = 1

    @property
    def image_no(self):
        return (59 - self.type) * 5 + self.rare_type

    @property
    def name(self):
        return const.ITEMS_DATA[self.type]['name']

    @property
    def main_type(self):
        # the main type means bigger division(e.g. a single-hand weapon is one
        # of the main types, which includes sword, bow, harmmer and so on)
        return const.ITEMS_DATA[self.type]['main_type']
    @property
    def equiped_pos(self):
        # the position where the item is equipped
        return const.ITEMS_DATA[self.type]['equiped_pos']



    def item_to_dict(self):
        '''Transfor a Item object to a dict for game-saving(W/R in JSON format)
        '''
        _affix_list = []
        for _ in range(const.AFFIX_MAX_USED_NO):
            _affix_list.append(self.affix[_])
        _dict = dict(item_type=self.type,
                main_type=self.main_type, 
                equiped_pos=self.equiped_pos, 
                level=self.level, 
                name=self.name, 
                rare_type=self.rare_type, 
                affix_list=_affix_list
                )
        return _dict

    def type_string(self):
        """Return the type string of the item for showing
        """
        return ('Lv ' + str(self.level) + '\n' + 
                const.RARE_TYPE_NAME[self.rare_type] + ' ' + 
                const.MAIN_TYPE_NAME[self.main_type])

    def main_affix_string(self):
        """for showing the item
        """
        _list = []
        for _ in range(const.AFFIX_MAX_USED_NO):
            if self.affix[_]:
                _list.append(_)
        # move the affix whose def-value is 4 and 3 to front
        for _ in _list:
            if const.ITEMS_DATA[self.type]['affix_value'][_] == 3:
                _list.remove(_)
                _list = [_] + _list
        for _ in _list:
            if const.ITEMS_DATA[self.type]['affix_value'][_] == 4:
                _list.remove(_)
                _list = [_] + _list
        return (const.ITEM_AFFIX_CNAME[_list[0]] + ' ' + 
                str(self.affix[_list[0]]))

    def affix_string(self):
        """for showing the item
        """
        _list = []
        for _ in range(const.AFFIX_MAX_USED_NO):
            if self.affix[_]:
                _list.append(_)
        # move the affix whose def-value is 4 and 3 to front
        for _ in _list:
            if const.ITEMS_DATA[self.type]['affix_value'][_] == 3:
                _list.remove(_)
                _list = [_] + _list
        for _ in _list:
            if const.ITEMS_DATA[self.type]['affix_value'][_] == 4:
                _list.remove(_)
                _list = [_] + _list
        _str = ''
        for _ in range(1, len(_list)):
            _str +=  (const.ITEM_AFFIX_CNAME[_list[_]] + ' ' + 
                    str(self.affix[_list[_]]) + '\n')
        return _str

    def show(self, image_sprite, item_box_sprite, 
            name_label, type_label, main_affix_label, affix_label):
        image_sprite.visible = True
        image_sprite.scale = 0.6
        image_sprite.image = materials.item_image[self.image_no]
        item_box_sprite.visible = True

        name_label.element.text = self.name
        type_label.element.text = self.type_string()
        name_label.visible = True
        type_label.visible = True
        main_affix_label.visible = True
        affix_label.visible = True
        main_affix_label.element.text = self.main_affix_string()
        affix_label.element.text = self.affix_string()
        
        

def dict_to_item(item_dict):
    '''Transfor a item_dictionary to a Item object for game-loading
    '''
    _item = Item(item_dict['item_type'])
    #_item.main_type = item_dict['main_type']
    #_item.equiped_pos = item_dict['equiped_pos']
    _item.level = item_dict['level']
    #_item.name = item_dict['name']
    _item.rare_type = item_dict['rare_type']
    _item.affix = []

    for _ in range(const.AFFIX_MAX_USED_NO):
        _item.affix.append(item_dict['affix_list'][_])

    return _item

def gen_random_item(item_type=None, level=None, mf=None):
    """Generate a random item with item_type, level, and mf
    """
    # not all types of the items have been used
    # the const.ITEM_TYPE_USED stores all the used item types
    # whose name are NOT '未定'
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
    
    # [0,1,...,seg_a,seg_a+1,...,seg_a+seg_b,seg_a+seg_b+1,...,
    #  seg_a+seg_b+seg_c,...]
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
        raise ValueError('rare_type error when generating a item')
    # rare_value = [0,1,2,3]
    _item.rare_type = rare_value

    if not(rare_value in const.ITEM_AFFIX_COUNT.keys()):
        raise ValueError('no rare type for the rare_value: ', rare_value)

    _r = random.randrange(100)
    # affix_no defines how many affix the item has
    if _r <= const.ITEM_AFFIX_COUNT[rare_value]['rate']:
        affix_no = const.ITEM_AFFIX_COUNT[rare_value]['max']
    else:
        affix_no = const.ITEM_AFFIX_COUNT[rare_value]['min']

    # _list is used to determine the affix to be used in the item
    _list = []

    for _ in range(const.AFFIX_MAX_USED_NO):
        # ['affix_value'] is a list whose value is [0,1,2,3,4]
        # 1 = '×'
        # 2 = '△' and so on
        if (const.ITEMS_DATA[item_type]['affix_value'][_] != 0 
                and const.ITEMS_DATA[item_type]['affix_value'][_] != 1):
            # now _list has all the affix index([0,19]) that can use
            _list.append(_)
    # the affix index 5 and 17 is 'max_dice' and 'min_dice'
    if 5 in _list or 17 in _list:
        # you won't have the dice-affix in normal and magic items
        # you won't have it when you're unlucky either 
        # (SPECIAL_AFFIX_RATE is only 20% now)
        if (rare_value == const.RARE_TYPE_NORMAL or 
                rare_value == const.RARE_TYPE_MAGIC or 
                random.randrange(100) > const.SPECIAL_AFFIX_RATE):
            if 5 in _list:
                _list.remove(5)
            if 17 in _list:
                _list.remove(17)
    # shuffle the _list to trim later
    random.shuffle(_list)
    # let the item always have affix whose def-value is 4 and 3
    # so we move them headmost 
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
    # Now set the value for every affix
    for _ in _list:
        #print(const.ITEM_AFFIX_BASE_VALUE[_], get_affix_value(60))
        if _ in [6,7,9,11,13,14,15,19]:
            # the affix that have fixed value
            _item.affix[_] = const.ITEM_AFFIX_BASE_VALUE[_] * get_affix_value(60)
        else:
            _item.affix[_] = const.ITEM_AFFIX_BASE_VALUE[_] * get_affix_value(level)
            # it's odd for having a affix equal to 0
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
def show(item, player_item):

    if item == None:
        print('无')
        return None
    item.show(materials.sprites['item'],
            materials.main_scr.sprites['item_box'],
            materials.main_scr.labels['item_name'],
            materials.main_scr.labels['item_type'],
            materials.main_scr.labels['item_main_affix'],
            materials.main_scr.labels['item_affix'])

    if player_item:
        player_item.show(materials.sprites['player_item'],
                materials.sprites['player_item'],
                materials.main_scr.labels['player_item_name'],
                materials.main_scr.labels['player_item_type'],
                materials.main_scr.labels['player_item_main_affix'],
                materials.main_scr.labels['player_item_affix'])

def hide():
    materials.main_scr.sprites['item_box'].visible = False
    materials.sprites['item'].visible = False
    materials.sprites['player_item'].visible = False
    materials.main_scr.labels['item_name'].visible = False
    materials.main_scr.labels['item_type'].visible = False
    materials.main_scr.labels['item_main_affix'].visible = False
    materials.main_scr.labels['item_affix'].visible = False
    materials.main_scr.labels['player_item_name'].visible = False
    materials.main_scr.labels['player_item_type'].visible = False
    materials.main_scr.labels['player_item_main_affix'].visible = False
    materials.main_scr.labels['player_item_affix'].visible = False

