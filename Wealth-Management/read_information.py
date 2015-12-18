def retrieve_broker(crd):
    
    import numpy as np
    import pandas as pd
    from selenium import webdriver
    
    
    import bs4 #this is beautiful soup
    import urllib2
    import re

    #-----------------------------------------------------------------------
    url='http://brokercheck.finra.org/Individual/Summary/'+str(crd) #url
    
    
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
    if d_soup.find('div',{'class':'currregfirstcolumn'}):
        current['current registration starts']=d_soup.find('div',{'class':'currregfirstcolumn'}).text.lstrip().rstrip()[-7:]
        tem=[i.lstrip() for i in d_soup.find('div',{'class':'currregsecondcolumn'}).text.replace('\r','').split('\n') if i.strip() !='']
        current['current firm name']=tem[0][:-13]
        current['current firm CRD']=[int(s) for s in tem[0].replace(')','').split() if s.isdigit()][0]
        current['current address']=tem[1]

    else:
        current['current registration starts']=None 
        current['current firm name']=None
        current['current firm CRD']=None
        current['current address']=None

    #previous registration
    previous={}
        
    tmp=[pre.get_text().replace('\r','').split('\n') for pre in d_soup.findAll('div',{'id':'prevregistrationSection'})]
    x=[i.replace('-','').strip() for i in tmp[0] if i.strip()!='']
    
    for idx in range(1,len(x)/5+1):
        previous['previous firm '+str(idx)+' starts']=x[(idx-1)*5+1]
        previous['previous firm '+str(idx)+' ends']=x[(idx-1)*5+2]
        previous['previous firm '+str(idx) + ' name ']=x[(idx-1)*5+3]
        previous['previous firm '+str(idx) + ' CRD ']=x[(idx-1)*5+4]
        previous['previous firm '+str(idx) + ' location ']=x[(idx-1)*5+5]
        
    
    #---------------------------------------------------------------------------------------------
    #disclosure briefs
    disclosure_date=[i.get_text().lstrip().rstrip() for i in d_soup.findAll('div',{'class':'discfirstcolumn TextBold'})]
    disclosure_type=[i.get_text().lstrip().rstrip() for i in d_soup.findAll('div',{'class':'discsecondcolumn TextBold'})]
        
    #set up scrape and javascript 
    
    driver = webdriver.Firefox() #open firefox
    driver.get(url)
    
    driver.find_element_by_id("ctl00_phContent_TermsAndCondUC_BtnAccept").click() #click on accept
    for i in driver.find_elements_by_id("plus"):    
        i.click() #click on expand
    
    
    # get the disclosure details and save in dictionary
    disclosure={}
    temp=driver.find_element_by_xpath('//table[@id="disclosuretable"]').text.split('\n')
    date_index=[temp.index(i) for i in temp if re.search(r'(\d+/\d+/\d+)',i)]
    
    for i in range(min(10,len(date_index))):
        disclosure['dis_date '+str(i+1)]=temp[date_index[i]]
        disclosure['dis_type '+str(i+1)]=temp[date_index[i]+1]
            
        if i<len(date_index)-1:
            if 'Allegations' in temp[date_index[i]:date_index[i+1]]: 
                disclosure['Allegations '+str(i+1)]=temp[temp[date_index[i]:date_index[i+1]].index('Allegations')+date_index[i]+1]
            else:
                disclosure['Allegations '+str(i+1)]=None
        else:
            if 'Allegations' in temp[date_index[i]:]:
                disclosure['Allegations '+str(i+1)]=temp[temp[date_index[i]:].index('Allegations')+date_index[i]+1]
            else:
                disclosure['Allegations '+str(i+1)]=None
    
    #Damage Amount Requested
        if i<len(date_index)-1:
            if 'Damage Amount Requested' in temp[date_index[i]:date_index[i+1]]: 
                disclosure['Damage Amount Requested '+str(i+1)]=temp[temp[date_index[i]:date_index[i+1]].index('Damage Amount Requested')+date_index[i]+1]
            else:
                disclosure['Damage Amount Requested '+str(i+1)]=None
        else:
            if 'Damage Amount Requested' in temp[date_index[i]:]:
                disclosure['Damage Amount Requested '+str(i+1)]=temp[temp[date_index[i]:].index('Damage Amount Requested')+date_index[i]+1]
            else:
                disclosure['Damage Amount Requested '+str(i+1)]=None
    #Damages Granted            
        if i<len(date_index)-1:
            if 'Damages Granted' in temp[date_index[i]:date_index[i+1]]: 
                disclosure['Damages Granted '+str(i+1)]=temp[temp[date_index[i]:date_index[i+1]].index('Damages Granted')+date_index[i]+1]
            else:
                disclosure['Damages Granted '+str(i+1)]=None
        else:
            if 'Damages Granted' in temp[date_index[i]:]:
                disclosure['Damages Granted '+str(i+1)]=temp[temp[date_index[i]:].index('Damages Granted')+date_index[i]+1]
            else:
                disclosure['Damages Granted '+str(i+1)]=None
                
    #Resolution            
        if i<len(date_index)-1:
            if 'Resolution' in temp[date_index[i]:date_index[i+1]]: 
                disclosure['Resolution '+str(i+1)]=temp[temp[date_index[i]:date_index[i+1]].index('Resolution')+date_index[i]+1]
            else:
                disclosure['Resolution '+str(i+1)]=None
        else:
            if 'Resolution' in temp[date_index[i]:]:
                disclosure['Resolution '+str(i+1)]=temp[temp[date_index[i]:].index('Resolution')+date_index[i]+1]
            else:url='http://brokercheck.finra.org/Individual/Summary/3122170' #url
    
    
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
    current['current firm CRD']=[int(s) for s in tem[0].replace(')','').split() if s.isdigit()][0]
    
    for ind in range(1,1+len(tem)-1):
        current['current address '+str(ind)]=tem[ind]
        
    #previous registration
    previous={}
        
    tmp=[pre.get_text().replace('\r','').split('\n') for pre in d_soup.findAll('div',{'id':'prevregistrationSection'})]
    x=[i.replace('-','').strip() for i in tmp[0] if i.strip()!='']
    
    for idx in range(1,len(x)/5+1):
        previous['previous firm '+str(idx)+' starts']=x[(idx-1)*5+1]
        previous['previous firm '+str(idx)+' ends']=x[(idx-1)*5+2]
        previous['previous firm '+str(idx) + ' name ']=x[(idx-1)*5+3]
        previous['previous firm '+str(idx) + ' CRD ']=x[(idx-1)*5+4]
        previous['previous firm '+str(idx) + ' location ']=x[(idx-1)*5+5]
        
    
    #---------------------------------------------------------------------------------------------
    #disclosure briefs
