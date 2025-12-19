def login_ini(data,path):
    file=open(path,"r",encoding="utf-8")
    lines=file.readlines()
    file.close()
    lines[11]='Account ={ Login = "'+str(data[1])+'", Password = "'+str(data[2])+'" }\n' #填充账户密码
    lines[12]='Server = { Host = "'+str(data[3])+'" }\n' #填充服务器IP
    lines[13]='AccountType = "'+str(data[0])+'" \n' #填充登录方式
    lines[14]='ProfileName = "'+str(data[5])+'"\n'
    lines[16]='AuthServer = { Host = "'+str(data[4])+'", Port = 443 }\n' #填充认证服务器
    lines[27]='MinecraftVersion = "1.20.4" \n' #填充游戏版本
    file=open(path,"w",encoding="utf-8")
    file.writelines(lines)
    print("修改ini成功")

