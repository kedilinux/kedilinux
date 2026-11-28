#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import mesontools
from pisi.actionsapi import pisitools

def setup():
    options = [
        "-Dtui=disabled",
        "-Dtray=sni",
    ]
    mesontools.configure(" ".join(options))

def build():
    mesontools.build()

def install():
    mesontools.install()
    pisitools.domove("/etc/xdg/autostart/org.iwdapplet.IwdApplet.desktop", "/etc/autostart")
    pisitools.removeDir("/etc/xdg")
    pisitools.dodoc("README.md", "LICENSE")
    pisitools.dosed("/etc/autostart/org.iwdapplet.IwdApplet.desktop", "^Exec=.*", "Exec=env GTK_THEME=Kedi-dark iwd-applet")
