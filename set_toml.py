'''
通过TOML模块修改TOML配置文件
'''

import os
import tomlkit
import toml
from pprint import pprint
from encryptor import decrypt

#代码文件名
FILE_NAME = os.path.basename(__file__) 

#Advance字段映射名称
# ADVANCED_MAPPING：{数据库字段名: (config键名, 数据类型)}
# 类型说明：bool=数据库0/1整数，str=文本，float=浮点，int=普通整数（无0/1限制）
ADVANCED_MAPPING = {
    "enable_sentry": ("EnableSentry", bool),
    "language": ("Language", str),
    "load_mcc_translation": ("LoadMccTranslation", bool),
    "console_title": ("ConsoleTitle", str),
    "internal_cmd_char": ("InternalCmdChar", str),
    "message_cooldown": ("MessageCooldown", float),
    "bot_owners": ("BotOwners", str),
    "minecraft_version": ("MinecraftVersion", str),
    "enable_forge": ("EnableForge", str),
    "brand_info": ("BrandInfo", str),
    "chatbot_log_file": ("ChatbotLogFile", str),
    "private_msgs_cmd_name": ("PrivateMsgsCmdName", str),
    "show_system_messages": ("ShowSystemMessages", bool),
    "show_xp_bar_messages": ("ShowXpBarMessages", bool),
    "show_chat_links": ("ShowChatLinks", bool),
    "show_inventory_layout": ("ShowInventoryLayout", bool),
    "terrain_and_movements": ("TerrainAndMovements", bool),
    "move_head_while_walking": ("MoveHeadWhileWalking", bool),
    "movement_speed": ("MovementSpeed", float),
    "temporary_fix_badpacket": ("TemporaryFixBadpacket", bool),
    "inventory_handling": ("InventoryHandling", bool),
    "entity_handling": ("EntityHandling", bool),
    "session_cache": ("SessionCache", str),
    "profile_key_cache": ("ProfileKeyCache", str),
    "resolve_srv_records": ("ResolveSrvRecords", str),
    "player_head_as_icon": ("PlayerHeadAsIcon", bool),
    "exit_on_failure": ("ExitOnFailure", bool),
    "cache_script": ("CacheScript", bool),
    "timestamps": ("Timestamps", bool),
    "auto_respawn": ("AutoRespawn", bool),
    "minecraft_realms": ("MinecraftRealms", bool),
    "tcp_timeout": ("TcpTimeout", int),
    "enable_emoji": ("EnableEmoji", bool),
    "min_terminal_width": ("MinTerminalWidth", int),
    "min_terminal_height": ("MinTerminalHeight", int),
    "ignore_invalid_player_name": ("IgnoreInvalidPlayerName", bool)
}

def set_data(user_data, advanced_data, path):
    '''修改配置文件设置'''
    
    try:
        with open(path, "r", encoding="utf-8") as f:     #读取TOML配置文件
            config = tomlkit.load(f)
    except Exception as e:
        print(f"[ERROR{FILE_NAME}]TOML文件读取失败，报错:{e}")
        return


    #修改用户账户信息(Main.General)

    config["Main"]["General"]["Account"]["Login"] = user_data["account"]                         #设置账号

    config["Main"]["General"]["Server"]["Host"] = user_data["game_server_ip"]                    #设置游戏服务器地址

    if user_data["game_server_port"]: 
        config["Main"]["General"]["Server"]["Port"] = user_data["game_server_port"]              #设置游戏服务器端口
    elif "Port" in config["Main"]["General"]["Server"]:
        config["Main"]["General"]["Server"].pop("Port")                                     

    
    if user_data["account_type"] in ("microsoft", "yggdrasil"):
        config["Main"]["General"]["AccountType"] = user_data["account_type"]                         #修改账号类型

    if user_data["account_type"] == "yggdrasil":
        config["Main"]["General"]["AuthServer"]["Host"] = user_data["login_server_ip"]               #设置认证服务器地址
        config["Main"]["General"]["Account"]["Password"] = decrypt(user_data["password"])            #设置密码
        config["Main"]["General"]["ProfileName"] = user_data["role_name"]                            #设置角色名称

        if user_data["login_server_port"]:
            config["Main"]["General"]["AuthServer"]["Port"] = user_data["login_server_port"]     #设置认证服务器端口
        else:
            config["Main"]["General"]["AuthServer"].pop("port")

    if user_data["account_type"] == "offline":
        config["Main"]["General"]["Account"]["Password"] = "-"                              #离线模式密码为“-”


    #修改高级设置(Main.Advanced)

    for option ,(mapping, target_type) in ADVANCED_MAPPING.items():
        if advanced_data[option] not in (None, ""):
            if target_type is bool:
                config["Main"]["Advanced"][mapping] = bool(advanced_data[option])   #批量设置
                print(f"[DEBUG]已设置{mapping}为{bool(advanced_data[option])}")
            else:
                config["Main"]["Advanced"][mapping] = advanced_data[option]     
                print(f"[DEBUG]已设置{mapping}为{advanced_data[option]}")




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
        print(f"[ERROR{FILE_NAME}]TOML文件读取失败，报错:{e}")
        return

    config["Main"]["General"]["Account"]["Password"] = ""

    try:
        with open(path, "w", encoding="utf-8") as f:     
            tomlkit.dump(config, f)
        print(f"[DEBUG:{FILE_NAME}]已清除密码，TOML文件路径{path}")
    except Exception as e:
        print(f"[ERROR{FILE_NAME}]TOML文件写入失败，报错:{e}")



def read(path) -> dict:
    '''读取toml文件的内容'''
    with open(path, "r", encoding="utf-8") as f:     #读取TOML配置文件
        config = toml.load(f)
    return config

if __name__ == "__main__":
    ini_path = r"config\app_default\MinecraftClient.ini"
    print(f"[DEBUG:{FILE_NAME}]MCCTOML文件内容：")
    pprint(read(ini_path))
