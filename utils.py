import json

origin_json_url = './dist/origin_data.json'
echart_json_url = './dist/echart_data.json'


def covertToEchart():
    originData = readJson(origin_json_url)
    jsonData = prepareOriginData(originData)
    # print(jsonData)
    nodes, links, categories = [], [], []
    x, y = 0, 0
    counts = 0
    for i in jsonData:
        tempJData = jsonData[i]
        reduceCount = 5
        modCount = mod(counts, 13)
        if modCount == 12:
            y = 0
            x = x + reduceCount
        else:
            y = y - reduceCount
        symbolSize = 5 * tempJData["count"]
        if symbolSize > 100:
            symbolSize = 100
        nodes.append({
            "id": tempJData["table"],
            "name": tempJData["table"],
            "symbol": "pin",
            "symbolSize": symbolSize,
            "x": x,
            "y": y,
            "value": tempJData["table"],
            "category": tempJData["table"],
        })

        for link in tempJData['relation']:
            # print(link)
            links.append({
                "source": tempJData["table"],
                "target": tempJData['relation'][link],
            })

        categories.append({
            "name": tempJData["table"]
        })
        counts = counts + 1
        # print(jsonData[i])

    res = {}
    res["nodes"] = nodes
    res["links"] = links
    res["categories"] = categories
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
    # print(tempMap)
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
                # print(line)
                if line:
                    r = json.loads(line)
                    # print(r)
                    return r
                else:
                    break
        except:
            f.close()
