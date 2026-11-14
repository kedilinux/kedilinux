#!/usr/bin/python
# -*- coding: utf-8 -*-

from pisi.actionsapi import pisitools

def setup():
    pass

def build():
    pass

def install():
    pisitools.doexe("syslogd.initd", "/etc/init.d")
    pisitools.rename("/etc/init.d/syslogd.initd", "syslogd")