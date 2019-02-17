# 一、首先安装必要的库
```
  pip install -r requirements.txt
```
# 二、补充必要的参数
  在`crwalIp\crwalIp\setting.py`中依次完善关于数据库的参数:  
```
MARIADB_HOST = "IP" -> IP地址,端口为默认值
MARIADB_DBNAME = "dbname" -> 数据库名称
MARIADB_USER = "username" -> 用户名
MARIADB_PASSWORD = "password" -> 密码
```
# 三、运行程序
`crwalIp\main.py` 是程序的启动入口,运行操作如下：
```
python main.py
```

## 特别说明，采集的网站为如下四个:
```
http://www.89ip.com
http://ip.jiangxianli.com
https://www.kuaidaili.com
http://www.xsdaili.com/
```
## 采集内容未区分是否支持HTTP/HTTPS，也未区分高匿和透明
