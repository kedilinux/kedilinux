#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import mesontools
from pisi.actionsapi import pisitools

def setup():
    options = [
        "--buildtype=release",
        "--sbindir=/sbin",
        "--bindir=/bin",
        "--libexecdir=/usr/libexec",
        "-Dpam=false",
        "-Duucp_group=root",
        "-Dsysvinit=true",
        "-Dselinux=disabled",
        "-Daudit=disabled",
        "-Dbash-completions=true",
        "-Dzsh-completions=false",
        "-Dpkgconfig=true",
        """-Dbranding='"Kedi GNU/Linux"'""",
    ]
    mesontools.configure(" ".join(options))

def build():
    mesontools.build()

def install():
    mesontools.install()

    pisitools.remove("/etc/runlevels/*/*")

    pisitools.dodoc("LICENSE", "README*")
