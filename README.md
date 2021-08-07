# sqlcharts 自动生成数据库关联关系图

- 复制settings.py.example 重命名为settings.py
- 将数据库配置信息填入settings.DATABASE，目前支持mysql和postgresql
- 执行 python build.py -b，-b是读取数据库表结构，如果只更新匹配规则，可以去掉-b
- 当前目录执行 python -m http.server --cgi 8000
- 本地访问 127.0.0.1:8000/dist 可看到效果

### 示例图
#### 首次进入
![](images/img1.png)
#### 选中左边栏
![](images/img2.png)
#### 选中图标
![](images/img3.png)

