# -*- coding: utf-8 -*-

import datetime
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

url = "http://yuanjian.cnki.net/Search/Result"
header = {}
header['User-Agent'] ='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
header['Cache-Control']='private'
header['Content-Type']='text/html; charset=utf-8'
header['Accept']='text/html, */*; q=0.01'
header['Connection']='keep-alive'
header['Host']='yuanjian.cnki.net'


data = pd.read_csv(r'school.csv',encoding = 'ANSI')
sch = data['school'].tolist()

starttime = datetime.datetime.now()
tot_data=pd.DataFrame()
for m in sch[40:60]:
    da = pd.DataFrame()
    for k in list(range(2008,2018)):
        daa = pd.DataFrame({'论文名字':[],'来源期刊':[],'出版日期':[],'出版类型':[]})
        for n in list(range(1,613)):
            form_data = {'searchType':'MulityTermsSearch','ArticleType':1,
                             'ParamIsNullOrEmpty': 'true','Islegal': 'false',
                             'Order':1,'Page':n,'ShowType':1,'Unit':m,'Year':k}
            print(form_data)
            r = requests.post(url,params=form_data,headers=header)   
            htmlcontent=r.content.decode('utf-8').replace('\n','').replace('\r','')
            r2 = BeautifulSoup(htmlcontent,'lxml')
        
            name = list(re.findall(r'class="left" title="(.*?)"',htmlcontent))
            
            if name[0] in daa['论文名字'].tolist():
                break
            
            source = []
            for i in list(r2.find_all('a',class_='source-i')):
                try:
                    s = re.findall( r'>(.*?)<',str(i))[0]
                except:
                    s = ['None']
                source.append(s)
                           
            year = []
            for i in list(r2.find_all('p',class_='source')):
                try:
                    y = re.findall( r'<span>(.*?)</span>',str(i))[0]
                except:
                    y = ['None']
                year.append(y)
            
            type_ = []
            for i in list(r2.find_all('a',class_='download left')):
                try:
                    t = re.findall( r'dbtype=(.*?)&amp',str(i))[0] 
                except:
                    t = ['None']
                type_.append(t)      
                  
            daa = daa.append(pd.DataFrame({'论文名字':name,'来源期刊':source,'出版日期':year,'出版类型':type_}))
            daa['学校名称']=m
            daa.to_csv(r'lunwen1.csv',encoding = 'utf-8-sig')
           
            if len(name)<20:
                break
        da=da.append(daa)
    tot_data=tot_data.append(da)
    tot_data.to_csv(r'lunwen.csv',encoding = 'utf-8-sig')
endtime = datetime.datetime.now()
print ((endtime - starttime).seconds)



        
    
