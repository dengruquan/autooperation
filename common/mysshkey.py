# -*- coding:utf8 -*-
#============================
#调用ansible命令实现指定主机
#免密码登录
#============================
# Host_Path = r"/data/ansible/playbook/hosts"
from . import common

def WriteHost(hosts):
    '''编辑hosts内容'''
 
    with open(common.Host_Path, "w") as f:
        f.write(hosts)

    
def DoCommamd(cmd):
    '''执行shell命令'''
    import os
    print (os.system(cmd))


def SendSSHKey(*args):
    '''使用ansible实现批量免密码登录'''
    WriteHost(args)
    DoCommamd(command)


if __name__ == "__main__":
    args = "", "", "", ""
    SendSSHKey(*args)


