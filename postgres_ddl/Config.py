#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import logging
import os

class Config():
    Connects = {}

    WorkPath = ""

    Threads = 4

    Indent = " " * 2

    NL = chr(10)

    SchemasExclude = [
        "information_schema",
        "pg_catalog",
    ]

    TablesSequencesGrantsShow = False

    ForeignServersUserMappingsShow = True

    FunctionsParamSign = ":="
    FunctionsFolderName = None
    TriggersFolderName = None

    @staticmethod
    def Parse(path):
        assert os.path.exists(path), \
            f"Config file '{path}' is not exists"

        with open(path, "r", encoding="utf8") as rf:
            data = json.loads(rf.read())

        assert data is not None, \
            "Config file is empty"

        assert isinstance(data, dict), \
            "Config file must contains dict"

        assert len(data or {}) > 0, \
            "Config file is empty"

        Config.Connects = data.get("connects", Config.Connects)
        assert len(Config.Connects.keys()) > 0, \
            "No connects in config"

        Config.WorkPath = data.get("path", Config.WorkPath).strip()
        assert len(Config.WorkPath), \
            "No work path in config"

        Config.Threads = data.get("threads", Config.Threads)

        Config.Indent = " " * data.get("indent", Config.Indent)

        Config.NL = data.get("new_line", Config.NL)

        schemas = data.get("schemas", {})
        Config.SchemasExclude = schemas.get("exclude", Config.SchemasExclude)

        tables = data.get("tables", {})
        Config.TablesSequencesGrantsShow = (tables.get("sequence_grants_show") is True)

        foreign_servers = data.get("foreign_servers", {})
        Config.ForeignServersUserMappingsShow = (foreign_servers.get("user_mappings_show") is not False)

        functions = data.get("functions", {})
        Config.FunctionsFolderName = functions.get("folder_name")
        Config.FunctionsParamSign = functions.get("param_sign") or Config.FunctionsParamSign

        triggers = data.get("triggers", {})
        Config.TriggersFolderName = triggers.get("folder_name")

        logs = data.get("logs", {})

        logs_level = logs.get("level", "INFO").strip().upper()
        if logs_level == "DEBUG":
            logs_level = logging.DEBUG
        else:
            logs_level = logging.INFO

        logs_format = logs.get("format", "%(asctime)s [%(levelname)s] %(message)s")

        logs_handlers = [logging.StreamHandler()]

        logs_path = logs.get("path", "").strip()
        if len(logs_path) > 0:
            logs_handlers.append(logging.handlers.TimedRotatingFileHandler(logs_path, backupCount=7, when='D', interval=1))

        logging.basicConfig(
            level    = logs_level,
            format   = logs_format,
            handlers = logs_handlers
        )
