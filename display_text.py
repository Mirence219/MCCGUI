'''用于解析ANSI转义符号并显示'''
import re
from itertools import count

#tag序号
tag_count = count()

#字体名称
TEXT_FONT_NAME = "TkDefualtFont"

#字体字号
TEXT_FONT_SIZE = 10

#ANSI转义符正则表达式
ANSI_PATTERN = r"\x1b\[[0-9]*m"

#AINSI转义符字体样式对照字典
ANSI_STYLE_DIC = {
    "\x1b[0m" : "normal",       #清除样式
    "\x1b[1m" : "bold",         #加粗
    "\x1b[2m" : "normal",       
    "\x1b[3m" : "italic",      #斜体
    "\x1b[4m" : "underline",    #下划线
    "\x1b[5m" : "normal",
    "\x1b[6m" : "normal",
    "\x1b[7m" : "normal",
    "\x1b[8m" : "normal",
    }

#AINSI转义符前景色对照字典
ANSI_TEXT_COLOR_DIC = {
    "\x1b[30m" : "black",
    "\x1b[31m" : "red",
    "\x1b[32m" : "green",
    "\x1b[33m" : "yellow",
    "\x1b[34m" : "blue",
    "\x1b[35m" : "purple",
    "\x1b[36m" : "cyan",
    "\x1b[37m" : "white",
    "\x1b[38m" : "black",
    "\x1b[39m" : None,
    "\x1b[90m": "gray",       # 灰色
    "\x1b[91m": "red2",       # 亮红色
    "\x1b[92m": "green2",     # 亮绿色
    "\x1b[93m": "yellow2",    # 亮黄色
    "\x1b[94m": "blue2",      # 亮蓝色
    "\x1b[95m": "purple2",    # 亮紫色
    "\x1b[96m": "cyan2",      # 亮青色
    "\x1b[97m": "white",      
    }

#AINSI转义符背景色对照字典
ANSI_BG_COLOR_DIC = {
    "\x1b[40m" : "black",
    "\x1b[41m" : "red",
    "\x1b[42m" : "green",
    "\x1b[43m" : "yellow",
    "\x1b[44m" : "blue",
    "\x1b[45m" : "purple",
    "\x1b[46m" : "cyan",
    "\x1b[47m" : "white",
    "\x1b[48m" : "black",
    "\x1b[49m" : None,
    "\x1b[100m": "gray",       # 灰色
    "\x1b[101m": "red2",       # 亮红色
    "\x1b[102m": "green2",     # 亮绿色
    "\x1b[103m": "yellow2",    # 亮黄色
    "\x1b[104m": "blue2",      # 亮蓝色
    "\x1b[105m": "purple2",    # 亮紫色
    "\x1b[106m": "cyan2",      # 亮青色
    "\x1b[107m": "white", 
    }

def display_text(ansi_text, text_window):
    '''解析ansi转义字符并用text组件显示'''
    ansi_list = re.findall(ANSI_PATTERN, ansi_text)
    color = None
    bg_color = None 
    text_font = (TEXT_FONT_NAME, TEXT_FONT_SIZE, "normal")
    bold = False
    italic = False
    overstrike = False
    text_list = re.split(ANSI_PATTERN, ansi_text)
    first_text = True
    if ansi_list == []:
        text_window.insert("end", text_list[0] + "\n")
    else:
        for text_index in range(len(text_list)):
            if ansi_list != [] and not first_text:
                ansi = ansi_list.pop(0)
                num_match  = re.search(r"[0-9]+", ansi)

                if num_match:
                    num = int(num_match.group())
                    if num == 1:
                        bold = True
                    elif num == 3:
                        italic = True
                    elif num == 4:
                        overstrike = True
                    elif 30 <= num <= 37 or 90 <= num <= 97:
                        color = ANSI_TEXT_COLOR_DIC[ansi]
                    elif 40 <= num <= 47 or 100 <= num <= 107:
                        bg_color = ANSI_BG_COLOR_DIC[ansi]

                if bold and italic:
                    text_font = (TEXT_FONT_NAME, TEXT_FONT_SIZE, "bold italic")
                elif bold:
                    text_font = (TEXT_FONT_NAME, TEXT_FONT_SIZE, "bold")
                elif italic:
                    text_font = (TEXT_FONT_NAME, TEXT_FONT_SIZE, "italic")

            if text_list[text_index]:
                text = text_list[text_index]
                tag_name = f"tag_{next(tag_count)}"
                text_window.tag_config(tag_name, foreground=color, background=bg_color, font=text_font, overstrike=overstrike)
                text_window.insert("end", text, tag_name)
                color = None
                bg_color = None 
                text_font = (TEXT_FONT_NAME, TEXT_FONT_SIZE, "normal")

            first_text = False

        text_window.insert("end", "\n")
