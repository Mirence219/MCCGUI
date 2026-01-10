'''
用于建立数据库，并进行修改、查找、插入等操作
'''

from sqlite3 import *
import os

#代码文件名
FILE_NAME = os.path.basename(__file__) 

#数据库文件名字
DB_NAME = os.path.join("config", "data.db")


class Data:
    '''通用表基类（仅用于继承）'''
     #表名
    TABLE_NAME = ""

    #表列标题（元组）
    TABLE_COLUMNS = ""

    def __init__(self):
        '''初始化表（创建和更新）'''

        self._columns = tuple(col.split()[0] for col in self.TABLE_COLUMNS)

        conn = connect(DB_NAME)
        cursor = conn.cursor()
        self._create(conn, cursor)
        self._update(conn, cursor)
        cursor.close()
        conn.close()

    def _create(self, conn, cursor):
        '''创建表（内部）'''
        try:
            cursor.execute(f"CREATE TABLE {self.TABLE_NAME}({",".join(self.TABLE_COLUMNS)})")
            print(f"[DEBUG:{FILE_NAME}]已创建表{self.TABLE_NAME}")
        except OperationalError:
            print(f"[DEBUG:{FILE_NAME}]表{self.TABLE_NAME}已存在")
        except Exception as e:
            print(f"[DEBUG:{FILE_NAME}]表{self.TABLE_NAME}无法创建，报错：{e}")

    def _update(self, conn, cursor):
        '''检查和更新表（内部）'''
        cursor.execute(f"PRAGMA TABLE_INFO({self.TABLE_NAME})")
        columns_info = cursor.fetchall()
        now_columns = [col[1] for col in columns_info]  #获取当前表的字段
        print(f"[DEBUG:{FILE_NAME}]表{self.TABLE_NAME}现有字段：{now_columns}")
        missing_columns = [col for col in self.columns() if col not in now_columns]   #和列标题列表比较得到缺失字段
        if missing_columns:
            print(f"[DEBUG:{FILE_NAME}]表{self.TABLE_NAME}缺失字段：{missing_columns},即将更新")
            try:
                for col in missing_columns:
                    cursor.execute(f"ALTER TABLE {self.TABLE_NAME} ADD COLUMN {col}")    #添加缺失字段
                    print(f"[DEBUG:{FILE_NAME}]已添加字段'{col}'")
            except Exception as e:
                print(f"[ERROR{FILE_NAME}]添加失败，报错：{e}'")
        else:
            print(f"[DEBUG:{FILE_NAME}]表{self.TABLE_NAME}字段完整，无需更新")

    def __len__(self) -> int:
        '''用len()获取数据行数'''
        conn = connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {self.TABLE_NAME}")
        count = int(cursor.fetchone()[0])
        cursor.close()
        conn.close()
        #print(count)
        return count

    def columns(self) -> tuple:
        '''返回包含所有列标题的元组（包括id）'''
        return self._columns

    def get_all(self):
        '''返回表全部数据（返回的是包含了字典和id的迭代器对象）'''
        conn = connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.TABLE_NAME}")
        all_data = cursor.fetchall()
        cursor.close()
        conn.close()
        for data in all_data:
            data_dic = dict(zip(self.columns(), data))  #变为字典（包含id）
            data_id = data_dic.pop("id")                #取出id单独返回
            yield data_id, data_dic

    def add(self, data_dic, data_id = None):
        '''添加新数据'''
        conn = connect(DB_NAME)
        cursor = conn.cursor()

        try:
            data_dic = data_dic
            if data_id:
                data_dic["id"] = data_id
            columns = ",".join(data_dic.keys())
            placeholders = ",".join(["?"] * len(data_dic))
            sql = f"INSERT INTO {self.TABLE_NAME} ({columns}) VALUES ({placeholders})"  #拼接SQL语句
            values = tuple(data_dic.values())                                           #传入的参数
            cursor.execute(sql, values)     #添加数据       
            last_id = cursor.lastrowid      #获取刚刚插入数据的ID
            conn.commit()
            print(f"[DEBUG:{FILE_NAME}]已添加账户（id={last_id}）：{data_dic}")
            return last_id  #返回id方便后续其他表的创建数据操作

        except Exception as e:
            conn.rollback()
            print(f"[ERROR{FILE_NAME}]添加失败，报错：{e}")

        finally:
            cursor.close()
            conn.close()

    def update(self, data_id, data_dic):
        '''修改指定数据'''
        conn = connect(DB_NAME)
        cursor = conn.cursor()

        try:
            set_statement = " , ".join([f"{key} = ?" for key in data_dic.keys()])   #拼接赋值语句部分
            sql = f"UPDATE {self.TABLE_NAME} SET {set_statement} WHERE id = ?"      
            values = list(data_dic.values())+ [data_id]                             
            cursor.execute(sql, values)     #修改数据
            conn.commit()
            print(f"[DEBUG:{FILE_NAME}]已修改账户（id={data_id}）为：{data_dic}")

        except Exception as e:
            conn.rollback()
            print(f"[ERROR{FILE_NAME}]修改账户{self.TABLE_NAME} id = {data_id}失败，报错：{e}")

        finally:
            cursor.close()
            conn.close()

    def delete(self, data_id):
        '''删除指定数据'''
        conn = connect(DB_NAME)
        cursor = conn.cursor()

        try:
            sql = f"DELETE FROM {self.TABLE_NAME} WHERE id = ?"
            value =  (data_id,)
            cursor.execute(sql, value)  #删除数据
            conn.commit()
            print(f"[DEBUG:{FILE_NAME}]已删除数据（id={data_id}）")

        except Exception as e:
            conn.rollback()
            print(f"[ERROR{FILE_NAME}]删除{self.TABLE_NAME} id = {data_id}失败，报错：{e}")

        finally:
            cursor.close()
            conn.close()

    def selete_all(self, data_id) -> dict:
        '''获取指定id的全部数据'''
        conn = connect(DB_NAME)
        cursor = conn.cursor()
        #print(self.columns())

        try:
            sql = f"SELECT * FROM {self.TABLE_NAME} WHERE id = ?"
            value =  (data_id,)
            cursor.execute(sql, value)  #查询数据
            data_list = cursor.fetchone()
            data_dic = dict(zip(self.columns(), data_list))
            data_dic.pop("id")  #删除id字段
            return data_dic

        except Exception as e:
            print(f"[ERROR{FILE_NAME}]查询{self.TABLE_NAME} id = {data_id}失败，报错：{e}")

        finally:
            cursor.close()
            conn.close()




