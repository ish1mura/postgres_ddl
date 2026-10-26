#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Config import Config

class DDL(object):
    def __init__(self, parent, data):
        self.Parent = (parent or "").strip().lower()

        assert data is not None, \
            f"{type(self)} data is null"

        assert isinstance(data, dict), \
            f"{type(self)} data type is not dict"

        assert len(data.keys()) > 0, \
            f"{type(self)} data is empty"

    def __str__(self):
        raise NotImplementedError(f"__str__ method is not implemented for class {type(self)}")

    def DDL_Create(self):
        raise NotImplementedError(f"DDL_Create method is not implemented for class {type(self)}")

    def DDL_Drop(self):
        raise NotImplementedError(f"DDL_Drop method is not implemented for class {type(self)}")

    def GetObjectType(self):
        raise NotImplementedError(f"GetObjectType method is not implemented for class {type(self)}")

    def GetObjectTypeComment(self):
        raise NotImplementedError(f"GetObjectTypeComment method is not implemented for class {type(self)}")

    def GetObjectName(self):
        raise NotImplementedError(f"GetObjectName method is not implemented for class {type(self)}")

    def GetFullName(self):
        raise NotImplementedError(f"GetFullName method is not implemented for class {type(self)}")

    def GetTag(self):
        raise NotImplementedError(f"GetTag method is not implemented for class {type(self)}")

    def Export(self):
        raise NotImplementedError(f"Export method is not implemented for class {type(self)}")

    def GetPath(self):
        return []

    def GetFileName(self):
        return None

    def Diff(self, another):
        return []

    def FillFunctionParams(self, params=[], is_inline=False, sign=Config.FunctionsParamSign):
        result = []

        if is_inline is True:
            sep = " "
            indent = ""
        else:
            sep = Config.NL
            indent = Config.Indent

        for (name, value, is_quote) in (params or []):
            if is_quote is True:
                value = f"'{value}'"
            result.append(f"{indent}{name} {sign} {value}")

        return f",{sep}".join(sorted(result))