#    disclosure_date=[i.get_text().lstrip().rstrip() for i in d_soup.findAll('div',{'class':'discfirstcolumn TextBold'})]
#    disclosure_type=[i.get_text().lstrip().rstrip() for i in d_soup.findAll('div',{'class':'discsecondcolumn TextBold'})]
        
    #set up scrape and javascript 
    
    driver = webdriver.Firefox() #open firefox
    driver.get(url)
    
    driver.find_element_by_id("ctl00_phContent_TermsAndCondUC_BtnAccept").click() #click on accept
    for i in driver.find_elements_by_id("plus"):    
        i.click() #click on expand
    
    
    # get the disclosure details and save in dictionary
    disclosure={}
    temp=driver.find_element_by_xpath('//table[@id="disclosuretable"]').text.split('\n')
    date_index=[temp.index(i) for i in temp if re.search(r'(\d+/\d+/\d+)',i)]
    
    for i in range(min(10,len(date_index))):
        disclosure['dis_date '+str(i+1)]=temp[date_index[i]]
        disclosure['dis_type '+str(i+1)]=temp[date_index[i]+1]
            
        if i<len(date_index)-1:
            if 'Allegations' in temp[date_index[i]:date_index[i+1]]: 
                disclosure['Allegations '+str(i+1)]=temp[temp[date_index[i]:date_index[i+1]].index('Allegations')+date_index[i]+1]
            else:
                disclosure['Allegations '+str(i+1)]=None
        else:
            if 'Allegations' in temp[date_index[i]:]:
                disclosure['Allegations '+str(i+1)]=temp[temp[date_index[i]:].index('Allegations')+date_index[i]+1]
            else:
                disclosure['Allegations '+str(i+1)]=None
    
    #Damage Amount Requested
        if i<len(date_index)-1:
            if 'Damage Amount Requested' in temp[date_index[i]:date_index[i+1]]: 
                disclosure['Damage Amount Requested '+str(i+1)]=temp[temp[date_index[i]:date_index[i+1]].index('Damage Amount Requested')+date_index[i]+1]
            else:
                disclosure['Damage Amount Requested '+str(i+1)]=None
        else:
            if 'Damage Amount Requested' in temp[date_index[i]:]:
                disclosure['Damage Amount Requested '+str(i+1)]=temp[temp[date_index[i]:].index('Damage Amount Requested')+date_index[i]+1]
            else:
                disclosure['Damage Amount Requested '+str(i+1)]=None
    #Damages Granted            
        if i<len(date_index)-1:
            if 'Damages Granted' in temp[date_index[i]:date_index[i+1]]: 
                disclosure['Damages Granted '+str(i+1)]=temp[temp[date_index[i]:date_index[i+1]].index('Damages Granted')+date_index[i]+1]
            else:
                disclosure['Damages Granted '+str(i+1)]=None
        else:
            if 'Damages Granted' in temp[date_index[i]:]:
                disclosure['Damages Granted '+str(i+1)]=temp[temp[date_index[i]:].index('Damages Granted')+date_index[i]+1]
            else:
                disclosure['Damages Granted '+str(i+1)]=None
                
    #Resolution            
        if i<len(date_index)-1:
            if 'Resolution' in temp[date_index[i]:date_index[i+1]]: 
                disclosure['Resolution '+str(i+1)]=temp[temp[date_index[i]:date_index[i+1]].index('Resolution')+date_index[i]+1]
            else:
                disclosure['Resolution '+str(i+1)]=None
        else:
            if 'Resolution' in temp[date_index[i]:]:
                disclosure['Resolution '+str(i+1)]=temp[temp[date_index[i]:].index('Resolution')+date_index[i]+1]
            else:
                disclosure['Resolution '+str(i+1)]=None            
    
    
    #Sactions
        if i<len(date_index)-1:
            if 'Sanctions' in temp[date_index[i]:date_index[i+1]]: 
                disclosure['Sanctions '+str(i+1)]=temp[temp[date_index[i]:date_index[i+1]].index('Sanctions')+date_index[i]+1]
            else:
                disclosure['Sanctions '+str(i+1)]=None
        else:
            if 'Sanctions' in temp[date_index[i]:]:
                disclosure['Sanctions '+str(i+1)]=temp[temp[date_index[i]:].index('Sanctions')+date_index[i]+1]
            else:
                disclosure['Sanctions '+str(i+1)]=None               
     
    #Broker Comments
        if i<len(date_index)-1:
            if 'Broker Comment' in temp[date_index[i]:date_index[i+1]]: 
                disclosure['Broker Comment '+str(i+1)]=temp[temp[date_index[i]:date_index[i+1]].index('Broker Comment')+date_index[i]+1]
            else:
                disclosure['Broker Comment '+str(i+1)]=None
        else:
            if 'Broker Comment' in temp[date_index[i]:]:
                disclosure['Broker Comment '+str(i+1)]=temp[temp[date_index[i]:].index('Broker Comment')+date_index[i]+1]
            else:
                disclosure['Broker Comment '+str(i+1)]=None                       
 
    ##merge dictionary
    data=dict(summary)
    data.update(current)
    data.update(previous)
    data.update(disclosure)
    
    return data