#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
   
#连接    
db=MySQLdb.connect(host="localhost",user="root",passwd="OStem@00",db="boss_zhipin",charset="utf8")  
cursor = db.cursor()    

#写入    
#sql="insert into career(keyword,company,Career,Salary_l,Salary_h,Exp_l,Exp_h) values('数据库','百度','dba',15,20,1,4)"
sql="insert into career(keyword,company,Career,Salary_l,Salary_h,Exp_l,Exp_h,description) values('%s','%s','%s',%d,%d,%d,%d,'%s')" % ('c++','facebook','cpp',1,2,3,4,'hl')
print sql
#sql="""insert into test(id,x) values(1,2)"""

try:
    n = cursor.execute(sql)
    print n
    db.commit()
except:
    db.rollback()

db.close()

