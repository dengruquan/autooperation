#-*- coding: utf8 -*-
#===========================================
#借鉴ansible源码编写adhoc和playbook
#===========================================

from ansible.cli.adhoc import AdHocCLI
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from  .callback     import   AdHocResultCallback, PlaybookResultCallBack, CommandResultCallback

class MyAdhoc(AdHocCLI):
    '''继承AdHocCLI类，只是编辑自己的run函数'''
    def __init__(self, hosts):
        self.inventory = JMSInventoryManager(hosts)
        self.loader = DataLoader()
        self.variable_manager = VariableManager(loader = self.loader, inventory = self.inventory)
        self.passwords = {}
        self.gather_facts = "no"
        
        
    @staticmethod
    def check_module_args(module_name, module_args=''):
        if module_name in C.MODULE_REQUIRE_ARGS and not module_args:
            err = "No argument passed to '%s' module." % module_name
            print(err)
            return False
        return True
      
      
    def run(self, task_tuple, pattern='all', task_name='Ansible Ad-Hoc'):
        no_hosts = False
        if len(inventory.list_hosts()) == 0:
            # Empty inventory
            no_hosts = True

        hosts = inventory.list_hosts(pattern)
        if not hosts:
            raise AnsibleError(
                "pattern: %s  dose not match any hosts." % self.pattern)
        
        for module, args in task_tuple:
            if not self.check_module_args(module, args):
                return
            self.tasks.append(
                dict(action=dict(
                    module=module,
                    args=args,
                ))
            )
            
        cb = AdHocResultCallback()
        
        play_source = dict(
            name = task_name,
            hosts = pattern,
            gather_facts = self.gather_facts,
            tasks = self.tasks
        )

        play = Play().load(
            play_source,
            variable_manager = self.variable_manager,
            loader = self.loader,
        )
        
        self._tqm = None
        try:
            self._tqm = TaskQueueManager(
                inventory = self.inventory,
                variable_manager = self.variable_manager,
                loader = self.loader,
                # options = self.options,
                passwords = self.passwords,
                stdout_callback = cb,
            )

            result = self._tqm.run(play)
        finally:
            if self._tqm:
                self._tqm.cleanup()
            if loader:
                loader.cleanup_all_tmp_files()
        
        #todo
        print()
        #end
        return cb.result_q
        
        
if __name__ == "__main__":
    ip = "192.168.15.15"
    port = 22
    username = ""
    password = ""
    hosts = [
        {
            "hostname": 'host',
            "ip": ip ,
            "port": port,
            "username": username,
            "password": password,
        },
    ]

    hosts_dict = {
	"kg" : hosts
	}

    obj = MyAdhoc(hosts)
    print(obj.run())
 
             
