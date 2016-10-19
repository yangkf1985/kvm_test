# -*- coding: utf-8 -*-
# /usr/bin/env python

"""
create by yang on 16-5-26
"""
import Utils

__author__ = 'muyidixin@126.com'


def main():
    for i in xrange(100):
        print("%s: %s" % (i, Utils.gen_compute_name()))


if __name__ == "__main__":
    main()