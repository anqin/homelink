#!/usr/bin/env python
#-*-coding:utf8*-
########################################################################
#
# Copyright (c) for Homelnk authors, Inc. All Rights Reserved
#
########################################################################

'''
Author: anqin.qin@gmail.com
'''

import os
import re
import urllib
import urllib2
import urlparse
import cookielib
import datetime
import glob
import socket
import time
socket.setdefaulttimeout(60)
    
#下载数据存放路径
#base_dir = r'H:\Stock\stock_data\BlockData'
base_dir = r'./testdata'

date_check = True
#date_check = False
date_line = '2016-01-01'


cookiejar = cookielib.LWPCookieJar()
cookies = [
  # ('username', '13070150510'),
  # ('password', 'e50614c4dee9936747e0ab92a25aed6c'),
  # ('usertype', 'mobile'),
  # ('uType', '2'),
  ('lianjia_ssid', '08c50cfa-dc50-43f9-92f8-1839f56db42d'),
  ('lianjia_uuid', '024fd171ab1d7bbead26760210fd9244'),
  ('lianjia_token', '2.000938833773a075941895aa0614095dc7'),
]
for c in cookies:
  ck = cookielib.Cookie(version=0, 
                        name=c[0],
                        value=c[1],
                        port=None, 
                        port_specified=False, 
                        domain='bj.lianjia.com', 
                        domain_specified=False, 
                        domain_initial_dot=False, 
                        path='/', 
                        path_specified=True, 
                        secure=False, 
                        expires=None, 
                        discard=True, 
                        comment=None, 
                        comment_url=None, 
                        rest={'HttpOnly': None}, 
                        rfc2109=False)
  cookiejar.set_cookie(ck)
myopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.18) Gecko/20081029 Firefox/2.0.0.18 (.NET CLR 3.5.30729)'}

date = ''

