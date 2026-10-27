#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging
from shutil import rmtree

from postgres_ddl.Config import Config
from postgres_ddl.Database import Database

class Diff():
    def __init__(self, path_config, path_result, connect_source, connect_target):
        Config.Parse(path_config)

        self.ConnectSource = connect_source.strip().lower()
        assert len(self.ConnectSource) > 0, \
            "No source connect name"

        self.ConnectTarget = connect_target.strip().lower()
        assert len(self.ConnectTarget) > 0, \
            "No target connect name"

        self.WorkPath = (path_result or "").strip()
        assert len(self.WorkPath) > 0, \
            "No work path"

        self.PathSource = os.path.join(self.WorkPath, "_source")
        self.PathTarget = os.path.join(self.WorkPath, "_target")
        self.PathDiff   = os.path.join(self.WorkPath, "_diff")

    def GetPath(self, db, root, object):
        # Get file name and path
        file_name = (object.GetFileName() or "").strip()
        file_name = file_name.replace('"', "")
        path = object.GetPath() or []

        # File name not found - get from parent object
        if len(file_name) <= 0:
            parent = db.Objects.get(object.Parent)
            file_name = (parent.GetFileName() or "").strip()
            path = parent.GetPath() or []

        assert len(file_name) > 0, \
            "Object file name is null"

        assert len(path) > 0, \
            "Object path is null"

        # Create subfolders
        path = os.path.sep.join([root] + path)
        if not os.path.exists(path):
            os.makedirs(path)

        return os.path.join(path, file_name)

    def Run(self):
        logging.info("Diff started")
        logging.info(f"PathSource = {self.PathSource}")
        logging.info(f"PathTarget = {self.PathTarget}")
        logging.info(f"PathDiff = {self.PathDiff}")

        # Recreate root folder
        if os.path.exists(self.WorkPath):
            rmtree(self.WorkPath)
        os.mkdir(self.WorkPath)

        # Subfolders
        os.mkdir(self.PathSource)
        os.mkdir(self.PathTarget)
        os.mkdir(self.PathDiff)

        logging.info("Folders created")

        # Parse and export source database
        source_db = Database(self.ConnectSource)
        source_db.Parse()

        logging.info(f"Source db parsed, {len(source_db.Objects)} objects")

        # Parse and export target database
        target_db = Database(self.ConnectTarget)
        target_db.Parse()

        logging.info(f"Target db parsed, {len(target_db.Objects)} objects")

        # Iterate objects of source database
        for sk, sv in source_db.Objects.items():

            # IN source, NOT IN target
            if sk not in target_db.Objects.keys():

                # Parent isn't in target too
                if len(sv.Parent or "") > 0 and sv.Parent not in target_db.Objects.keys():
                    continue

                logging.debug(f"CREATE {sk} not in target")

                # Write CREATE to source
                with open(self.GetPath(source_db, self.PathSource, sv), "a", encoding="utf-8") as wf:
                    wf.write(sv.DDL_Create())
                    wf.write(Config.NL + Config.NL)

                # Write CREATE to diff
                with open(self.GetPath(source_db, self.PathDiff, sv), "a", encoding="utf-8") as wf:
                    wf.write(sv.DDL_Create())
                    wf.write(Config.NL + Config.NL)

                # Write CREATE to object type file
                with open(os.path.join(self.WorkPath, f"{sv.GetObjectType()}.sql"), "a", encoding="utf-8") as wf:
                    wf.write(sv.DDL_Create())
                    wf.write(Config.NL + Config.NL)

            # IN source, IN target
            else:
                tv = target_db.Objects.get(sk)

                # Calculate diff
                diff = sv.Diff(tv)
                if len(diff or []) <= 0:
                    continue

                logging.debug(f"DIFF {sk} both source and target")

                # Write CREATE to source
                with open(self.GetPath(source_db, self.PathSource, sv), "a", encoding="utf-8") as wf:
                    wf.write(sv.DDL_Create())
                    wf.write(Config.NL + Config.NL)

                # Write CREATE to target
                with open(self.GetPath(target_db, self.PathTarget, tv), "a", encoding="utf-8") as wf:
                    wf.write(tv.DDL_Create())
                    wf.write(Config.NL + Config.NL)

                # Write DROP and CREATE to diff
                with open(self.GetPath(source_db, self.PathDiff, sv), "a", encoding="utf-8") as wf:
                    wf.write((Config.NL + Config.NL).join(diff))
                    wf.write(Config.NL + Config.NL)

                # Write DROP and CREATE to object type file
                with open(os.path.join(self.WorkPath, f"{sv.GetObjectType()}.sql"), "a", encoding="utf-8") as wf:
                    wf.write((Config.NL).join(diff))
                    wf.write(Config.NL + Config.NL)

        # Iterate objects of target database
        for tk, tv in target_db.Objects.items():

            # NOT IN source, IN target
            if tk in source_db.Objects.keys():
                continue

            # Parent object deleted in source DB
            if len(tv.Parent or "") > 0 and tv.Parent not in source_db.Objects.keys():
                continue

            logging.debug(f"DROP {tk} not in source")

            # Write CREATE to target
            with open(self.GetPath(target_db, self.PathTarget, tv), "a", encoding="utf-8") as wf:
                wf.write(tv.DDL_Create())
                wf.write(Config.NL + Config.NL)

            # Write DROP to diff
            with open(self.GetPath(target_db, self.PathDiff, tv), "a", encoding="utf-8") as wf:
                wf.write(tv.DDL_Drop())
                wf.write(Config.NL + Config.NL)

            # Write DROP to object type file
            with open(os.path.join(self.WorkPath, f"{tv.GetObjectType()}.sql"), "a", encoding="utf-8") as wf:
                wf.write(tv.DDL_Drop())
                wf.write(Config.NL + Config.NL)
