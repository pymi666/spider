#!python3
# -*- coding: utf-8 -*-

'''
import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "lianjia")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

#SQL = "INSERT INTO xiaoqu (小区,均价,建设时间,出租数,挂牌数,街道,大区) VALUES ('大拇指',11267,'2015',3,53,'蔡甸','蔡甸')"
SQL = "select 小区,街道,大区 from xiaoqu limit 1"
# 使用 execute()  方法执行 SQL 查询
cursor.execute(SQL)

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchall()

print(data)

# 关闭数据库连接
db.close()
'''
index = 2
for i in range(1, index + 1):
    index_url = "https://wh.lianjia.com/chengjiao/" + "pg" + str(i) + "xiaoqu"
    html = 'self.parse_url(self.xiaoqu_url % (xiaoqu))' if i == 1 else 'self.parse_url(index_url)'
    print (i)
    print (html)
