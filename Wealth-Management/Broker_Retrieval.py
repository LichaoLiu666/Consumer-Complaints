
"""
This module is used to retrieve broker's detailed information from brokercheck.finra.org
"""


#----------------------------------------------
#Main Function

CRD=pd.read_csv('crd.csv')
output=[]
#crd=1696906




for crd in CRD.CRD:
    output.append(retrieve_broker(crd))
    
df=pd.DataFrame.from_dict(output)
df.set_index('CRD')
df.to_csv('output.csv')