from celery import shared_task
from common import mysshkey
from subprocess import Popen, PIPE


@shared_task
def deal_sshkey(public_ip, ssh_port, user, passwd):
	'''ssh免密码登录'''
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


