from django.db import models

#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models


ASSET_STATUS = (
    (str(1), u"使用中"),
    (str(2), u"未使用"),
    (str(3), u"故障"),
    (str(4), u"其它"),
    )

ASSET_TYPE = (
    (str(1), u"物理机"),
    (str(2), u"虚拟机"),
    (str(3), u"容器"),
    (str(4), u"网络设备"),
    (str(5), u"其他")
    )

   

class Operator(models.Model):
    '''运营商'''
    name = models.CharField(verbose_name = "运营商", max_length=30, unique=True)
    desc = models.CharField(verbose_name = "描述", max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class  Meta:
        db_table ="operator"
        
        
class GameProject(models.Model):
    '''项目'''
    name = models.CharField(verbose_name = "游戏项目", max_length=30, unique=True)
    desc = models.CharField(verbose_name = "描述", max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.name
        
    class  Meta:
        db_table ="gameproject"  
        

class GameVersion(models.Model):
    '''项目版本'''
    name = models.CharField(verbose_name="游戏版本名称", max_length=30, unique=True)
    project_name = models.ForeignKey(GameProject, null=True, verbose_name = "游戏项目", on_delete=models.CASCADE)
    desc = models.CharField(verbose_name = "描述", max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
        
    class  Meta:
        db_table ="gameversion"

        
class Host(models.Model):
    '''主机信息'''
    operator = models.ForeignKey(Operator, verbose_name = "运营商", on_delete=models.CASCADE)
    project = models.ForeignKey(GameProject, verbose_name = "游戏项目", null=True, on_delete=models.CASCADE)
    version = models.ForeignKey(GameVersion, verbose_name=u"版本名称", on_delete=models.CASCADE, null=True, blank=True)
    
    describe_name = models.CharField(max_length = 50, verbose_name = "名称", null=True, blank=True)
    hostname = models.CharField(max_length=50, verbose_name=u"主机名", unique=True)
    
    os = models.CharField(verbose_name = "操作系统", max_length=100, null=True, blank=True)
    cpu_num = models.IntegerField(verbose_name = "CPU数量", default = 4)
    memory = models.CharField(verbose_name = "内存大小", max_length=30, null=True, blank=True)
    disk = models.CharField(verbose_name = "硬盘信息", max_length=255, null=True, blank=True)
    
    private_ip = models.GenericIPAddressField(verbose_name = "内网IP", max_length=15, null=True, blank=True)
    public_ip = models.GenericIPAddressField(verbose_name = "公网IP", max_length=15, null=True, blank=True)
    
    user = models.CharField(verbose_name = "密码", max_length=50, null=True, blank=True, default = "root")
    passwd = models.CharField(verbose_name = "密码", max_length=50, null=True, blank=True)
    ssh_port = models.IntegerField(verbose_name = "ssh端口", default = 22)
    
    asset_type = models.CharField(verbose_name = "设备类型", choices=ASSET_TYPE, max_length=30, null=True, blank=True)
    status = models.CharField(verbose_name = "设备状态", choices=ASSET_STATUS, max_length=30, null=True, blank=True)
    memo = models.TextField(verbose_name = "备注信息", max_length=200, null=True, blank=True)

    def __str__(self):
        return self.hostname
        
    class  Meta:
        db_table ="host"
        verbose_name="主机管理"
        # verbose_name_plural = '资产管理'
        # permissions = {
            # ('read_asset',u"只读资产管理"),
        # }
        
        

