#!/usr/bin/python
# -*- coding: utf-8 -*-
import settings
import importlib


class SqlFactory():
    def getFactory(self, sqlmode='mysql'):
        if sqlmode == 'mysql':
            return MysqlFactory()
        else:
            return PgFactory()


class PgFactory:
    def __init__(self):
        self.tableMap = {}
        pgsql = importlib.import_module('psycopg2')
        ## 连接到一个给定的数据库
        self.connection = pgsql.connect(database=settings.databases['default']['name'],
                                           user=settings.databases['default']['user'],
                                           password=settings.databases['default']['pwd'],
                                           host=settings.databases['default']['host'],
                                           port=settings.databases['default']['port'])

    def getTableOriginData(self):
        tableMap = self.getTableMap()
        tableData = {}
        for i in tableMap:
            tableData[i] = self.getTableColumns(i)
        return tableData

    def getTableMap(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "select relname as tabname,cast(obj_description(relfilenode,'pg_class') as varchar) as comment from pg_class c where relkind = 'r' and relname not like 'pg_%' and relname not like 'sql_%'")
        tables = cursor.fetchall()
        res = {}
        for table in tables:
            if table[0].find('mv_order') >= 0:
                continue

            res[table[0]] = table[0]
        self.tableMap = res
        return res

    def getTableColumns(self, tablename):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull FROM pg_class as c,pg_attribute as a where c.relname = '" + tablename + "' and a.attrelid = c.oid and a.attnum>0")
        columns = cursor.fetchall()
        res, relation = {}, {}
        for col in columns:
            title = col[2]
            desc = col[0]
            relation.append({
                "title": title,
                "tp": "",
                "desc": desc,
            })
        res['columns'] = relation
        res['table'] = tablename
        return res


class MysqlFactory:
    def __init__(self):
        self.tableMap = {}
        mysql = importlib.import_module('pymysql')
        ## 连接到一个给定的数据库
        self.connection = mysql.connect(database=settings.databases['default']['name'],
                                          user=settings.databases['default']['user'],
                                          password=settings.databases['default']['pwd'],
                                          host=settings.databases['default']['host'],
                                          port=settings.databases['default']['port'])

    def getTableOriginData(self):
        tableMap = self.getTableMap()
        tableData = {}
        for i in tableMap:
            tableData[i] = self.getTableColumns(i)
        return tableData

    def getTableMap(self):
        cursor = self.connection.cursor()
        cursor.execute("show tables;")
        tables = cursor.fetchall()
        res = {}
        for table in tables:
            res[table[0]] = table[0]
        self.tableMap = res
        return res

    def getTableColumns(self, tablename):
        cursor = self.connection.cursor()
        cursor.execute("show full columns from " + tablename)
        columns = cursor.fetchall()
        res, relation = {}, []
        for col in columns:
            title = col[0]
            tp = col[1]
            desc = col[8]
            relation.append({
                "title": title,
                "tp": tp,
                "desc": desc,
            })
        res['columns'] = relation
        res['table'] = tablename
        return res
