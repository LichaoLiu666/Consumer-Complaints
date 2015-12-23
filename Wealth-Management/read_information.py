def retrieve_broker(crd):
    
    import numpy as np
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.support.wait import WebDriverWait
    import time

    
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
    if d_soup.find('div','summarybizcardsectionNoborder'):
        xx=d_soup.find('div','summarybizcardsectionNoborder').text.lstrip().rstrip()
        
        briefs=[th.get_text().lstrip().rstrip() for th in d_soup.findAll('div',{'class':'summarybizcardsection'})]
        briefs+=[i.strip() for i in briefs.pop(2).split('\n\r\n')]
        
        summary={}
        summary['title']=xx.replace('\n\r\n        ',',')
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
            current['current registration starts']='' 
            current['current firm name']=''
            current['current firm CRD']=''
            current['current address']=''
    
        #previous registration
        previous={}
            
        tmp=[pre.get_text().replace('\r','').split('\n') for pre in d_soup.findAll('div',{'id':'prevregistrationSection'})]
        x=[i.replace('-','').strip() for i in tmp[0] if i.strip()!='']
        
        CRD_index=[x.index(ele) for ele in x if 'CRD' in ele]     
        
        
        for idx in range(len(CRD_index)):
            previous['previous firm '+str(idx+1)+' starts']=x[CRD_index[idx]-3]
            previous['previous firm '+str(idx+1)+' ends']=x[CRD_index[idx]-2]
            previous['previous firm '+str(idx+1) + ' name ']=x[CRD_index[idx]-1]
            previous['previous firm '+str(idx+1) + ' CRD ']=x[CRD_index[idx]]
            
        
        #---------------------------------------------------------------------------------------------
        #disclosure briefs
    #    disclosure_date=[i.get_text().lstrip().rstrip() for i in d_soup.findAll('div',{'class':'discfirstcolumn TextBold'})]
    #    disclosure_type=[i.get_text().lstrip().rstrip() for i in d_soup.findAll('div',{'class':'discsecondcolumn TextBold'})]
    #        
        #set up scrape and javascript 
        
        driver = webdriver.Firefox() #open firefox
        driver.get(url)
        time.sleep(1)        
        
        driver.find_element_by_id("ctl00_phContent_TermsAndCondUC_BtnAccept").click() #click on accept
        for i in  driver.find_elements_by_id("plus"):    
            i.click() #click on expand
        
        time.sleep(2)
        # get the disclosure details and save in dictionary
        disclosure={}
        if summary['num_disclosure']>0:
            temp= WebDriverWait(driver, 10).until(lambda driver :driver.find_element_by_xpath('//table[@id="disclosuretable"]')).text.split('\n')
            date_index=[temp.index(i) for i in temp if re.search(r'(^\d+/\d+/\d+$)',i)]
            
            for i in range(min(10,len(date_index))):
                disclosure['dis_date '+str(i+1)]=temp[date_index[i]]
                disclosure['dis_type '+str(i+1)]=temp[date_index[i]+1]
                
#                print len(date_index)-1
                if i<len(date_index)-1:
                    if 'Allegations' in temp[date_index[i]:date_index[i+1]]: 
                        disclosure['Allegations '+str(i+1)]=temp[temp[date_index[i]:date_index[i+1]].index('Allegations')+date_index[i]+1]
                    else:
                        disclosure['Allegations '+str(i+1)]=''
                else:
