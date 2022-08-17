#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import settings

origin_json_url = './dist/origin_data.json'
echart_json_url = './dist/echart_data.json'


def covertToEchart():
    originData = readJson(origin_json_url)
    jsonData = prepareOriginData(originData)
    nodes, links, categories = [], [], []
    x, y = 0, 0
    counts = 0
    for i in jsonData:
        tempJData = jsonData[i]
        reduceCount = settings.ShowEchart['padding']
        modCount = mod(counts, settings.ShowEchart['line_count'])
        if modCount == min(0, settings.ShowEchart['line_count'] - 1):
            y = 0
            x = x + reduceCount
        else:
            y = y - reduceCount
        symbolSize = settings.ShowEchart['symbol_size'] * tempJData["count"]
        if symbolSize > settings.ShowEchart['max_symbol_size']:
            symbolSize = settings.ShowEchart['max_symbol_size']
        nodes.append({
            "id": tempJData["table"],
            "name": tempJData["table"],
            "symbol": "circle",
            "symbolSize": symbolSize,
            "x": x,
            "y": y,
            "value": tempJData["table"],
            "category": tempJData["table"],
        })

        for link in tempJData['relation']:
            links.append({
                "source": tempJData["table"],
                "target": tempJData['relation'][link],
            })

        categories.append({
            "name": tempJData["table"]
        })
        counts = counts + 1

    res = {}
    res["nodes"] = nodes
    res["links"] = links
    res["categories"] = categories
    res["show_all"] = settings.ShowEchart['show_all']
    writeJson(res, echart_json_url, True)


def prepareOriginData(data):
    tempMap = {}
    for i in data:
        tempJData = data[i]
        for j in tempJData['relation']:
            tempj = tempJData['relation'][j]
            if tempMap.get(tempj) is None:
                tempMap[tempj] = 1
            tempMap[tempj] = tempMap[tempj] + 1
    for i in data:
        if tempMap.get(i) is None:
            data[i]['count'] = 1
            continue
        data[i]['count'] = tempMap[data[i]['table']]

    return data


def mod(a, b):
    c = a // b
    r = a - c * b
    return r


def writeJson(data, filename, format=False):
    with open(filename, 'w') as file_obj:
        if format:
            json.dump(data, file_obj, indent=4)
        else:
            json.dump(data, file_obj)


def readJson(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        try:
            while True:
                line = f.readline()
                if line:
                    r = json.loads(line)
                    return r
                else:
                    break
        except:
            f.close()
