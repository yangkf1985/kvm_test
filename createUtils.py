
# -*- coding: utf-8 -*-
# /usr/bin/env python

"""
create by yang on 16-5-30
"""

import os
import sys
import shutil
import commands
from xml.dom.minidom import parseString

import Utils

__author__ = 'muyidixin@126.com'

__VM_XML_PATH = "/etc/libvirt/qemu"
__VM_DISK_PATH = "/home/yang/disk"
__VM_XML_TMPL = ""
__VM_DISK_TMPL = ""


def copy_vm_xml(src, dst):
    if os.path.exists(dst):
        return
    shutil.copy2(src=src, dst=dst)
    # cmd = "cp -r %s %s" % (src, dst)
    # if commands.getstatusoutput(cmd)[0] != 0:
    #     print "copy xml file failure!"


def alter_vm_xml(vm_xml, vm_name, vm_img, vm_uuid="", vm_mac=""):
    if not os.path.exists(vm_xml):
        return
    if not os.path.exists(vm_img):
        return

    with open(vm_xml, 'r') as read_vm_xml:
        doc_xml = parseString(read_vm_xml.read())

        name = doc_xml.getElementsByTagName('name')[0].firstChild
        name.nodeValue = vm_name

        uuid = doc_xml.getElementsByTagName('uuid')[0].firstChild
        uuid.nodeValue = vm_uuid

        for disk in doc_xml.getElementsByTagName('disk'):
            if disk.getAttribute('device') == 'disk':
                for node in disk.childNodes:
                    if node.nodeName == 'source':
                        node.setAttribute('file', vm_img)

        for interface in doc_xml.getElementsByTagName('interface'):
            for node in interface.childNodes:
                if node.nodeName == 'mac':
                    node.setAttribute('address', vm_mac)

        with open(vm_xml, 'w') as write_vm_xml:
            write_vm_xml.write(doc_xml.toxml())


def bak_vm_img(src_img, dst_img):
    if os.path.exists(dst_img):
        return

    cmd = "qemu-img create -f qcow2 -b %s %s" % (src_img, dst_img)
    if commands.getstatusoutput(cmd)[0] == 0:
        # vm_name = os.path.basename(dst_img)
        # Utils.alter_vm_compute_name(dst_img, vm_name)
        pass
    else:
        print "create backing file of source image failure!"


def create_and_boot_vm(vm_name):
    vm_xml = "%s/%s.xml" % (__VM_XML_PATH, vm_name)
    vm_img = "%s/%s.qcow2" % (__VM_DISK_PATH, vm_name)

    if not os.path.exists(vm_xml) \
            or not os.path.exists(vm_img):
        return

    cmd = "virsh define %s" % vm_xml
    if commands.getstatusoutput(cmd)[0] != 0:
        print "define vm domain failure!"
        return

    cmd = "virsh start %s" % vm_name
    if commands.getstatusoutput(cmd)[0] != 0:
        print "start vm failure!"


@Utils.timeit
def main(vm_tmpl_name, vm_prefix=None):
    if os.geteuid():
        args = [sys.executable] + sys.argv
        # 下面两种写法，一种使用su，一种使用sudo，都可以
        os.execlp('su', 'su', '-c', ' '.join(args))
        # os.execlp('sudo', 'sudo', *args)

    # 设置调试
    # import pdb
    # pdb.set_trace()

    dst_vm_name = Utils.gen_compute_name(vm_prefix)
    tmpl_xml = "%s/%s.xml" % (__VM_XML_PATH, vm_tmpl_name)
    dst_xml = "%s/%s.xml" % (__VM_XML_PATH, dst_vm_name)
    copy_vm_xml(tmpl_xml, dst_xml)

    tmpl_img = "%s/%s.qcow2" % (__VM_DISK_PATH, vm_tmpl_name)
    dst_vm_img = "%s/%s.qcow2" % (__VM_DISK_PATH, dst_vm_name)
    bak_vm_img(tmpl_img, dst_vm_img)

    dst_vm_mac = Utils.random_mac()
    dst_vm_uuid = Utils.random_uuid()
    alter_vm_xml(dst_xml, dst_vm_name, dst_vm_img, dst_vm_uuid, dst_vm_mac)
    create_and_boot_vm(dst_vm_name)

if __name__ == "__main__":
    main("win7", "win7")
