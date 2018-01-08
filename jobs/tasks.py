from celery import shared_task
from common import mysshkey
from subprocess import Popen, PIPE


@shared_task
def deal_sshkey(public_ip, ssh_port, user, passwd, cmd):
	'''
    ssh免密码登录
    @parameter public_ip : 主机外网ip
    @parameter ssh_port : 主机ssh端口
    @parameter user : 主机ssh登录用户
    @parameter passwd : 主机外网密码
    @parameter cmd : 实现ssh免密码登录命令
    '''
    hosts = '''
    [{0}]
    {0}
    [{0}:vars]
    ansible_ssh_port = {1}
    ansible_ssh_user = {2}
    ansible_ssh_pass = {3}'''.format(public_ip,  ssh_port, ssh_user, ssh_pass)
    
	mysshkey.WriteHost(hosts)	
	DoShellCommand(cmd)


@shared_task
def deal_setupinfo(public_ip, ssh_port, cmd):
	'''使用ansible获取硬件信息'''
	hosts = '''
    [{0}]
    {0}
    [{0}:vars]
    ansible_ssh_port = {1}
    '''.format(public_ip,  ssh_port)
    mysshkey.WriteHost(hosts)
    DoShellCommand(cmd)
   

@shared_task
def DoShellCommand(cmd):
	'''执行shell命令'''
	Popen(cmd, shell = True)


