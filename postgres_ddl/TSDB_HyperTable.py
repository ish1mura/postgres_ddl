#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL
from postgres_ddl.TSDB_Dimension import TSDB_Dimension

class TSDB_HyperTable(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.ID = data.get("id") or 0
        assert self.ID > 0, \
            "TimescaleDB hypertable id is null"

        self.TSDB_Schema = (data.get("tsdb_schema") or "timescaledb").strip().lower()
        assert len(self.TSDB_Schema) > 0, \
            "TimescaleDB hypertable relation is null"

        self.Relation = (data.get("relation") or "").strip().lower()
        assert len(self.Relation) > 0, \
            "TimescaleDB hypertable relation is null"

        self.PartsSchema = (data.get("parts_schema") or "").strip().lower()
        assert len(self.PartsSchema) > 0, \
            "TimescaleDB hypertable parts_schema is null"

        self.PartsPrefix = (data.get("parts_prefix") or "").strip().lower()
        assert len(self.PartsPrefix) > 0, \
            "TimescaleDB hypertable parts_prefix is null"

        self.IsCompress = (data.get("is_compress") is True)
        self.CompressAfter = (data.get("compress_after") or "").strip().lower()
        self.DropAfter = (data.get("drop_after") or "").strip().lower()

        self.PartColumn = None
        self.Dimensions = []

        for row in (data.get("dimensions") or []):
            row = TSDB_Dimension(self.GetFullName(), row)
            if row.OrderNum == 1:
                self.PartColumn = row
            else:
                self.Dimensions.append(row)

    def __str__(self):
        return self.GetFullName()

    def GetObjectType(self):
        return "tsdb_hypertable"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.GetFullName()}"

    def GetFullName(self):
        return self.Relation

    def DDL_FncParam(self, name, value, is_quote=False):
        if is_quote is True:
            value = f"'{value}'"
        return f"{Config.Indent}{name} := {value}"

    def DDL_FncParams(self, params=[], is_inline=False):
        result = []
        sep = " " if is_inline is True else Config.NL

        for (name, value, is_quote) in (params or []):
            if is_quote is True:
                value = f"'{value}'"
            result.append(f"{Config.Indent}{name} := {value}")

        return f",{sep}".join(sorted(result))

    def DDL_Create(self):
        r = f"-- TimescaleDB hypertable: {self.Relation}"
        r += Config.NL + Config.NL
        r += f"SELECT {self.TSDB_Schema}.create_hypertable("
        r += Config.NL

        params = [
            self.DDL_FncParam("relation", self.Relation, True),
            self.DDL_FncParam("time_column_name", self.PartColumn.Column, True),
            self.DDL_FncParam("if_not_exists", "TRUE"),
            self.DDL_FncParam("create_default_indexes", "FALSE"),
            self.DDL_FncParam("migrate_data", "FALSE"),
            self.DDL_FncParam("associated_schema_name", self.PartsSchema, True),
            self.DDL_FncParam("associated_table_prefix", self.PartsPrefix, True)
        ]

        if self.PartColumn is not None:
            if len(self.PartColumn.Interval) > 0:
                params.append(self.DDL_FncParam("chunk_time_interval", self.PartColumn.Interval))
            if len(self.PartColumn.FncPart) > 0:
                params.append(self.DDL_FncParam("time_partitioning_func", self.PartColumn.FncPart, True))
            if self.PartColumn.SlicesNum > 0:
                params.append(self.DDL_FncParam("number_partitions", self.PartColumn.SlicesNum))
            if len(self.PartColumn.FncIntNow) > 0:
                params.append(self.DDL_FncParam("partitioning_func", self.PartColumn.FncIntNow, True))

        r += f",{Config.NL}".join(sorted(params))
        r += Config.NL
        r += ");"
        r += Config.NL + Config.NL

        if self.IsCompress:
            r += f"ALTER TABLE {self.Relation} SET(timescaledb.compress);"
            r += Config.NL + Config.NL

        if len(self.CompressAfter) > 0:
            r += f"-- TimescaleDB hypertable compression policy: {self.Relation}"
            r += Config.NL + Config.NL
            r += f"-- SELECT {self.TSDB_Schema}.remove_compression_policy('{self.Relation}');"
            r += Config.NL + Config.NL
            r += f"SELECT {self.TSDB_Schema}.add_compression_policy("
            r += Config.NL
            r += f",{Config.NL}".join(sorted([
                self.DDL_FncParam("hypertable", self.Relation, True),
                self.DDL_FncParam("compress_after", self.CompressAfter),
                self.DDL_FncParam("if_not_exists", "TRUE"),
            ]))
            r += Config.NL
            r += ");"
            r += Config.NL + Config.NL

        if len(self.DropAfter) > 0:
            r += f"-- TimescaleDB hypertable retention policy: {self.Relation}"
            r += Config.NL + Config.NL
            r += f"-- SELECT {self.TSDB_Schema}.remove_retention_policy('{self.Relation}');"
            r += Config.NL + Config.NL
            r += f"SELECT {self.TSDB_Schema}.add_retention_policy("
            r += Config.NL
            r += self.DDL_FncParams([
                ["hypertable", self.Relation, True],
                ["drop_after", self.DropAfter, False],
                ["if_not_exists", "TRUE", False],
            ])
            r += Config.NL
            r += ");"
            r += Config.NL + Config.NL

        return r.strip() + Config.NL

    def Diff(self, another):
        if self.Value != another.Value:
            return [
                self.DDL_Create()
            ]
        else:
            return []
