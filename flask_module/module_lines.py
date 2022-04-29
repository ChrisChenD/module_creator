
import copy
from urllib.request import parse_keqv_list

class Item_line:
    def __init__(self, field_list, select_line):
        self.head = self.__class__.__name__
        self.field_list = field_list
        self.select_line = select_line
        self.init_data_list()
    def init_data_list(self): 
        self.data_list = [field['Field'] for field in self.field_list]
    @property
    def select_list(self):
        return self.select_line.data_list
    @staticmethod
    def selected_field(value, selected=True):
        return dict(value=value, selected=selected)
    def selected_data(self, head=True):
        return [self.selected_field(self.head,True)
        ]+[self.selected_field(value, self.select_list[i])
            for i,value in enumerate(self.data_list)
            if self.select_list[i] == True
        ]+[self.selected_field(value, self.select_list[i])
            for i,value in enumerate(self.data_list)
            if self.select_list[i] == False
        ]
    # @staticmethod
    def _real_id(self, maped_id):
        maped_id -= 1
        if maped_id == -1:
            return -1
        # 因为我们重排了列的位置，(true在前)需要逻辑映射
        id_map = [
            i
            for i,b in enumerate(self.select_list) if b==True
        ]+[
            i
            for i,b in enumerate(self.select_list) if b==False
        ]
        return id_map[maped_id]
    def set(self, i, value):
        self.data_list[i] = value

class Field_line(Item_line):
    def init_data_list(self): 
        self.data_list = [field['Field'] for field in self.field_list]
        self.head = 'field_list'

class Comment_line(Item_line):
    def init_data_list(self): 
        self.data_list = [field['Comment'] for field in self.field_list]
        self.head = 'Comment_list'

class Cond_line(Item_line):
    def init_data_list(self): 
        self.data_list = ['' for field in self.field_list]
        self.head = 'cond_list'
        self.set_default()

    def set_default(self):
        field_list = [field['Field'] for field in self.field_list]
        for i in range(len(field_list)):
            field = field_list[i]
            if field == 'dataStatus':
                self.data_list[i] = 'dataStatus!=3'
            if field == 'isValid':
                self.data_list[i] = 'isValid=1'

class Select_line(Item_line):
    def init_data_list(self): 
        self.select_line = self
        self.data_list = [True]*len(self.field_list)
        self.head = '选择:默认'
        self.set_default()

    def set_default(self):
        field_list = [field['Field'] for field in self.field_list]
        for i,field in enumerate(field_list):
            if field in 'id,isValid,dataStatus,modifyTime,createTime'.split(','):
                # print('field!', field)
                self.data_list[i] = False
            else: self.data_list[i] = True
    def select_switch(self, field_id):
        field_id = self._real_id(field_id)
        if field_id == -1:
            if self.head == '选择:默认':
                self.head = '选择:全不选'
                data_len = len(self.data_list)
                self.data_list = [False]*data_len
            else:
                self.head = '选择:默认'
                self.set_default()
        else:
            self.data_list[field_id] = not self.data_list[field_id] 
class Key_line(Item_line):
    def init_data_list(self): 
        self.data_list = [field['Key'] for field in self.field_list]
        self.head = 'key_list'
        self.select_keyid = -1
    # 我们可能需要把前端全都改革掉.
    # 我们需要探索一个从后端到前端的整体 compo
    # 这个compo直接从后端传入所有的参数
    # >>>>>>>>>

    # def selected_data(self, head=True):
    #     pass

class Prev_line(Item_line):
    def init_data_list(self): 
        self.data_list = []
        self.head = '选择 chunk.key'
        self.select_keyid = -1
    def selected_data(self, head=True):
        # return [self.head]+self.data_list
        return [self.selected_field(self.head,True)
        ]+[self.selected_field(value, i==self.select_keyid)
            for i,value in enumerate(self.data_list)
        ]
    @property
    def prev_list(self):
        return self.data_list
    @prev_list.setter
    def prev_list(self, prev_list):
        self.data_list = prev_list
    
    def select_chunk_key(self, field_id):
        field_id -= 1
        if self.select_keyid == field_id:
            # 取消选择
            self.select_keyid = -1
        else:
            # 选择
            self.select_keyid = field_id
# def Prev_line_to_list(prev_list):
#     head = '选择 chunk.key'
#     return [head]+prev_list


# line组
def item_map(field_list):
    select_line = Select_line(field_list, None)
    return {
        'field_list': Field_line(field_list, select_line),
        'comment_list': Comment_line(field_list, select_line),
        'cond_list': Cond_line(field_list, select_line),
        'select_list': select_line,
        'prev_list':Prev_line(field_list, select_line)
    }

def item_map2(field_list):
    select_line = Select_line(field_list, None)
    return {
        'field_list': Field_line(field_list, select_line),
        'comment_list': Comment_line(field_list, select_line),
        'cond_list': Cond_line(field_list, select_line),
        'select_list': select_line,
        'key_list':Key_line(field_list, select_line),
        'prev_list':Prev_line(field_list, select_line)
    }


