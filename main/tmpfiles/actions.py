#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import mesontools

def setup():
    options = " ".join([
        "-Dtests=false",
    ])
    mesontools.configure(options)

def build():
    mesontools.build()

def install():
    pisitools.insinto("/usr/bin", "build/src/tmpfiles/sd-tmpfiles")
    pisitools.dodoc("README.md", "LICENSE.LGPL2.1")
    pisitools.dosym("tmpfiles-setup", "/etc/init.d/systemd-tmpfiles-setup")
    pisitools.dosym("tmpfiles-setup-dev", "/etc/init.d/systemd-tmpfiles-setup-dev")
