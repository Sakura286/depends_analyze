# pip install semver
from semver.version import Version
import re
import copy


PACKAGES_FILE = "Packages"


class Package:

    def __init__(self, pkg_str: str):
        self.name = re.search(
            r'Package: ([a-z0-9-:]+)$', pkg_str, re.M).group(1)

        version_group = re.search(r'Version: ([\S]+)$', pkg_str, re.M)
        if version_group:
            self.version = version_group.group(1)
        else:
            self.version = ""

        depends_group = re.search(r'Depends: ([^\n]+)$', pkg_str, re.M)
        if depends_group:
            self.depends = self.split_depend(depends_group.group(1))
        else:
            self.depends = []

    def split_depend(self, depend_str: str):
        return re.compile(r'[a-z0-9-:]{4,}').findall(depend_str)


def get_duplicate_id(pkgs, pkg):
    i = 0
    while i < len(pkgs):
        if pkgs[i].name == pkg.name:
            return i
        i += 1
    return -1


def update_duplicate(pkg1, pkg2):
    if Version.parse(pkg1.version) < Version.parse(pkg2.version):
        pkg1.version = pkg2.version
        pkg1.depends = pkg2.depends


pkgs = []

# initialize
pkgs_str = []
with open(PACKAGES_FILE) as file:
    pkgs_str = file.read().split("\n\n")

for pkg_str in pkgs_str:
    if not pkg_str:
        continue
    pkg = Package(pkg_str)
    dup_id = get_duplicate_id(pkgs, pkg)
    if dup_id == -1:
        pkgs.append(pkg)
    else:
        update_duplicate(pkgs[dup_id], pkg)


# remove debian official pkgs in depends
pkg_name_list = []
for pkg in pkgs:
    pkg_name_list.append(pkg.name)

for pkg in pkgs:
    depends = copy.copy(pkg.depends)
    for depend in depends:
        if not depend in pkg_name_list:
            if pkg.depends:
                pkg.depends.remove(depend)

# print result
for pkg in pkgs:
    print("Package: {0}\nVersion: {1}\nDepends: {2}\n".format(
        pkg.name, pkg.version, str(pkg.depends)))


# generate the chain


# traverse the chain