class TestData(Data):
    '''测试表类（用于测试）'''
     #表名
    TABLE_NAME = "test"

    #表列标题
    TABLE_COLUMNS = (
        "id INTEGER PRIMARY KEY",                                                            
        "account TEXT",                                                                       
        "password BLOB",                                                                      
        "game_server_ip TEXT",                                                               
        "game_server_port INTEGER",                                                          
        "login_server_ip TEXT",                                                               
        "login_server_port INTEGER",
        "hahaha TEXT"
        )



class UserData(Data):
    '''账户数据表类'''

    #表名
    TABLE_NAME = "user"

    #表列标题
    TABLE_COLUMNS = [
        "id INTEGER PRIMARY KEY",                                                             # ID，账户在MCCGUI的唯一编号，用于查询
        "account TEXT",                                                                       # 账号（离线模式写玩家名字）
        "password BLOB",                                                                      # 密码（密文存储，离线玩家写“-”）
        "game_server_ip TEXT",                                                                # 游戏服务器域名或IP
        "game_server_port INTEGER",                                                           # 游戏服务器端口
        "login_server_ip TEXT",                                                               # 认证服务器域名或IP
        "login_server_port INTEGER",                                                          # 认证服务器端口
        "role_name TEXT",                                                                     # 角色名称（用于认证服务器多角色登录）
        "account_type TEXT CHECK (account_type IN ('microsoft', 'yggdrasil', 'offline'))",     # 帐户类型：mojang/microsoft/yggdrasil
    ]




