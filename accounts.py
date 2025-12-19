# coding: utf-8

import pandas as pd

class Accounts:
    '''账户管理与保存类'''
    def __init__(self):
        self.count = 0
        self.data = pd.read_csv("config/data.csv")
        #print(self.data)

    def add(self,login_data):
        '''添加账户'''
        print("已添加：",login_data)
        self.data.loc[len(self.data)]=login_data
        self.data.to_csv("config/data.csv", index=False)
        #print(self.data)

    def delete(self,number):
        '''删除账户'''
        self.data = self.data.drop(index = number).reset_index(drop=True)
        self.data.to_csv("config/data.csv", index=False)
        print(f"已删除账户{number}")
        #print(self.data)

    def read(self,number):
        '''读取并返回账户(列表[way,account,password,server,login_server,role])'''
        return self.data.iloc[number].tolist()

    def set(self, index, new_data):
        '''修改账户信息'''
        print(f"已修改第{index}项为：{new_data}")
        self.data.loc[index] = new_data
        self.data.to_csv("config/data.csv", index=False)
        #print(self.data)

    def len(self):
        '''返回账户的数量'''
        return len(self.data);