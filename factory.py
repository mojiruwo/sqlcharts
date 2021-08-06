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
        self.connection = pgsql.connect(database=settings.DATABASES['default']['NAME'],
                                           user=settings.DATABASES['default']['USER'],
                                           password=settings.DATABASES['default']['PASSWORD'],
                                           host=settings.DATABASES['default']['HOST'],
                                           port=settings.DATABASES['default']['PORT'])

    def getTableOriginData(self):
        tableMap = self.getTableMap()
        tableData = {}
        for i in tableMap:
            tableData[i] = self.getTableCloumns(i)
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

    def getTableCloumns(self, tablename):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull FROM pg_class as c,pg_attribute as a where c.relname = '" + tablename + "' and a.attrelid = c.oid and a.attnum>0")
        cloumns = cursor.fetchall()
        res, relation = {}, {}
        for clo in cloumns:
            title = clo[2]
            des = clo[0]
            rel = matchRelationTable(self.tableMap, tablename, title)
            if rel != "":
                relation[title] = rel
        res['relation'] = relation
        res['table'] = tablename
        # print(res)
        return res


class MysqlFactory:
    def __init__(self):
        self.tableMap = {}
        mysql = importlib.import_module('pymysql')
        ## 连接到一个给定的数据库
        self.connection = mysql.connect(database=settings.DATABASES['default']['NAME'],
                                          user=settings.DATABASES['default']['USER'],
                                          password=settings.DATABASES['default']['PASSWORD'],
                                          host=settings.DATABASES['default']['HOST'],
                                          port=settings.DATABASES['default']['PORT'])

    def getTableOriginData(self):
        tableMap = self.getTableMap()
        tableData = {}
        for i in tableMap:
            tableData[i] = self.getTableCloumns(i)
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

    def getTableCloumns(self, tablename):
        cursor = self.connection.cursor()
        cursor.execute("show full columns from " + tablename)
        cloumns = cursor.fetchall()
        res, relation = {}, {}
        for clo in cloumns:
            title = clo[0]
            des = clo[8]
            rel = matchRelationTable(self.tableMap, tablename, title)
            if rel != "":
                relation[title] = rel
        res['relation'] = relation
        res['table'] = tablename
        return res


def matchRelationTable(tableMap, tablename, name):
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
    if settings.SPECIALRELATIONTABLE.get(tablename):
        if settings.SPECIALRELATIONTABLE[tablename].get(name):
            print('SPECIALRELATIONTABLE:' + settings.SPECIALRELATIONTABLE[tablename][name])
            return settings.SPECIALRELATIONTABLE[tablename][name]
    for i in [newname, newname + 's']:
        i = settings.TABLEPREFIX + i
        if tableMap.get(i):
            return tableMap.get(i)
    # 匹配一些强制关联的字段 例如 create_id => users
    if settings.SPECIALRELATIONCLOUMN.get(name):
        print('SPECIALRELATIONCLOUMN:' + settings.SPECIALRELATIONCLOUMN[name])
        return settings.SPECIALRELATIONCLOUMN[name]
    print('tableName:' + tablename + ' cloumn:' + name + ' is not found relation')
    return ''
