# coding=utf-8
import time
import os
import urllib
import urllib2
from StringIO import StringIO
import gzip
import re
import json 
from lxml import etree 
import jieba

def getText(elem):
    rc = []
    for node in elem.itertext():
        rc.append(node.strip())
    return ''.join(rc)


#url="https://www.liepin.com/zhaopin/;jsessionid=C9EBE05DDDBDEF867F4A2C8B450CBDF3?imscid=R000000035&key=Java&dqs=020"

url_head="www.zhipin.com"

url="https://www.zhipin.com/job_detail/1415596224.html?ka=search_list_2"

req=urllib2.Request(url,None)
res=urllib2.urlopen(req)
data=res.read()
print '\n'
res.close()
print data 
print "++++++++++++++++++++++++++++++++++++++++"
html = etree.HTML(data.decode('utf-8'))
#html = etree.parse(data)

#res = html.xpath('//a[@data-promid]')
res = html.xpath("//div[@class='text']")
i=0
for each in res:
    i = i + 1
    print i
    txt = getText(each)
    divide = jieba.cut(txt ,cut_all=False)
    for word in divide:
        print word
#    print "default mode:","/".join(divide)
#    print '\n'
