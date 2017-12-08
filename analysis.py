#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
   
#连接    
db=MySQLdb.connect(host="localhost",user="root",passwd="OStem@00",db="boss_zhipin",charset="utf8")  
cursor = db.cursor()    

#写入    
sql="select keyword, count(*) from c2 group by keyword order by count(*) desc limit 500;"
print sql

# 打开一个文件
fp = open("stat.txt", "w")

# SQL 查询语句
try:
    cursor.execute(sql)
    db.commit()
    results = cursor.fetchall()
    print len(results)
    
    for row in results:
        keyword = row[0]
        cnt = row[1]
        line = "%s,%s\n" % (keyword,cnt)
        print line
        #写文件编码格式不对写不进去，还不报错
        fp.write(line.encode("utf-8")) 
except:
    db.rollback()

fp.close()

db.close()

