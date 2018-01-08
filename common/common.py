Host_Path = r"/data/ansible/playbook/hosts"
Ssh_Command = "/usr/bin/ansible-playbook -i {} /data/ansible/playbook/ssh-addkey.yml -v".format(Host_Path)

setup_Command = "ansible -m setup --tree out/ all"
