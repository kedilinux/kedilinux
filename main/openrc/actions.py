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
        # mesontools passes /usr/sbin and /usr/bin; OpenRC belongs in /sbin and /bin
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

    # Ship empty runlevels: which services are enabled is up to the system,
    # and pisi would bring removed links back on every upgrade.
    pisitools.remove("/etc/runlevels/*/*")

    pisitools.dodoc("LICENSE", "README*")
