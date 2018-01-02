# -*- coding:utf8 -*-
#============================
#调用ansible命令实现指定主机
#免密码登录
#============================
host_path = r"/data/ansible/playbook/hosts"
command =" /usr/bin/ansible-playbook -i /data/ansible/playbook/hosts /data/ansible/playbook/ssh-addkey.yml -v"


def sshkey(obj):
    '''实现ssh免密码登录'''
    WriteHost(obj)
    DoCommamd(command)
    
    
def WriteHost(obj):
    '''编辑hosts内容'''
    public_ip = obj.public_ip
    ssh_port = obj.ssh_port
    ssh_user = obj.user
    ssh_pass = obj.passwd
    hosts = '''
    [{}]
    {}
    [{}:vars]
    ansible_ssh_port = {}
    ansible_ssh_user = {}
    ansible_ssh_pass = {}'''.format(public_ip, public_ip, public_ip, ssh_port, ssh_user, ssh_pass)
    
    with open(host_path, "w") as f:
        f.write(hosts)

    
def DoCommamd(cmd):
    '''执行shell命令'''
    import os
    print (os.system(cmd))


class A():
    def __init__(self):
    
       self.public_ip = "xxx" 
       self.ssh_port = 22
       self.user = "kg"
       self.passwd = ""
if __name__ == "__main__":
    obj = A()
    sshkey(obj)
    #DoCommamd(" /usr/bin/ansible-playbook -i /data/ansible/playbook/hosts /data/ansible/playbook/ssh-addkey.yml")
    
