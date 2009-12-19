#!/usr/bin/env python
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

import os.path as op

from hsdocgen import generate_help, filters

def generate(windows=False):
    tix = filters.tixgen("https://hardcoded.lighthouseapp.com/projects/31473-moneyguru/tickets/{0}")
    basepath = op.dirname(__file__)
    generate_help.main(basepath, op.join(basepath, 'moneyguru_help'), force_render=True, tix=tix, windows=windows)
