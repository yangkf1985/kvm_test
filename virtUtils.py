# -*- coding: utf-8 -*-
# /usr/bin/env python

"""
create by yang on 16-6-1
"""
import guestfs
import hivex

__author__ = 'muyidixin@126.com'


def alter_vm_compute_name(vm_name):
    # Use libguestfs to download the HKEY_LOCAL_MACHINE\SYSTEM hive.
    # g = guestfs.GuestFS()
    # g.add_domain(vm_name)
    # g.launch()
    #
    # roots = g.inspect_os()
    # root = roots[0]
    # g.mount_options("", root, "/")

    # systemroot = g.inspect_get_windows_systemroot(root)
    # path = "%s/system32/config/system" % systemroot
    # path = g.case_sensitive_path(path)
    # g.download(path, "/tmp/system")

    # Open the hive file for writing.
    h = hivex.Hivex("/tmp/system", write=True)

    # Navigate down to the TCP/IP parameters.
    key = h.root()
    key = h.node_get_child(key, "ControlSet001")
    key = h.node_get_child(key, "Services")
    key = h.node_get_child(key, "Tcpip")
    key = h.node_get_child(key, "Parameters")

    # Get the old hostname.
    val = h.node_get_value(key, "Hostname")
    old_hostname = h.value_value(val)

    # Keep the old type (probably 1 = string)
    type = old_hostname[0]

    # The registry key is encoded as UTF-16LE.
    old_hostname = old_hostname[1].decode('utf-16le').encode('utf-8')

    print "old hostname = %s" % old_hostname

    # Change the hostname.
    new_hostname = vm_name.encode('utf-16le')
    new_value = {'key': "Hostname", 't': type,
                 'value': new_hostname}
    h.node_set_value(key, new_value)

    # Commit the changes to the hive.
    h.commit(None)

    # # Upload the hive back to the guest.
    # g.upload("/tmp/system", path)
    #
    # # This is only needed for libguestfs < 1.5.24, but
    # # it won't hurt for newer versions.
    # g.sync()


def main():
    alter_vm_compute_name("xipu-winxp-cnhsk9YR1Vwi")


if __name__ == "__main__":
    main()
