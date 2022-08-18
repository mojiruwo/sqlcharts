#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import settings
import json
import utils
from factory import SqlFactory


# Create your views here.
def main():
    runWithCmd()
    covertData()


def buildData():
    fa = SqlFactory()
    tableClass = fa.getFactory(settings.databases['default']['engine'])
    tableData = tableClass.getTableOriginData()
    # 对应关系写入文件
    utils.writeJson(tableData, utils.origin_json_url)


def covertData():
    # 生成echarts对应json文件
    utils.covertToEchart()


def runWithCmd():
    for i in range(1, len(sys.argv)):
        command = sys.argv[i]
        if command == '-b':
            buildData()


main()
