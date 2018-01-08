Host_Path = r"/data/ansible/playbook/hosts"
SSH_Command = "/usr/bin/ansible-playbook -i {} /data/ansible/playbook/ssh-addkey.yml -v".format(Host_Path)

setup_Command = "ansible -m setup --tree out/ all"


def deal_disk(disk_list):
    '''
    特殊处理磁盘容量
    @parameter disk_list: 磁盘列表[{}, {}]
    @return disk_total :返回指定挂载点中最大容量值为磁盘容量
    '''
    mount_path = {"/", "/data"}
    disk_total = 0
    tmp_disk_list = []
    size = 1024
    for mount_dict in disk_list:
        if mount_dict["mount"] not in mount_path:
            continue
        tmp_disk_list.append(mount_dict["size_available"])

    disk_total = int(max(tmp_disk_list)/size**3 )

    return disk_total


def deal_hostip(ipv4_list):
    '''
    处理外网ip和内网ip
    @parameter ipv4_list: ipv4ip地址：[]
    return private_ip
    '''
    private_ip_set = {"192", "10"}
    for ip in ipv4_list:
        start_ip = ip.split(".")[0]
        if start_ip not in private_ip_set:
            continue
        return ip

