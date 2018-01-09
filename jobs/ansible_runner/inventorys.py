# ~*~ coding: utf-8 ~*~
from ansible.vars.manager import VariableManager
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager

class JMSInventoryManager(InventoryManager):
    '''提供生成Ansible inventory对象的方法'''
    def __init__(self, hosts):
        '''
        @parameter hosts: 主机信息,可能为两种情形,
        单机：[{ip:, port:, vars: {}}, {}]or 
        组：{group1:[{ip:, port:, vars: {}}, {}], }
        '''
    loader = DataLoader()
    super(JMSInventoryManager, self).__init__(loader = loader)
    self.parse_inventory(hosts)
    
    def parse_inventory(hosts):
        
        try:
            if instance(hosts, list):
                myaddhost(hosts)
            elif instance(hosts, dict):
                for groupname, host_list in hosts.iteritems():
                    myaddhost(hosts, groupname)
        except:
            print("JMSInventoryManager error")
            pass
            
            
    def myaddhost(self, host_list, group = None):
        '''
        按照自己的规则组织inventory
        @parameter host_list: 主机列表字典
        @parameter group: 组名
        '''
        inventory = self._inventory
        #创建未存在的组
        if groupname and groupname not in inventory.groups:
            self.add_group(groupname)
            
        for hostinfo in host_list:
            ip = hostinfo["ip"]
            port = hostinfo["port"]
            inventory.add_host(ip, group, port)


if __name__ == "__main__":
    hosts = [
        {
            "hostname": 'host',
            "ip": ip,
            "port": port,
            "username": username,
            "password": password,
        },
    ]
    obj = JMSInventoryManager(hosts)
    print obj.hosts