downloaded = []
commuities = [
    {'code': 'cpbjc', 'name':'昌平佰嘉城', 'id':'1111027375875'},
    {'code': 'cpbjrj', 'name':'昌平天通北京人家', 'id':'1111027375926'},
    {'code': 'cpdysbzx', 'name':'昌平东亚上北中心', 'id':'1111027374040'},
    {'code': 'cplyydeq', 'name':'昌平龙跃苑东二区', 'id':'1111027378207'},
    {'code': 'cpttxyeq', 'name':'昌平天通西苑二区', 'id':'1111027380053'},
    {'code': 'cpttxysq', 'name':'昌平天通西苑三区', 'id':'1111027380054'},
    {'code': 'cpttybeq', 'name':'昌平天通苑北二区', 'id':'1111027380040'},
    {'code': 'cpttybsq', 'name':'昌平天通苑北三区', 'id':'1111027380043'},
    {'code': 'cpttybyq', 'name':'昌平天通苑北一区', 'id':'1111027380047'},
    {'code': 'cpttydeq', 'name':'昌平天通苑东二区', 'id':'1111027380049'},
    {'code': 'cpttydsq', 'name':'昌平天通苑东三区', 'id':'1111027380050'},
    {'code': 'cpttydyq', 'name':'昌平天通苑东一区', 'id':'1111027380051'},
    {'code': 'cpttyzy', 'name':'昌平天通苑中苑', 'id':'1111027380057'},
    {'code': 'cpxlc', 'name':'昌平新龙城', 'id':'1111027380057'},
    {'code': 'cplxhgdq', 'name':'昌平领秀慧谷D区', 'id':'1111063405237'},
    {'code': 'cplxhgcq', 'name':'昌平领秀慧谷C区', 'id':'1111050770108'},
    {'code': 'cyahlyq', 'name':'朝阳安慧里一区', 'id':'1111027375605'},
    {'code': 'cyazkd', 'name':'朝阳澳洲康都', 'id':'1111027375680'},
    {'code': 'cyazxl', 'name':'朝阳安贞西里', 'id':'1111027375686'},
    {'code': 'cybjxs', 'name':'朝阳北京像素', 'id':'1111045342092'},
    {'code': 'cybjxtd', 'name':'朝阳北京新天地', 'id':'1111027375945'},
    {'code': 'cyblayeq', 'name':'朝阳柏林爱乐二期', 'id':'1111027375966'},
    {'code': 'cyblaysq', 'name':'朝阳柏林爱乐三期', 'id':'1111027375967'},
    {'code': 'cybljq', 'name':'朝阳宝利金泉', 'id':'1111027375984'},
    {'code': 'cybyjymly', 'name':'朝阳北苑家园茉藜园', 'id':'1111027376255'},
    {'code': 'cycbdcq', 'name':'朝阳CBD传奇', 'id':'1111027376317'},
    {'code': 'cyfhc', 'name':'朝阳凤凰城', 'id':'1111027374224'},
    {'code': 'cyfhcsq', 'name':'朝阳凤凰城三期', 'id':'1111027374224'},
    {'code': 'cyflcaq', 'name':'朝阳富力城A区', 'id':'1111027374272'},
    {'code': 'cygdhy', 'name':'朝阳国典华园', 'id':'1111027374537'},
    {'code': 'cygfbjeq', 'name':'朝阳国风北京二期', 'id':'1111027374551'},
    {'code': 'cygfbjyq', 'name':'朝阳国风北京一期', 'id':'1111027374552'},
    {'code': 'cygmdyceh', 'name':'朝阳国美第一城2号', 'id':'1111027374656'},
    {'code': 'cygmdycsh', 'name':'朝阳国美第一城3号', 'id':'1111027374654'},
    {'code': 'cygxjy1', 'name':'朝阳光熙家园1', 'id':'1111027374752'},
    {'code': 'cygxjy2', 'name':'朝阳光熙家园2', 'id':'1111027374751'},
    {'code': 'cygxjy3', 'name':'朝阳光熙家园3', 'id':'1111043443524'},
    {'code': 'cygzxl', 'name':'朝阳管庄西里', 'id':'1111027374857'},
    {'code': 'cyhfyc', 'name':'朝阳华纺易城', 'id':'1111027374971'},
    {'code': 'cyhmc', 'name':'朝阳华贸城', 'id':'1111027374971'},
    {'code': 'cyhty', 'name':'朝阳华腾园', 'id':'1111027375333'},
    {'code': 'cyhwbl', 'name':'朝阳华威北里', 'id':'1111027375341'},
    {'code': 'cyhxdc', 'name':'朝阳后现代城', 'id':'1111027375357'},
    {'code': 'cyhzl', 'name':'朝阳慧忠里', 'id':'1111027376953'},
    {'code': 'cyjmtca', 'name':'朝阳嘉铭桐城A', 'id':'1111027377291'},
    {'code': 'cyjmtcb', 'name':'朝阳嘉铭桐城B', 'id':'1111027377292'},
    {'code': 'cyjmtcc', 'name':'朝阳嘉铭桐城C', 'id':'1111027377293'},
    {'code': 'cyjmtcd', 'name':'朝阳嘉铭桐城D', 'id':'1111027377294'},
    {'code': 'cyjmtce', 'name':'朝阳嘉铭桐城E', 'id':'1111027377295'},
    {'code': 'cyjmtcf', 'name':'朝阳嘉铭桐城F', 'id':'1111027377296'},
    {'code': 'cyjty', 'name':'朝阳京通苑', 'id':'1111027377416'},
    {'code': 'cyjxy', 'name':'朝阳金星园', 'id':'1111027377484'},
    {'code': 'cylgjy', 'name':'朝阳鹿港嘉苑', 'id':'1111027377839'},
    {'code': 'cymls', 'name':'朝阳美丽山', 'id':'1111027378350'},
    {'code': 'cyngl', 'name':'朝阳农光里', 'id':'1111027378492'},
    {'code': 'cynhdyeq', 'name':'朝阳南湖东园二区', 'id':'1111027378504'},
    {'code': 'cynhdyyq', 'name':'朝阳南湖东园一区', 'id':'1111027378505'},
    {'code': 'cynpl', 'name':'朝阳南平里', 'id':'1111027378574'},
    {'code': 'cypgp', 'name':'朝阳苹果派', 'id':'1111027378712'},
    {'code': 'cyqhjy', 'name':'朝阳千鹤家园', 'id':'1111027378816'},
    {'code': 'cyqnhjy', 'name':'朝阳青年汇佳园', 'id':'1111027378890'},
    {'code': 'cyqqjy', 'name':'朝阳万科青青家园', 'id':'1111027380334'},
    {'code': 'cyrfss', 'name':'朝阳润枫水尚', 'id':'1111027379004'},
    {'code': 'cysajy', 'name':'朝阳世安家园', 'id':'1111027379082'},
    {'code': 'cyscgj', 'name':'朝阳首城国际', 'id':'1111027379107'},
    {'code': 'cysxy', 'name':'朝阳水星园', 'id':'1111027379622'},
    {'code': 'cysyj', 'name':'朝阳芍药居北里', 'id':'1111027379657'},
    {'code': 'cysyxl', 'name':'朝阳松榆西里', 'id':'1111027379691'},
    {'code': 'cywjhydq', 'name':'朝阳望京花园东区', 'id':'1111027380302'},
    {'code': 'cywjxc', 'name':'朝阳望京新城', 'id':'1111027380317'},
    {'code': 'cywjxysq', 'name':'朝阳望京西园三区', 'id':'1111027380321'},
    {'code': 'cywxstsq', 'name':'朝阳万象新天四区', 'id':'1111027380516'},
    {'code': 'cyxbhdl', 'name':'朝阳西坝河东里', 'id':'1111027380576'},
    {'code': 'cyxcgj', 'name':'朝阳新城国际', 'id':'1111027380611'},
    {'code': 'cyxljy', 'name':'朝阳兴隆家园', 'id':'1111027381021'},
    {'code': 'cyxtjysq', 'name':'朝阳炫特嘉园三期', 'id':'1111027381238'},
    {'code': 'cyyhad', 'name':'朝阳旭辉奥都', 'id':'1111027380785'},
    {'code': 'cyyhslc', 'name':'朝阳沿海赛洛城', 'id':'1111027381719'},
    {'code': 'cyzjdj', 'name':'朝阳珠江帝景', 'id':'1111027382490'},
    {'code': 'cyzjlmjyxq', 'name':'朝阳珠江罗马嘉园西', 'id':'1111027382525'},
    {'code': 'hdbsl', 'name':'海淀宝盛里', 'id':'1111027382525'},
    {'code': 'hdbsyt', 'name':'海淀碧水云天', 'id':'1111027376101'},
    {'code': 'hdbyxq', 'name':'海淀北影小区', 'id':'1111027376278'},
    {'code': 'hdchy', 'name':'海淀城华园', 'id':'1111027376447'},
    {'code': 'hdddcsjy', 'name':'海淀当代城市家园', 'id':'1111027376795'},
    {'code': 'hddhzy', 'name':'海淀大河庄苑', 'id':'1111027373705'},
    {'code': 'hddxy', 'name':'海淀稻香园', 'id':'1111027373995'},
    {'code': 'hdfnsq', 'name':'海淀蜂鸟社区', 'id':'1111027374308'},
    {'code': 'hdgdhy', 'name':'海淀光大花园', 'id':'1111027374538'},
    {'code': 'hdgjkxq', 'name':'海淀甘家口小区', 'id':'1111027374608'},
    {'code': 'hdhqjy', 'name':'海淀华清嘉园', 'id':'1111027375225'},
    {'code': 'hdhzxq', 'name':'海淀黄庄小区', 'id':'1111027376959'},
    {'code': 'hdjrjy', 'name':'海淀今日家园', 'id':'1111027377326'},
    {'code': 'hdjsbdy', 'name':'海淀建设部大院', 'id':'1111027377326'},
    {'code': 'hdmky', 'name':'海淀铭科苑', 'id':'1111027378318'},
    {'code': 'hdqsy', 'name':'海淀清上园', 'id':'1111027378913'},
    {'code': 'hdsddl', 'name':'海淀上地东里', 'id':'1111046342806'},
    {'code': 'hdddcsjy', 'name':'海淀当代城市家园', 'id':'1111027376795'},
    {'code': 'hdymjy', 'name':'海淀怡美家园', 'id':'1111027381904'},
    {'code': 'hdslx', 'name':'海淀上林溪', 'id':'1111027379460'},
    {'code': 'hdsysbl', 'name':'海淀双榆树北里', 'id':'1111027379678'},
    {'code': 'hdsysdl', 'name':'海淀双榆树东里', 'id':'1111027379682'},
    {'code': 'hdtyxq', 'name':'海淀塔院小区', 'id':'1111027380129'},
    {'code': 'hdtyy', 'name':'海淀太月园', 'id':'1111027380127'},
    {'code': 'hdtyy2', 'name':'海淀太阳园', 'id':'1111027380126'},
    {'code': 'hdwqxxjy', 'name':'海淀万泉新新', 'id':'1111027380422'},
    {'code': 'hdxky', 'name':'海淀新康园', 'id':'1111027380996'},
    {'code': 'hdxnzsq', 'name':'海淀小南庄社区', 'id':'1111027381078'},
    {'code': 'hdxsw', 'name':'海淀橡树湾', 'id':'1111027380722'},
    {'code': 'hdydy', 'name':'海淀远大园', 'id':'1111027381601'},
    {'code': 'hdytdl', 'name':'海淀永泰东里', 'id':'1111027382073'},
    {'code': 'hdyxhy', 'name':'海淀育新花园', 'id':'1111027382146'},
    {'code': 'hdzcl', 'name':'海淀知春里', 'id':'1111027382321'},
    {'code': 'hdzcy', 'name':'海淀展春园', 'id':'1111027382338'},
    {'code': 'hdzxy', 'name':'海淀智学苑', 'id':'1111027382721'},
    {'code': 'sjsbjbl', 'name':'石景山八角北路', 'id':'1111027375872'},
    {'code': 'sjsyyss', 'name':'石景山远洋山水', 'id':'1111027382209'},
    {'code': 'tzccgj', 'name':'通州长城国际', 'id':'1111027376334'},
    {'code': 'tzjyzyz', 'name':'通州金隅自由筑', 'id':'1111046557572'},
    {'code': 'tzxhljy', 'name':'通州新华联锦园', 'id':'1111027380845'},
    {'code': 'tzxmzy', 'name':'通州西马庄园', 'id':'1111027381072'},
    {'code': 'tzzjyj', 'name':'通州珠江逸景', 'id':'1111027382552'},
    {'code': 'xcmdnc', 'name':'西城马甸南村', 'id':'1111027378248'},
    {'code': 'xcrf', 'name':'西城荣丰2008', 'id':'1111027378998'},
    {'code': 'xcxwmxdj', 'name':'西城宣武门西大街', 'id':'1111027381293'},
]

