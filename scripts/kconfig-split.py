#!/usr/bin/env python

# This is a slightly modified version of ChromiumOS' splitconfig
# https://chromium.googlesource.com/chromiumos/third_party/kernel/+/stabilize-5899.B-chromeos-3.14/chromeos/scripts/splitconfig

"""See this page for more details:
http://dev.chromium.org/chromium-os/how-tos-and-troubleshooting/kernel-configuration
"""

import os
import re
import sys

allconfigs = {}

# Parse config files
for config in sys.argv[1:]:

    allconfigs[config] = set()

    for line in open(config):
        m = re.match("#*\s*CONFIG_(\w+)[\s=](.*)$", line)
        if not m:
            continue
        option, value = m.groups()
        allconfigs[config].add((option, value))

# Split out common config options
common = allconfigs.values()[0].copy()
for config, value___ in allconfigs.items():
    common &= value___
for config, value_ in allconfigs.items():
    value_ -= common

allconfigs["common"] = common

# Generate new splitconfigs
for config, value__ in allconfigs.items():
    f = open("split-" + config, "w")
    for option, value in sorted(list(value__)):
        if value == "is not set":
            print >>f, "# CONFIG_%s %s" % (option, value)
        else:
            print >>f, "CONFIG_%s=%s" % (option, value)
    f.close()
