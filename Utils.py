# -*- coding: utf-8 -*-
# /usr/bin/env python

"""
create by yang on 16-5-26
"""

import os
import sys
import uuid
import random
import time
import commands
import functools

__author__ = 'muyidixin@126.com'
__VM_NAME_PREFIX = "xipu-win"
__vm_index = 0

reg_txt = '''[HKLM\SYSTEM\ControlSet001\Control\ComputerName\ActiveComputerName]
"ComputerName"="%s"

[HKLM\SYSTEM\ControlSet001\Control\ComputerName\ComputerName]
"ComputerName"="%s"

[HKLM\SYSTEM\ControlSet001\Services\Tcpip\Parameters]
"Hostname"="%s"

[HKLM\SYSTEM\ControlSet001\Services\Tcpip\Parameters]
"NV Hostname"="%s"'''


def timeit(func):
    @functools.wraps(func)
    def warp(*args, **kwargs):
        print "execute '%s' start: %s" % \
              (func.__name__,
               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        start = time.time()
        ret = func(*args, **kwargs)
        print "execute '%s' end: %s, elapsed time: %.3s s" % \
              (func.__name__,
               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
               time.time() - start)
        return ret

    return warp


def random_mac():
    mac = [0x52, 0x54, 0x00,
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: '%02x' % x, mac))


def random_uuid():
    return str(uuid.uuid1())


def gen_compute_name(vm_name_prefix):
    """ generate compute name
    :param vm_name_prefix: vm name prefix
    :return:
    """
    random_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return "%s-%s" % (vm_name_prefix if vm_name_prefix else __VM_NAME_PREFIX,
                      ''.join(random.sample(random_list, 12)))


def alter_vm_compute_name(image_original, compute_name):
    reg_file_path = "/tmp/win-reg.reg"

    if not os.path.exists(reg_file_path):
        os.system("touch %s" % reg_file_path)

    compute_name = compute_name[:15]
    with open(reg_file_path, 'w') as reg:
        reg.write(reg_txt % (compute_name, compute_name,
                             compute_name, compute_name))
    cmd = "virt-win-reg --merge %s %s" % (image_original, reg_file_path)
    if commands.getstatusoutput(cmd)[0] != 0:
        print "change the windows image's name did not finished!"


@timeit
def main():
    print(random_mac())
    print(random_uuid())
    print gen_compute_name("vm")
    if os.geteuid():
        args = [sys.executable] + sys.argv
        # 下面两种写法，一种使用su，一种使用sudo，都可以
        os.execlp('su', 'su', '-c', ' '.join(args))
        # os.execlp('sudo', 'sudo', *args)
    alter_vm_compute_name("win2k3-m8AsrdEL1Rte", "win2k3-m8AsrdEL1Rte")


if __name__ == "__main__":
    main()
