# -*- coding:utf8 -*-
#============================
#调用ansible命令实现指定主机
#免密码登录
#============================
host_path = r"/data/ansible/playbook/hosts"
command = r"/data/ansible/playbook/ssh-addkey.yml"


def sshkey(*args):
    '''实现ssh免密码登录'''
    WriteHost(args)
    DoCommamd(command)
    
    
def WriteHost(hosts):
    '''编辑hosts内容'''
 
    with open(host_path, "w") as f:
        f.write(hosts)

    
def DoCommamd(cmd):
    '''执行shell命令'''
    import os
    print os.system(cmd)



def SendSSHKey(*args):
    '''使用ansible实现批量免密码登录'''
    obj = A(*args)
    sshkey(obj)


if __name__ == "__main__":
    args = "", "", "", ""
    sshkey(*args)
    
    