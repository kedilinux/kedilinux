#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
#
# Makes Kedi's merged binary repo index: Pisi's packages plus Kedi's, in one index.
#
#   pisi index --skip-signing        (in the folder with Kedi's .pisi files, as before)
#   python merge-index.py pisi-index.xml -o merged
#
# The first argument is Kedi's own index from `pisi index`. Pisi's index is downloaded
# from stable2 and checked against its .sha1sum. When a package is in both, Kedi's wins.
# Pisi's packages keep their paths; repo.kedilinux.org fetches and caches them from
# stable2 the first time someone downloads them.
#
# The output folder gets the same files `pisi index` writes (pisi-index.xml, .xz and
# their .sha1sum, plus a gpg .sig for each unless --skip-signing). Upload them to 1/.
# Run it again whenever Pisi updates; Kedi's own index stays the input every time.

from __future__ import print_function

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

PISI_INDEX = "https://stable2.pisilinux.org/pisi-index.xml.xz"


def sha1_file(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(256 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_sha1sum(path):
    # Like pisi: just the hex digest, no file name, no newline.
    with open(path + ".sha1sum", "w") as f:
        f.write(sha1_file(path))


def download_pisi_index(url, tmp):
    xz = os.path.join(tmp, "pisi-index.xml.xz")
    subprocess.check_call(["curl", "-fsSL", "-o", xz, url])
    subprocess.check_call(["curl", "-fsSL", "-o", xz + ".sha1sum", url + ".sha1sum"])
    with open(xz + ".sha1sum") as f:
        want = f.read().split()[0]
    got = sha1_file(xz)
    if got != want:
        sys.exit("Pisi's index doesn't match its .sha1sum (%s, expected %s), try again later" % (got, want))
    xml = os.path.join(tmp, "pisi-index.xml")
    with open(xml, "wb") as out:
        subprocess.check_call(["xz", "-dc", xz], stdout=out)
    return xml


def version(package):
    update = package.find("History/Update")
    return "%s-%s" % (update.findtext("Version"), update.get("release"))


def main():
    parser = argparse.ArgumentParser(description="Merge Kedi's index with Pisi's.")
    parser.add_argument("kedi_index", help="Kedi's own pisi-index.xml, from `pisi index`")
    parser.add_argument("-o", "--output", required=True, help="folder for the merged index files")
    parser.add_argument("--pisi-index", default=PISI_INDEX, help="Pisi's pisi-index.xml.xz URL")
    parser.add_argument("--skip-signing", action="store_true", help="don't run gpg --detach-sig")
    args = parser.parse_args()

    kedi = ET.parse(args.kedi_index).getroot()
    # A merged index has Pisi's <Distribution>; Kedi's own never does. Merging a merged
    # index would freeze every Pisi package at today's version as if it were Kedi's.
    if kedi.find("Distribution") is not None:
        sys.exit("%s is already a merged index; give the one from `pisi index`" % args.kedi_index)
    kedi_packages = kedi.findall("Package")
    kedi_names = set(p.findtext("Name") for p in kedi_packages)

    tmp = tempfile.mkdtemp(prefix="merge-index-")
    try:
        pisi = ET.parse(download_pisi_index(args.pisi_index, tmp)).getroot()
    finally:
        shutil.rmtree(tmp)

    merged = ET.Element("PISI")
    merged.text, merged.tail = pisi.text, pisi.tail
    pisi_count = 0
    replaced = []
    for element in list(pisi):
        if element.tag == "Package":
            name = element.findtext("Name")
            if name in kedi_names:
                replaced.append((name, version(element)))
                continue
            pisi_count += 1
        elif element.tag == "Distribution":
            # Pisi must not treat one of Kedi's packages as obsolete.
            obsoletes = element.find("Obsoletes")
            if obsoletes is not None:
                for p in list(obsoletes):
                    if p.text in kedi_names:
                        obsoletes.remove(p)
        merged.append(element)
    for package in kedi_packages:
        merged.append(package)

    if not os.path.isdir(args.output):
        os.makedirs(args.output)
    index = os.path.join(args.output, "pisi-index.xml")
    for old in [index + s for s in ("", ".sha1sum", ".sig", ".xz", ".xz.sha1sum", ".xz.sig")]:
        if os.path.exists(old):
            os.remove(old)
    ET.ElementTree(merged).write(index, encoding="utf-8")
    subprocess.check_call(["xz", "-9", "-k", index])
    write_sha1sum(index)
    write_sha1sum(index + ".xz")
    if not args.skip_signing:
        for path in (index, index + ".xz"):
            subprocess.check_call(["gpg", "--detach-sig", path])

    kedi_versions = dict((p.findtext("Name"), version(p)) for p in kedi_packages)
    print("%d packages from Pisi, %d from Kedi" % (pisi_count, len(kedi_packages)))
    for name, pisi_version in sorted(replaced):
        print("  %s: Kedi %s replaces Pisi %s" % (name, kedi_versions[name], pisi_version))
    print("Wrote %s/pisi-index.xml%s" % (args.output, "" if args.skip_signing else " (signed)"))


if __name__ == "__main__":
    main()
