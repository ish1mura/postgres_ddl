#!/usr/bin/python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import os
from postgres_ddl.Diff import Diff

if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument(
        "-c", "--config",
        help    = "Path to config file",
        default = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json"),
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

    args = parser.parse_args()

    Diff(
        path_config    = args.config,
        connect_source = args.source,
        connect_target = args.target
    ).Run()
