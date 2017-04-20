#!/usr/bin/env python
#coding: utf-8


import re
import requests
import socket
import sys


if len(sys.argv) == 2:
    keyword = sys.argv[1]
    r = requests.get('https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word='+str(keyword)+'Dpn=20&gsm=3c')
    html = r.text
else:
    sys.exit(1)

reload(sys)
sys.setdefaultencoding('utf-8')


match = re.findall('"objURL":"(.*?)"', html)

print '一共发现图片: %d'  % len(match)
id = 0
success = 0
faild = 0

for i in match:
    try:
        ibin = requests.get(i)
    except (requests.exceptions.ConnectionError,socket.error) as e:
        print "下载[%s]失败, %s" % (i, e)
        faild += 1
    else:
        fd = open('/tmp/spider/'+str(id)+'.jpg', 'wb+')
        fd.write(ibin.text)
        print "下载[%s]成功" % i
        success += 1
    finally:
        id += 1
        fd.close()

print "------------------done------------------"
print "下载成功: %d\n下载失败: %d" %(success, faild)
