# -*- coding:utf8 -*-
#============================
#调用ansible命令实现指定主机
#免密码登录
#============================
host_path = r"/data/ansible/playbook/hosts"
command = "/usr/bin/ansible-playbook -i /data/ansible/playbook/hosts /data/ansible/playbook/ssh-addkey.yml -v"

    
    
def WriteHost(hosts):
    '''编辑hosts内容'''
 
    with open(host_path, "w") as f:
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
    
    
=======
class A():
    def __init__(self):
    
       self.public_ip = "xxx" 
       self.ssh_port = 22
       self.user = "kg"
       self.passwd = ""
if __name__ == "__main__":
    sshkey(obj)

