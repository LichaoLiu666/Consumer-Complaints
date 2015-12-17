import numpy as np
import pandas as pd
from selenium import webdriver

from pdfminer import *
from cStringIO import StringIO
import re
import csv

import bs4 #this is beautiful soup
import pandas as pd
import urllib2
"""
This module is used to retrieve broker's detailed information from brokercheck.finra.org
"""

#---------------------------------------------------------------------------------
##stationary extraction
data=urllib2.urlopen(url).read()
d_soup=bs4.BeautifulSoup(data)

#background summary 
x=d_soup.find('div','summarybizcardsectionNoborder')
xx=x.text.lstrip().rstrip()

briefs=[th.get_text().lstrip().rstrip() for th in d_soup.findAll('div',{'class':'summarybizcardsection'})]
briefs+=[i.strip() for i in briefs.pop(2).split('\n\r\n')]

summary={}
summary['title']=xx.replace('\n\r\n        ',';')
summary['num_disclosure']=int(re.match(r'\d+',briefs[0]).group())
summary['year_experience']=int(re.match(r'\d+',briefs[1]).group())
summary['num_exams']=[int(s) for s in briefs[2].split() if s.isdigit()][0]

#current registration
current={}
current['current registration starts']=d_soup.find('div',{'class':'currregfirstcolumn'}).text.lstrip().rstrip()[-7:]
tem=[i.lstrip() for i in d_soup.find('div',{'class':'currregsecondcolumn'}).text.replace('\r','').split('\n') if i.strip() !='']
current['current firm name']=tem[0][:-13]
current['current firm CRD']=tem[0][-6:-1]

for ind in range(1,1+len(tem)-1):
    current['current address '+str(ind)]=tem[ind]
    
#previous registration
previous={}
previous_date=[pre.get_text().lstrip().rstrip().split('-\r\n') for pre in d_soup.findAll('div',{'class':'prevregfirstcolumn'})]
for ind in range(len(previous_date)):
    previous['previous firm '+str(ind+1)+' starts']=previous_date[ind][0]
    previous['previous firm '+str(ind+1)+' ends']=previous_date[ind][1]
previous_company=[pre.get_text().lstrip().rstrip().split('\r\n') for pre in d_soup.findAll('div',{'class':'prevregsecondcolumn'})]
for ind in range(len(previous_company)):
    previous['previous firm '+str(ind+1) + ' name ']=previous_company[ind][0]
    previous['previous firm '+str(ind+1) + ' CRD ']=previous_company[ind][2][-6:-1]
    previous['previous firm '+str(ind+1) + ' location ']=previous_company[ind][4].lstrip()[2:]
#---------------------------------------------------------------------------------
##merge dictionary
data=dict(summary)
data.update(current)
data.update(previous)


#---------------------------------------------------------------------------------------------
#set up scrape and javascript 
url='http://brokercheck.finra.org/Individual/Summary/3122170' #url

driver = webdriver.Firefox() #open firefox
driver.get(url)

driver.find_element_by_id("ctl00_phContent_TermsAndCondUC_BtnAccept").click() #click on accept
driver.find_element_by_id("plus").click() #click on expand


# get the disclosure details and save in dictionary
table={}
disclosure_date=[]
disclosure_type=[]
for i in driver.find_elements_by_xpath('//div[@class="discfirstcolumn TextBold"]'):
    disclosure_date.append(i.text)
for i in driver.find_elements_by_xpath('//div[@class="discsecondcolumn TextBold"]'):
    disclosure_type.append(i.text)
        
    
for i in zip(driver.find_elements_by_xpath('//div[@class="disclosureInnerTable"]'),\
               driver.find_elements_by_xpath('//div[@class="disclosureValue"]')):
   table[i[0].text]=i[1].text

driver.close()

print table
