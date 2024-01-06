#!/usr/bin/python
# -*- coding: utf-8 -*-

class Config():
    Indent = " " * 2
    NL = chr(10)
    FunctionParamSign = ":="
    SequenceGrantsInTable = False
    UserMappingsHide = False

    @staticmethod
    def Parse(json):
        Config.Indent = " " * (json.get("indent") or 2)
        Config.NL = json.get("new_line") or chr(10)
        Config.FunctionParamSign = json.get("fnc_param_sign") or ":="

        style = json.get("style") or []
        Config.SequenceGrantsInTable = "seq_grants_in_table" in style
        Config.UserMappingsHide = "hide_user_mappings" in style
