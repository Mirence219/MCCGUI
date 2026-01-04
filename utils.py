from ntpath import isfile
import shutil
import os

#代码文件名
FILE_NAME = os.path.basename(__file__) 

def creat_user_file(path):
    '''生成配置文件'''
    f"[DEBUG:{FILE_NAME}]已删除{path}"
    try:
        if os.path.isfile(path):
            shutil.rmtree(path, ignore_errors=False, onerror=None)
        shutil.copytree("config/app_default",path)
        print(f"[DEBUG:{FILE_NAME}]已生成{path}")
    except Exception as e:
        print(f"[ERROR:{FILE_NAME}]创建{path}失败，报错{e}")

def delete_user_file(path):
    '''删除配置文件'''
    try:
        if os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=False, onerror=None)
            print(f"[DEBUG:{FILE_NAME}]已删除{path}")
            return 0
        else:
            print(f"[DEBUG:{FILE_NAME}]未检测到{path}")
            return 1
    except Exception as e:
        print(f"[ERROR:{FILE_NAME}]删除{path}失败，报错{e}")
        return -1


def MCCGUI_print(text, log = None):
    '''同时输出到输出流和日志(如果有的话)'''
    print(text)
    if log != None:
        log.info(text)



