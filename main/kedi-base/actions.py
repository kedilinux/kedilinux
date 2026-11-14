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
    pisitools.insinto("/etc/init.d", "hostname-hosts")
    pisitools.insinto("/etc/pisi", "blacklist")
    pisitools.insinto("/etc/tmpfiles.d", "udev.conf")
    pisitools.dodir("/etc/mudur/services/disabled")
    pisitools.dosym("../proc/self/mounts", "/etc/mtab")
