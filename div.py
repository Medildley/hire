# coding=utf-8
import time
import string
import os
import urllib
import urllib2
from StringIO import StringIO
import gzip
import re
import json 
from lxml import etree 
import jieba
import MySQLdb
import requests
import random
   

def mysql_add(url_real, table):
    req=urllib2.Request(url_real,None)
    res=urllib2.urlopen(req)
    data=res.read()
    print '\n'
    res.close()
    print "++++++++++++++++++++++++++++++++++++++++"
    html = etree.HTML(data.decode('utf-8'))

    #get career
    res = html.xpath("//div[@class='info-primary']/div[@class='name']")
    if(len(res)>0):
        career=getText(res[0])
    else:
        career="null"
    print "career:"+career
    
    #get publish time
    res = html.xpath("//div[@class='info-primary']/div[@class='job-author']/span")
    if(len(res)>0):
        pub_time=getText(res[0])
    else:
        pub_time="0"
    ts=filter(str.isdigit, pub_time.encode('utf-8'))
    print "publish time:"+ts

    #get salary
    res = html.xpath("//div[@class='info-primary']/div[@class='name']/span")
    if(len(res)>0):
        salary=res[0]
        print "salary:"+getText(salary)
        salary_array=getText(salary).split('-')
        if(len(salary_array) > 1):
            s_l=filter(str.isdigit, salary_array[0])
            s_l_n=string.atoi(s_l)
            s_h=filter(str.isdigit, salary_array[1])
            s_h_n=string.atoi(s_h)
            print s_l_n
            print s_h_n
        else:
            s_l_n=0
            s_h_n=0

    #get experience
    res = html.xpath("//div[@class='info-primary']/p")
    if(len(res)>0):
        exp=res[0]
        #exp_a=getText(exp).split('-')
        exp_a=getText(exp).split('-')
        if(len(exp_a) > 1):
            e_l=filter(str.isdigit, exp_a[0].encode("utf-8"))
            e_l_n=string.atoi(e_l)
            e_h=filter(str.isdigit, exp_a[1].encode("utf-8"))
            e_h_n=string.atoi(e_h)
            print e_l_n
            print e_h_n
        else:
            e_l_n=0
            e_h_n=0

    #get company
    res = html.xpath("//div[@class='info-company']//a/@title")
    if(len(res)>0):
        comp=res[0]
    else:
        comp="null"
    print "comp:"+comp

    #get description
    res = html.xpath("//div[@class='info-company']//p")
    if(len(res)>0):
        desc=getText(res[0])
    else:
        desc='null'
    print "desc:"+desc

    #get full description
    res = html.xpath("//div[@class='text']")
    i=0
    for each in res:
        i = i + 1
        print i
        txt = getText(each)
        divide = jieba.cut(txt ,cut_all=False)
        #divide = jieba.cut_for_search(txt)
        for word in divide:
            if(len(word)>1):
                #print word
                sql="insert into %s(keyword,company,Career,Salary_l,Salary_h,Exp_l,Exp_h,description,publish_time) values('%s','%s','%s',%d,%d,%d,%d,'%s','%s')" % (table,word,comp,career,s_l_n,s_h_n,e_l_n,e_h_n,desc,ts)
                #print sql
                try:
                    n = cursor.execute(sql)
                    #print n
                    db.commit()
                except:
                    db.rollback()
    return

def getText(elem):
    rc = []
    for node in elem.itertext():
        rc.append(node.strip())
    return ''.join(rc)



###### begin main #######


#连接    
db=MySQLdb.connect(host="localhost",user="root",passwd="OStem@00",db="boss_zhipin",charset="utf8")  
cursor = db.cursor()    

url_head="https://www.zhipin.com"

for i in range(15,16):
    url="https://www.zhipin.com/c101020100-p100101/?page=%d&ka=page-%d" % (i,i)
    print url
    
    proxy_on=0
    if(i%5>=4):
        proxy_on=(proxy_on+1)%2
    print "proxy on:%d" % (proxy_on)
    table='java'
    if(proxy_on==1):
        #set proxy
        proxy_list=['217.182.76.151:54566','191.22.216.122:8080','209.9.104.10:80']
        proxy={"https":"41.203.183.50:8080"}
        #proxy_s=urllib2.ProxyHandler({"https":random.choice(proxy_list)})
        proxy_s=urllib2.ProxyHandler(proxy)
        opener=urllib2.build_opener(proxy_s)
        urllib2.install_opener(opener)

    req=urllib2.Request(url,None)
    res=urllib2.urlopen(req)
    data=res.read()
    print '\n'
    res.close()
    html = etree.HTML(data.decode('utf-8'))

    res = html.xpath('//a[@data-jobid]/@href')
    i=0
    for each in res:
        print i
        i=i+1
        url_real=url_head+each
        print url_real
        mysql_add(url_real,table)
        time.sleep(0.1)
    time.sleep(1)

db.close()




