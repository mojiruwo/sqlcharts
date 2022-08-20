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
        x, y = 0, 0
        for i in jsonData:
            tempJData = jsonData[i]
            # 表字段数据
            erRect = {
                "id": tempJData["table"],
                "shape": "er-rect",
                "label": tempJData["table"],
                "width": 250,
                "height": 24,
                "position": {
                    "x": 24,
                    "y": 250
                }
            }
            ports = []
            for filed in tempJData["columns"]:
                ports.append({
                    "id": tempJData["table"] + "." + filed["title"],
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
            for filed in tempJData["columns"]:
                source = matchRelationTable(tempJData["table"], filed["title"])
                if source != "":
                    splitSource = source.split('.')
                    if len(splitSource) != 2:
                        continue
                    nodes.append({
                        "id": tempJData["table"] + "." + filed["title"] + source,
                        "shape": "edge",
                        "source": {
                            "cell": tempJData["table"],
                            "port": tempJData["table"] + "." + filed["title"]
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
        utils.writeJson(nodes, utils.sql_er_url, True)
        
def initSqlData():
    global jsonData
    jsonData = utils.readJson(utils.sql_json_url)
    
def matchRelationTable(tablename, name):
    if name == 'id':
        return ''
    l = name.split('_')
    newname = ''

    if l[-1] == 'id':
        newl = l[:-1]
        newname = "_".join(newl)
    else:
        return ''
    # 匹配配置文件中自定义的关联
    if settings.mapRelationTable.get(tablename):
        if settings.mapRelationTable[tablename].get(name):
            print('mapRelationTable:' + settings.mapRelationTable[tablename][name])
            return settings.mapRelationTable[tablename][name]
    for i in [newname, newname + 's']:
        i = settings.tablePrefix + i
        if jsonData.get(i):
            return jsonData.get(i)['table'] + '.id'
    # 匹配一些强制关联的字段 例如 create_id => users.id
    if settings.mapRelationColumn.get(name):
        print('mapRelationColumn:' + settings.mapRelationColumn[name])
        return settings.mapRelationColumn[name]
    print('tableName:' + tablename + ' column:' + name + ' is not found relation')
    return ''


