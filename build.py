#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import settings
import json
import utils
from factory import SqlFactory
from data import DataFactory


# Create your views here.
def main():
    runWithCmd()
    covertData()


def buildData():
    fa = SqlFactory()
    tableClass = fa.getFactory(settings.databases['default']['engine'])
    tableData = tableClass.getTableOriginData()
    # 表结构写入文件
    utils.writeJson(tableData, utils.sql_json_url)


def covertData():
    # 生成chart对应json文件
    df = DataFactory()
    er = df.getFactory("er")
    er.covertToChart()


def runWithCmd():
    for i in range(1, len(sys.argv)):
        command = sys.argv[i]
        if command == '-b':
            buildData()


main()