def form_code_name(community):
  return 'CJ%s' % community['code']

def form_file_name(community):
  return 'CJ%s.txt' % community['code']

def form_url(community, page_no):
    url_pattern_page_1 = "http://bj.lianjia.com/chengjiao/C%s"
    url_pattern_page_2 = "http://bj.lianjia.com/chengjiao/pg%dc%s"
    if page_no == 0:
        return url_pattern_page_1% (community['id'])
    else :
        return url_pattern_page_2 % (page_no, community['id'])

def dzh2():
    os.chdir(base_dir)
    get_prices(commuities)
    generate_code_list(commuities)

def get_prices(commuities):
  for community in commuities:
    get_community_price(community)

def generate_code_list(commuities):
  f = open('community.fnt', 'w')
  print >> f, "FT Name Table"
  print >> f, "CJ"
  for community in commuities:
    print >> f, "%s\t%s" % (community['code'], community['name'].decode('utf8').encode('gbk'))
  f.close()

def get_content(url):
    req = urllib2.Request(url, headers=headers)
    response = myopener.open(req).read()
    return response

def get_test_content(url):
    return open(r'/Users/anqin/Documents/Workspace/homesink/px_datasource/testdata/test.htm', 'r').read()

def get_community_price(community):
    f = open(form_file_name(community), 'w')
    page_no = 1
    date_ok = False
    while True:
      url = form_url(community, page_no)
      #print "Processing community: " + community['name'].decode('utf-8').encode('gbk') + ", page:" + str(page_no)
      print "Processing community: " + community['name'].decode('utf-8') + ", page:" + str(page_no)
      content = get_content(url)
	  # content = get_test_content(url)
      item_pattern = re.compile(r'<div class="dealDate">([\d\.]*?)</div>.*?<div class="unitPrice"><span class="number">(\d+)', re.DOTALL)
      items = item_pattern.findall(content)
      for item in items:
        date, price = item
        if price < 20000:
          continue
        date = date.replace('.', '-')
        print >> f, "%s %s %s %s %s %s" % (date, price, price, price, price, 1)
        if date_check and date < date_line:
          print 'Got date ok', item[0]
          date_ok = True

      final_page_pattern = re.compile('"totalPage":%d' % page_no)
      if not final_page_pattern.findall(content):
        page_no+=1
        time.sleep(5)
        if date_ok:
          break
      else:
        print "Final page"
        break

def date_transform(old_date):
  d = datetime.datetime.strptime(old_date, '%Y-%m-%d')
  if (d.weekday() >= 5):
    d = d - datetime.timedelta(2)
  return d.strftime('%Y-%m-%d')
    


def remove_old_file(date):
    files = glob.glob('*.rar')
    for file in files:
        if date not in file:
            os.remove(file)

if __name__=='__main__':
    dzh2()
    input("Please close this")
