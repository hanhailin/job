#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import urllib2
from ansible_api import AnsibleAPI
from unicodeformat import unicodeformat



class AnsiInterface(AnsibleAPI):
    def __init__(self, resource, *args, **kwargs):
        super(AnsiInterface, self).__init__(resource, *args, **kwargs)

    @staticmethod
    def deal_result(info):
        host_ips = info.get('success').keys()
        info['success'] = host_ips

        error_ips = info.get('failed')
        error_msg = {}
        for key, value in error_ips.items():
            temp = {}
            temp[key] = value.get('stderr')
            error_msg.update(temp)
        info['failed'] = error_msg
        return json.dumps(info)

    def copy_file(self, host_list, src=None, dest=None):
        """
        copy file
        """
        module_args = "src=%s  dest=%s mode=0700"%(src, dest)
        self.run(host_list, 'copy', module_args)
        result = self.get_result()
        return self.deal_result(result)

    def exec_command(self, host_list, cmds):
        """
        commands
        """
        self.run(host_list, 'command', cmds)
        result = self.get_result()
        return self.deal_result(result)

    def exec_script(self, host_list, path):
        """
        在远程主机执行shell命令或者.sh脚本
        """
        self.run(host_list, 'shell', path)
        result = self.get_result()
        return self.deal_result(result)



if __name__ == "__main__":

    req = urllib2.Request('http://172.16.100.50/jasset/asset/inventory/')
    response = urllib2.urlopen(req)
    resource = unicodeformat(json.loads(response.read()))['invernory']
    interface = AnsiInterface(resource)
    print "copy: ", interface.copy_file(['localhost.localdomain'], src='/Users/hanhailin/Desktop/maochang/utils/hostname.sh', dest='/home/')
    # print "commands: ", interface.exec_command(['172.16.100.50'], 'hostname')
    # print "shell: ", interface.exec_script(['172.20.3.18', '172.20.3.31'], 'chdir=/home ls')
    print "shell: ", interface.exec_script(['localhost.localdomain', 'paas.blueking.com'], '/bin/bash /home/hostname.sh')
