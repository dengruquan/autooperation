from celery import shared_task
from django.http import HttpResponseRedirect 
from subprocess import Popen, PIPE
from jobs.ansible_runner import runner 
from cmdb.models import Host
from common import mysshkey, common

@shared_task
def deal_sshkey(hostid, public_ip, ssh_port, user, passwd, cmd):
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
    #免密码登录后同步硬件信息
    run(hostid, public_ip, ssh_port, user, passwd)


@shared_task
def callsetup(hostid, assets, task_tuple):
    '''执行ansible setup模块获取硬件信息'''
    runobj = runner.AdHocRunner(assets)
    result = runobj.run(task_tuple=task_tuple, pattern='all', task_name='Ansible Ad-hoc')
    return (hostid, result)


@shared_task
def parse_setupinfo(setupdata, hostid):
    '''
    解析硬件信息
    @parameter hostid: 主机id
    @parameter setupdata: 硬件信息字典{}
    '''
    try:
    	data = setupdata['contacted']['host'][0]['ansible_facts']
        hostname = data['ansible_nodename']
        os = " ".join((data['ansible_distribution'], data['ansible_distribution_version']))
        cpu_num = data["ansible_processor_vcpus"]
        memory = data["ansible_memtotal_mb"]
        disk = common.deal_disk(data["ansible_mounts"])
        private_ip = common.deal_hostip(data["ansible_all_ipv4_addresses"])
        
        ass = Host.objects.get(id=hostid)
        ass.hostname = hostname
        ass.os = os
        ass.cpu_num = cpu_num
        ass.memory = memory
        ass.disk = disk
        ass.private_ip = private_ip
        ass.save()

    except:
        print("data=", data) 
        pass
   

@shared_task
def DoShellCommand(cmd):
	'''执行shell命令'''
	Popen(cmd, shell = True)


def run(hostid, ip, port, username, password):
    '''
    执行ansible命令
    @parameter hostid : 主机数据表id
    @parameter ip : 主机外网ip
    @parameter port : ssh端口
    @parameter username : 用户名
    @parameter password : 用户密码
    '''
    assets = [
        {
            "hostname": 'host',
            "ip": ip,
            "port": port,
            "username": username,
            "password": password,
        },
    ]

    task_tuple = (('setup', ''),)
    callsetup.apply_async((assets, task_tuple), link=parse_setupinfo.s(hostid))
    
    return HttpResponseRedirect("/cmdb/asset.html")
