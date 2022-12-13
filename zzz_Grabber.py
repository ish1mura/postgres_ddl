#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
from postgres_ddl.Grabber import Grabber
from postgres_ddl.System import ReadConfig

if __name__ == '__main__':
    if len(sys.argv) > 1:
        path_config = sys.argv[1]
    else:
        path_config = "/".join([os.path.dirname(os.path.abspath(__file__)), "config_grab.json"])

    Grabber(ReadConfig(path_config)).Run()
