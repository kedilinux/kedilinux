#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import pisitools

def setup():
    pass

def build():
    pass

def install():
    pisitools.doexe("iwd.initd-r1", "/etc/init.d")
    pisitools.rename("/etc/init.d/iwd.initd-r1", "iwd")