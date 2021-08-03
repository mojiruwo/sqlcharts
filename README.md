# sqlcharts 自动生成数据库关联关系图

- 复制settings.py.example 重命名为settings.py
- 将数据库配置信息填入settings.DATABASE
- 执行 python build.py -b
- 当前目录执行 python -m http.server --cgi 8000
- 本地访问 127.0.0.1:8000/dist 可看到效果

