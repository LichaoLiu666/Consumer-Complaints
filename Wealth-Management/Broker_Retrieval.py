
"""
This module is used to retrieve broker's detailed information from brokercheck.finra.org
"""


#----------------------------------------------
#Main Function

CRD=pd.read_csv('crd.csv')

for crd in CRD.CRD:
    retrieve_broker(crd)
    
pd.DataFrame.from_dict(data, orient="index")