#                    print driver.find_element_by_xpath('//table[@id="disclosuretable"]').text
                    if 'Allegations' in temp[date_index[i]:]:
                        disclosure['Allegations '+str(i+1)]=temp[temp[date_index[i]:].index('Allegations')+date_index[i]+1]
                    else:
                        disclosure['Allegations '+str(i+1)]=''
            
            #Damage Amount Requested
                if i<len(date_index)-1:
                    if 'Damage Amount Requested' in temp[date_index[i]:date_index[i+1]]: 
                        disclosure['Damage Amount Requested '+str(i+1)]=temp[temp[date_index[i]:date_index[i+1]].index('Damage Amount Requested')+date_index[i]+1]
                    else:
                        disclosure['Damage Amount Requested '+str(i+1)]=''
                else:
                    if 'Damage Amount Requested' in temp[date_index[i]:]:
                        disclosure['Damage Amount Requested '+str(i+1)]=temp[temp[date_index[i]:].index('Damage Amount Requested')+date_index[i]+1]
                    else:
                        disclosure['Damage Amount Requested '+str(i+1)]=''
            #Damages Granted            
                if i<len(date_index)-1:
                    if 'Damages Granted' in temp[date_index[i]:date_index[i+1]]: 
                        disclosure['Damages Granted '+str(i+1)]=temp[temp[date_index[i]:date_index[i+1]].index('Damages Granted')+date_index[i]+1]
                    else:
                        disclosure['Damages Granted '+str(i+1)]=''
                else:
                    if 'Damages Granted' in temp[date_index[i]:]:
                        disclosure['Damages Granted '+str(i+1)]=temp[temp[date_index[i]:].index('Damages Granted')+date_index[i]+1]
                    else:
                        disclosure['Damages Granted '+str(i+1)]=''
                        
            #Resolution            
                if i<len(date_index)-1:
                    if 'Resolution' in temp[date_index[i]:date_index[i+1]]: 
                        disclosure['Resolution '+str(i+1)]=temp[temp[date_index[i]:date_index[i+1]].index('Resolution')+date_index[i]+1]
                    else:
                        disclosure['Resolution '+str(i+1)]=''
                else:
                    if 'Resolution' in temp[date_index[i]:]:
                        disclosure['Resolution '+str(i+1)]=temp[temp[date_index[i]:].index('Resolution')+date_index[i]+1]
                    else:
                        disclosure['Resolution '+str(i+1)]=''
            #Sactions
                if i<len(date_index)-1:
                    if 'Sanctions' in temp[date_index[i]:date_index[i+1]]: 
                        disclosure['Sanctions '+str(i+1)]=temp[temp[date_index[i]:date_index[i+1]].index('Sanctions')+date_index[i]+1]
                    else:
                        disclosure['Sanctions '+str(i+1)]=''
                else:
                    if 'Sanctions' in temp[date_index[i]:]:
                        disclosure['Sanctions '+str(i+1)]=temp[temp[date_index[i]:].index('Sanctions')+date_index[i]+1]
                    else:
                        disclosure['Sanctions '+str(i+1)]=''               
             
            #Broker Comments
                if i<len(date_index)-1:
                    if 'Broker Comment' in temp[date_index[i]:date_index[i+1]]: 
                        disclosure['Broker Comment '+str(i+1)]=temp[temp[date_index[i]:date_index[i+1]].index('Broker Comment')+date_index[i]+1]
                    else:
                        disclosure['Broker Comment '+str(i+1)]=''
                else:
                    if 'Broker Comment' in temp[date_index[i]:]:
                        disclosure['Broker Comment '+str(i+1)]=temp[temp[date_index[i]:].index('Broker Comment')+date_index[i]+1]
                    else:
                        disclosure['Broker Comment '+str(i+1)]=''                  
        driver.quit()

        ##merge dictionary
        data=dict(summary)
        data['CRD']=crd
        data['Name']=d_soup.find('span',{'class':'summarydisplayname'}).text
        data.update(current)
        data.update(previous)
        data.update(disclosure)
    
        return data
    else:
        pass

#----------------------------------------------
#Main Function
#retrieve_broker(crd)
import pandas as pd
#
CRD=pd.read_csv('crd.csv')
output={}
##crd=2176306
#output.append(retrieve_broker(crd))
#
#
for crd in CRD.CRD:
    print crd
    temp=retrieve_broker(crd)
    if temp: output[temp['CRD']]=temp
    
df=pd.DataFrame.from_dict(output,orient='index')
df.to_csv('output_all.csv')
