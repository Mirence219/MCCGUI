import shutil
import os


def creat_user_file(filename,user_data):
    '''生成配置文件'''
    if os.path.isdir(f"user/{filename}"):
        shutil.rmtree(f"user/{filename}",ignore_errors=False,onerror=None)
    shutil.copytree("config/app_default",f"config/app_data/{filename}")
    print(f"[DEBUG]已生成{filename}")


def MCCGUI_print(text, log = None):
    '''同时输出到输出流和日志(如果有的话)'''
    print(text)
    if log != None:
        log.info(text)



