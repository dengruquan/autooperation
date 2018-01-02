# -*- coding:utf8 -*-
#============================
#调用ansible命令实现指定主机
#免密码登录
#============================
host_path = r"/data/ansible/playbook/hosts"
command = r"/data/ansible/playbook/ssh-addkey.yml"


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
    print os.system(cmd)


class A():
    def __init__(self):
       self.public_ip = "192.168.15.15" 
       self.ssh_port = 22
       self.user = "kg"
       self.passwd = "kg88888888"
    
if __name__ == "__main__":
    # obj = {
    # "public_ip": "192.168.15.15",
    # "ssh_port" : 22,
    # "ssh_user" : "kg",
    # "ssh_pass" : "kg88888888"
    # }
    # obj = A()
    # sshkey(obj)
    DoCommamd("cat /data/ansible/playbook/ssh-addkey.yml")
    