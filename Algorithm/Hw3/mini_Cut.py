import random

with open("C:\Users\J046314\Documents\IPython Notebooks\Algorithm\Hw3-Mini Cut\Test1.txt", "r") as f:
    amatrix=[ map(int,line.split(' ')) for line in f]
    
random.seed(1)

while len(amatrix)>2:
    first_node=random.randint(1,len(amatrix))
    second_node=random.sample(amatrix[first_node-1],1)[0]
    print 'first and second node: '+ str(first_node)+','+str(second_node)
    
    consolidate_list=map(lambda x:x,set(amatrix[first_node-1]+amatrix[second_node-1]))
    amatrix[first_node-1]=consolidate_list
    amatrix[second_node-1]=consolidate_list

#    amatrix=amatrix[0:second_node-1]+amatrix[second_node:]
    for i in range(len(amatrix)):
        line=amatrix[i]
        if line.count(second_node)>=1: line[line.index(second_node)]=first_node
        line.sort()       
        amatrix[i]=line

#        amatrix[j]=[ele for ele in amatrix[j] if ele<second_node]+[ele-1 for ele in line if ele>second_node]

    list=[]        
    for j in range(len(amatrix)-1):
        for k in range(j+1,len(amatrix)):
            print j,k,amatrix[j],amatrix[k]
            if amatrix[j]==amatrix[k]:  list+=[k]
                
    for l in list:
        for j in range(len(amatrix)):
            amatrix[j]=[ele for ele in amatrix[j] if ele<=l]+[ele-1 for ele in amatrix[j] if ele>l]    
            
    for l in list:
        amatrix=amatrix[0:l-1]+amatrix[l:]           
        
    for j in amatrix:
        amatrix[j]=[ele for ele in amatrix[j] if ele<k]+[ele-1 for ele in line if ele>k]
#
# 
