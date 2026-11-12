#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools

def setup():
    pass

def build():
    autotools.build()

def install():
    autotools.install()
    autotools.rawInstall(parameters = 'DESTDIR=%s' % get.installDIR())
