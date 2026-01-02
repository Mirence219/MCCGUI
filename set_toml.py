'''
通过TOML模块修改TOML配置文件
'''

import os
import tomlkit
import toml
from pprint import pprint

#代码文件名
FILE_NAME = os.path.basename(__file__) 

def set_user_data(data, path):
    '''修改用户账户信息(Main.General)'''
    try:
        with open(path, "r", encoding="utf-8") as f:     #读取TOML配置文件
            config = tomlkit.load(f)
    except Exception as e:
        print(f"[ERROR{FILE_NAME}]文件打开失败，报错:{e}")
        return
    
    config["Main"]["General"]["Account"]["Login"] = data["account"]                         #设置账号

    config["Main"]["General"]["Server"]["Host"] = data["game_server_ip"]                    #设置游戏服务器地址

    if data["game_server_port"]: 
        config["Main"]["General"]["Server"]["Port"] = data["game_server_port"]              #设置游戏服务器端口
    else:
        config["Main"]["General"]["Server"].pop("Port")                                     #设置游戏服务器端口

    
    if data["account_type"] in ("microsoft", "yggdrasil"):
        config["Main"]["General"]["AccountType"] = data["account_type"]                         #修改账号类型

    if data["account_type"] == "yggdrasil":
        config["Main"]["General"]["AuthServer"]["Host"] = data["login_server_ip"]               #设置认证服务器地址
        config["Main"]["General"]["Account"]["Password"] = data["password"]                     #离线模式密码
        config["Main"]["General"]["ProfileName"] = data["role_name"]                            #设置角色名称

        if data["login_server_port"]:
            config["Main"]["General"]["AuthServer"]["Port"] = data["login_server_port"]     #设置认证服务器端口
        else:
            config["Main"]["General"]["AuthServer"].pop("port")

    if data["account_type"] == "offline":
        config["Main"]["General"]["Account"]["Password"] = "-"                              #离线模式密码为“-”

    try:
        with open(path, "w", encoding="utf-8") as f:
            tomlkit.dump(config, f)
        print(f"[DEBUG:{FILE_NAME}]TOML文件修改成功")
    except Exception as e:
        print(f"[ERROR:{FILE_NAME}]TOML文件修改失败，报错：{e}")


def clear_password(path):
    try:
        with open(path, "r", encoding="utf-8") as f:     #读取TOML配置文件
            config = tomlkit.load(f)
    except Exception as e:
        print(f"[ERROR{FILE_NAME}]文件打开失败，报错:{e}")
        return

    config["Main"]["General"]["Account"]["Password"] = ""
    print(f"[DEBUG{FILE_NAME}]已清除密码")

def read(path) -> dict:
    '''读取toml文件的内容'''
    with open(path, "r", encoding="utf-8") as f:     #读取TOML配置文件
        config = toml.load(f)
    return config

if __name__ == "__main__":
    ini_path = r"config\app_default\MinecraftClient.ini"
    print(f"[DEBUG:{FILE_NAME}]MCCTOML文件内容：")
    pprint(read(ini_path))





'''    
file=open(path,"r",encoding="utf-8")
    lines=file.readlines()
    file.close()
    lines[11]='Account ={ Login = "'+str(data["account"])+'", Password = "'+str(data["password"])+'" }\n' #填充账户密码
    lines[12]='Server = { Host = "'+str(data["game_server_ip"])+'" }\n' #填充服务器IP
    lines[13]='AccountType = "'+str(data["account_type"])+'" \n' #填充登录方式
    lines[14]='ProfileName = "'+str(data["role_name"])+'"\n'
    lines[16]='AuthServer = { Host = "'+str(data["login_server_ip"])+'", Port = 443 }\n' #填充认证服务器
    lines[27]='MinecraftVersion = "1.20.4" \n' #填充游戏版本
    file=open(path,"w",encoding="utf-8")
    file.writelines(lines)
    print(f"[DEBUG:{FILE_NAME}]修改toml文件完成")
    '''