class AdvancedData(Data):
    '''高级设置项类'''

    #表名
    TABLE_NAME = "advanced"

    #表列标题
    TABLE_COLUMNS = [
        "id INTEGER PRIMARY KEY",                                                             # ID，账户在MCCGUI的唯一编号，用于查询
        "enable_sentry INTEGER CHECK (enable_sentry IN (0, 1))",                              # 将此项设置为 false（假），即可选择退出 / 禁用 Sentry 错误日志记录功能。
        "language TEXT",                                                                      # 使用的语言包
        "load_mcc_translation INTEGER CHECK (load_mcc_translation IN (0, 1))",                # 是否加载MCC翻译（0=禁用，1=启用）
        "console_title TEXT",                                                                 # MCC窗口标题（通常用不上）
        "internal_cmd_char TEXT CHECK (internal_cmd_char IN ('none', 'slash', 'backslash'))", # 内部命令前缀（none/slash/backslash）
        "message_cooldown REAL",                                                              # 消息发送间隔（秒）
        "bot_owners TEXT",                                                                    # 机器人所有者列表（格式：'["nick1","nick2"]'）
        "minecraft_version TEXT",                                                             # 游戏版本（"auto" 或 "1.X.X"），MCC只支持 1.4.6 - 1.19.2
        "enable_forge TEXT CHECK (enable_forge IN ('auto', 'no', 'force'))",                  # Forge支持（auto/no/force），仅1.13+
        "brand_info TEXT",                                                                    # 客户端标识（如 "mcc"、"vanilla"）
        "chatbot_log_file TEXT",                                                              # ChatBot日志路径（留空禁用）
        "private_msgs_cmd_name TEXT",                                                         # 远程控制命令名称
        "show_system_messages INTEGER CHECK (show_system_messages IN (0, 1))",                # 显示系统消息（0=隐藏，1=显示）
        "show_xp_bar_messages INTEGER CHECK (show_xp_bar_messages IN (0, 1))",                # 显示经验条消息（防刷屏）
        "show_chat_links INTEGER CHECK (show_chat_links IN (0, 1))",                          # 解码并显示聊天链接
        "show_inventory_layout INTEGER CHECK (show_inventory_layout IN (0, 1))",              # 显示库存布局（/inventory命令）
        "terrain_and_movements INTEGER CHECK (terrain_and_movements IN (0, 1))",              # 地形处理和移动（0=禁用，1=启用）
        "move_head_while_walking INTEGER CHECK (move_head_while_walking IN (0, 1))",          # 移动时转向头部（防反作弊）
        "movement_speed INTEGER",                                                                # 移动速度（建议≤2）
        "temporary_fix_badpacket INTEGER CHECK (temporary_fix_badpacket IN (0, 1))",          # 修复坏数据包问题（需启用地形处理）
        "inventory_handling INTEGER CHECK (inventory_handling IN (0, 1))",                    # 库存处理（0=禁用，1=启用），1.4.6-1.9不支持
        "entity_handling INTEGER CHECK (entity_handling IN (0, 1))",                          # 实体处理（0=禁用，1=启用），1.4.6-1.7不支持
        "session_cache TEXT CHECK (session_cache IN ('none', 'memory', 'disk'))",             # 会话缓存（none/memory/disk）
        "profile_key_cache TEXT CHECK (profile_key_cache IN ('none', 'memory', 'disk'))",     # 聊天密钥缓存（none/memory/disk）
        "resolve_srv_records TEXT CHECK (resolve_srv_records IN ('no', 'fast', 'yes'))",      # SRV记录解析（no/fast/yes）
        "player_head_as_icon INTEGER CHECK (player_head_as_icon IN (0, 1))",                  # 玩家头像作为窗口图标（旧版控制台有效）
        "exit_on_failure INTEGER CHECK (exit_on_failure IN (0, 1))",                          # 错误时退出（0=继续，1=退出）
        "cache_script INTEGER CHECK (cache_script IN (0, 1))",                                # 缓存编译脚本（提升低端设备加载速度）
        "timestamps INTEGER CHECK (timestamps IN (0, 1))",                                    # 聊天消息添加时间戳
        "auto_respawn INTEGER CHECK (auto_respawn IN (0, 1))",                                # 自动重生（确保出生点安全）
        "minecraft_realms INTEGER CHECK (minecraft_realms IN (0, 1))",                        # 支持Minecraft Realms服务器
        "tcp_timeout INTEGER",                                                                # TCP连接超时时间（秒）
        "enable_emoji INTEGER CHECK (enable_emoji IN (0, 1))",                                # 显示Emoji表情（0=替换为简单字符）
        "min_terminal_width INTEGER",                                                         # 终端最小宽度限制
        "min_terminal_height INTEGER",                                                        # 终端最小高度限制
        "ignore_invalid_player_name INTEGER CHECK (ignore_invalid_player_name IN (0, 1))"     # 忽略非标准玩家名（0=严格检查，1=允许）
        ]
    


user_data = UserData()
advanced_data = AdvancedData()