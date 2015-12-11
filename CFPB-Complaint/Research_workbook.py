
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from collections import Counter
import re
import nltk


# In[2]:

#read all the complaint data
CFPB_consumer_complaints_20151130=pd.read_csv('Consumer_Complaints.csv')

#change column name
# l=list(CFPB_consumer_complaints_20151130.columns)
# l[2]='Subproduct'
new_column=['Date_received', 'Product', 'Subproduct', 'Issue', 'Subissue',
       'Complaint_narrative', 'Company_public_response', 'Company',
       'State', 'ZIP code', 'Submitted_via', 'Date_sent_to_company',
       'Company_response_to_consumer', 'Timely_response',
       'Consumer_disputed', 'Complaint_ID']
CFPB_consumer_complaints_20151130.columns=new_column


# #Citizens Checking Complaint

# In[3]:

Citizens_Checking=CFPB_consumer_complaints_20151130.query("Subproduct=='Checking account' and Company in 'RBS Citizens'")

#Pull Citizens complaint narrative for loss and nonloss 
Citizens_Checking_Loss_Narrative=Citizens_Checking.query("Company_response_to_consumer=='Closed with monetary relief'")['Complaint_narrative'][~Citizens_Checking['Complaint_narrative'].isnull()]
Citizens_Checking_NotLoss_Narrative=Citizens_Checking.query("Company_response_to_consumer!='Closed with monetary relief'")['Complaint_narrative'][~Citizens_Checking['Complaint_narrative'].isnull()]


# In[4]:

#studying simple word frequency does not offer anything meaningful. 
#need to analyze phrase or specific type of word
print (Counter(re.findall('\w+', ''.join(Citizens_Checking_Loss_Narrative).lower())).most_common(20)) #loss narative

print (Counter(re.findall('\w+', ''.join(Citizens_Checking_NotLoss_Narrative).lower())).most_common(20)) #nonloss narative


# In[97]:

#Look at the most frequent 25 words
freq = nltk.FreqDist(re.findall('\w+', ''.join(Citizens_Checking_Loss_Narrative).lower()))
freq.plot(25)


# ###NLTK

# In[98]:

tokens=nltk.word_tokenize(''.join(Citizens_Checking_Loss_Narrative).lower())
tagged=nltk.pos_tag(tokens)


# In[76]:

nltk.help.upenn_tagset('VB')


# In[96]:

# nltk.FreqDist([w for w,v in tagged if v in ["jj","RB"]]).plot(20)
nltk.FreqDist([w for w,v in tagged if w.endswith('ly')]).plot(20)


# In[82]:

bgs=nltk.bigrams(tokens)
# bgs=nltk.bigrams([w for w,v in tagged if v in ["JJ","NN"]])
fdist = nltk.FreqDist(bgs)
fdist.most_common(10)
# for k,v in fdist.items():
#     print (k,v)


# In[87]:

text=nltk.Text([w for w,v in tagged if v in ["JJ","NN"]])
text.collocations()


# #Stop here

# In[109]:

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()
finder = nltk.collocations.BigramCollocationFinder.from_words(tokens)
finder.nbest(trigram_measures.pmi, 10) 


# In[89]:

phrase=dict()
for i in text.collocations():
    if i not in phrase:
        phrase[i]=1
    else:
        phrase[i]+=1


# In[46]:

wsj = nltk.corpus.treebank.tagged_words(tagset='universal')
cfd1 = nltk.ConditionalFreqDist(wsj)
cfd1['yield'].most_common()


# In[ ]:




# #Peer Bank Checking Complaint

# In[102]:

Peer_Checking=CFPB_consumer_complaints_20151130.query("Subproduct=='Checking account' and Company in ('BB&T Financial','Comerica','Fifth Third Bank','KeyBank NA','M&T Bank','PNC Bank','Regions','SunTrust Bank','U.S. Bancorp')")


# In[39]:

Counter(words).most_common(20)

