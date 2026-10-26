#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
from shutil import rmtree
from multiprocessing import Pool

from postgres_ddl.Config import Config
from postgres_ddl.Database import Database
from postgres_ddl.System import FileDataProcess

class Grabber():
    def __init__(self, path_config, connect_name):
        Config.Parse(path_config)

        self.ConnectName = connect_name.strip().lower()
        assert len(self.ConnectName) > 0, \
            "No connect name"

    def NonSuperUserUndo(self):
        """
        Undo changes for superuser-only files
        """
        os.chdir(Config.WorkPath)
        res = subprocess.run(["git", "status", "--short"], shell=True, capture_output=True)
        res = res.stdout.decode("utf-8")
        res = FileDataProcess(res)
        for file in res.split(Config.NL):
            file = file[3:]
            if file.find("_logical") >= 0:
                subprocess.run(["git", "checkout", "-q", "--", file], shell=True)

    def WriteFile(self, file):
        with open(file.get("path"), "w", encoding="utf-8") as wf:
            wf.write(FileDataProcess(file.get("data")) + Config.NL)

    def Run(self):
        database = Database(self.ConnectName)
        database.Parse()

        if os.path.exists(Config.WorkPath):
            rmtree(Config.WorkPath)

        write_data = []
        for k,o in database.Objects.items():
            path = o.GetPath()
            if len(path) <= 0:
                continue

            file_name = o.GetFileName()
            if len(file_name) <= 0:
                continue
            file_name = file_name.replace("\\", "_")
            file_name = file_name.replace("/", "_")
            file_name = file_name.replace('"', "")

            path = [Config.WorkPath] + path
            path = os.path.sep.join(path)
            if not os.path.exists(path):
                os.makedirs(path)

            write_data.append({
                "path" : os.path.join(path, file_name),
                "data" : o.DDL_Create()
            })

        if (Config.Threads or 1) <= 1:
            for file in write_data:
                self.WriteFile(file)
        else:
            with Pool(Config.Threads) as pool:
                pool.map(self.WriteFile, write_data)

        if not database.IsSuperUser:
            self.NonSuperUserUndo()
