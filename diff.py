#!/usr/bin/python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import os
from postgres_ddl.Diff import Diff

PATH_CURRENT = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument(
        "-c", "--config",
        help    = "Path to config file",
        default = os.path.join(PATH_CURRENT, "config.json"),
    )

    parser.add_argument(
        "-s", "--source",
        help    = "Source connect name from config file",
        default = "source",
    )

    parser.add_argument(
        "-t", "--target",
        help    = "Target connect name from config file",
        default = "target",
    )

    parser.add_argument(
        "-f", "--folder",
        help = "Path to result folder",
        default = os.path.join(PATH_CURRENT, "result"),
    )

    args = parser.parse_args()

    Diff(
        path_config    = args.config,
        path_result    = args.folder,
        connect_source = args.source,
        connect_target = args.target
    ).Run()
