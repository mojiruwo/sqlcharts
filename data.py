#!/usr/bin/python
# -*- coding: utf-8 -*-
import settings
import utils

class DataFactory():
    def getFactory(self, mode='er'):
        if mode == 'er':
            return DataErFactory()

class DataErFactory:
    def __init__(self):
        self.jsonData = {}
    
    def covertToChart(self):
        initSqlData()
        nodes = []
        for i in jsonData:
            tableInfo = jsonData[i]
            # 表字段数据
            erRect = {
                "id": tableInfo["table"],
                "shape": "er-rect",
                "label": tableInfo["table"],
                "width": 250,
                "height": 24,
                "position": {
                    "x": 24,
                    "y": 250
                }
            }
            ports = []
            for filed in tableInfo["columns"]:
                ports.append({
                    "id": tableInfo["table"] + "." + filed["title"],
                    "group": "list",
                    "attrs": {
                        "portNameLabel": {
                        "text": filed["title"]
                        },
                        "portTypeLabel": {
                        "text": filed["desc"]
                        }
                    }
                })
            erRect["ports"] = ports
            nodes.append(erRect)
            # 关联关系
            for filed in tableInfo["columns"]:
                source = matchRelationTable(tableInfo["table"], filed["title"])
                if source != "":
                    splitSource = source.split('.')
                    if len(splitSource) != 2:
                        continue
                    nodes.append({
                        "id": tableInfo["table"] + "." + filed["title"] + source,
                        "shape": "edge",
                        "source": {
                            "cell": tableInfo["table"],
                            "port": tableInfo["table"] + "." + filed["title"]
                        },
                        "target": {
                            "cell": splitSource[0],
                            "port": source
                        },
                        "attrs": {
                            "line": {
                            "stroke": "#A2B1C3",
                            "strokeWidth": 2
                            }
                        },
                        "zIndex": 0
                    })
        res = {}
        res["nodes"] = nodes
        res["config"] = settings.chartConfig
        utils.writeJson(res, utils.sql_er_url, True)
        
def initSqlData():
    global jsonData
    jsonData = utils.readJson(utils.sql_json_url)
    if settings.enableFilter:
        filterData = {}
        for i in settings.allowTable:
            filterData[getTableName(i)] = jsonData.get(getTableName(i))
        jsonData = filterData
    
    if len(settings.ignoreTable) > 0:
        tmp = {}
        for i in jsonData:
            if i not in handleIgnoreTable():
                tmp[i] = jsonData.get(i)
        jsonData = tmp
    
    
def matchRelationTable(tableName, fieldName):
    if fieldName == 'id':
        return ''
    # todo 使用middleware模式进行匹配 

    # 匹配配置文件中自定义的关联
    tableRes = relationTable(tableName, fieldName)
    if tableRes != "":
        return tableRes
    
    # 匹配一些强制关联的字段 例如 create_id => users.id
    columnRes = relationColumn(tableName, fieldName)
    if columnRes != "":
        return columnRes

    # 匹配默认公共规则（_id）
    commonRes = relationCommon(tableName, fieldName)
    if commonRes != "":
        return commonRes

    l = fieldName.split('_')
    if l[-1] == 'id':
        print('notFoundRelation: ' + tableName + '.' + fieldName)
    
    return ''

def relationTable(tableName, fieldName):
    tmp = {}
    for i in settings.mapRelationTable:
        tmp[getTableName(i)] = settings.mapRelationTable[i]
    
    if tmp.get(tableName) == None:
        return ''
    
    if tmp[tableName].get(fieldName):
        print('mapRelationTable: ' + tableName + '.' + fieldName + ' => ' + tmp[tableName][fieldName])
        return getTableName(tmp[tableName][fieldName])
    
    return ''

def relationColumn(tableName, fieldName):
    if settings.mapRelationColumn.get(fieldName):
        print('mapRelationColumn: ' + tableName + '.' + fieldName + ' => ' +  settings.mapRelationColumn[fieldName])
        return getTableName(settings.mapRelationColumn[fieldName])
    
    return ''

def relationCommon(tableName, fieldName):
    tName = ''
    l = fieldName.split('_')
    if l[-1] == 'id':
        x = l[:-1]
        tName = "_".join(x)
    else:
        return ''
    for i in tableNameArr(tName):
        if jsonData.get(i):
            return i + '.id'
    return ''

def tableNameArr(table):
    t = getTableName(table)
    return [t, t + 's']

def handleIgnoreTable():
    tmp = []
    for i in settings.ignoreTable:
        tmp.append(getTableName(i))
    return tmp

def getTableName(table):
    return settings.tablePrefix+table