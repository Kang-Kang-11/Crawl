# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 15:26:29 2019

@author: guokl
"""

import requests
import request
import pymongo
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import urllib.request
import urllib.parse
url = "http://yuanjian.cnki.net/cjfd/Home/CJfdList"
header = {}
header['User-Agent'] ='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
header['Cache-Control']='private'
header['Content-Type']='text/html; charset=utf-8'
header['Accept']='text/html, */*; q=0.01'
header['Connection']='keep-alive'
header['Host']='yuanjian.cnki.net'




'''
re.findall( r'>(.*?)<',str(list(r2.find_all('div',class_='name'))[0]))[1]
"".join(re.findall( r'>(.*?)<',str(list(r2.find_all('div',class_='year'))[0])))
'''

tot_data = pd.DataFrame()
for j in list(range(1,4)):
    print(j)
    form_data ={'tag':'','code':'','catecode':'','title':'','Name':'',\
            'Issn':'','Cn':'', 'Keyword':'','Unit':'', 'PublicAddress':'', \
           'Selects':'','Order':1,'Page':j,'HYPY':'','ShowType':1} 
    print(form_data)
    r = requests.post(url,params=form_data,headers=header)
    htmlcontent=r.content.decode('utf-8') 
    r2 = BeautifulSoup(htmlcontent,'lxml')
    host = [re.findall( r'>(.*?)<',str(i))[0] for i in list((r2.find_all('div',class_='host')))]
    print(host[0])
    name = [re.findall( r'>(.*?)<',str(i))[1] for i in list(r2.find_all('div',class_='name'))]
    place = [re.findall( r'>(.*?)<',str(i))[0] for i in list(r2.find_all('div',class_='place'))]
    year = ["".join(re.findall( r'>(.*?)<',str(i))) for i in list(r2.find_all('div',class_='year'))]
    type_ = [re.findall( r'>(.*?)<',str(i))[0] for i in list(r2.find_all('div',class_='type'))]
    i = [re.findall( r'>(.*?)<',str(i))[0] for i in list(r2.find_all('div',class_='i'))]
    s = [re.findall( r'>(.*?)<',str(i))[0] for i in list(r2.find_all('div',class_='s'))]
    u = [re.findall( r'>(.*?)<',str(i))[0] for i in list(r2.find_all('div',class_='u'))]
    
    da = pd.DataFrame({'期刊名字':name,'主办方':host,'出版地':place,'周期':type_,\
                         '出版年份':year,'复合影响':i,'综合影响':s,'被引':u})
    tot_data = tot_data.append(da)


