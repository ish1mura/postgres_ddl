#!/usr/bin/python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import os
from postgres_ddl.Grabber import Grabber

if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument(
        "-c", "--config",
        help = "Path to config file",
        default = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json"),
    )

    parser.add_argument(
        "-n", "--name",
        help = "Connect name from config file",
        default = "default",
    )

    args = parser.parse_args()

    Grabber(
        path_config  = args.config,
        connect_name = args.name
    ).Run()
