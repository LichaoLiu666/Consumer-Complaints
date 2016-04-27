import random
with open("C:\Users\J046314\Documents\IPython Notebooks\Algorithm\Hw3-Mini Cut\Test1.txt", "r") as f:
    original=[ map(int,line.split(' ')) for line in f ]

        
link_list=[]        
length=len(original)
min_cut=len(original)
#%convert all the larger to smaller
def convert(amatrix,a,b):
    for i in range(len(amatrix)):
        line=amatrix[i]
        if line.count(b)>=1: line[line.index(b)]=a
        line.sort()       
        amatrix[i]=line
    return amatrix
    

for x in range(100000):
    random.seed(x+41566)
    num_cut=0
    
    with open("C:\Users\J046314\Documents\IPython Notebooks\Algorithm\Hw3-Mini Cut\Test1.txt", "r") as f:
        amatrix=[ map(int,line.split(' ')) for line in f ]  
    
    while len(link_list)==0 or  (not (len(set(reduce(lambda x,y: x+y, link_list)))==length-1 and len(link_list)==1)) \
        and (not (len(link_list)>1 and len(set(reduce(lambda x,y: x+y, link_list)))==length)):
        first_node=random.randint(1,len(amatrix))
        second_node=random.sample(amatrix[first_node-1],1)[0]
        temp=[first_node,second_node]
        temp.sort()
        
        if len(link_list)==0:
            link_list.append(temp)     
            amatrix=convert(amatrix,temp[0],temp[1])
        
        else:
        #    pdb.set_trace()
            while first_node==second_node or temp in link_list:
                first_node=random.sample(reduce(lambda x,y: x+y,link_list),1)[0]  
                second_node=random.sample(amatrix[first_node-1],1)[0]
                temp=[first_node,second_node]
                temp.sort()
            if first_node not in reduce(lambda x,y:x+y,link_list) \
            and second_node not in reduce(lambda x,y:x+y,link_list):
                link_list.append(temp)          
                amatrix=convert(amatrix,temp[0],temp[1])
            else:         
                for idx in range(len(link_list)):
                    if first_node in link_list[idx]:
                        temp=link_list[idx]+[second_node]
                        amatrix=convert(amatrix,temp[0],second_node)
                        temp.sort()
                        link_list[idx]=temp
                        break    
                    elif  second_node in link_list[idx]:
                        temp=link_list[idx]+[first_node]
                       
                        amatrix=convert(amatrix,temp[0],first_node)
                        temp.sort()
                        link_list[idx]=temp
                        break
                l_list=range(len(link_list))    
                l_list.remove(idx)
                for l in l_list:
                    if set(link_list[idx]).intersection(set(link_list[l])):
                        link_list[idx]=list(set(link_list[idx]+link_list[l]))
                        link_list.remove(link_list[l])
                        break
        
        consolidate_list=list(set(amatrix[first_node-1]+amatrix[second_node-1]))
        amatrix[first_node-1]=consolidate_list
        amatrix[second_node-1]=consolidate_list
#        print 'first and second node: '+ str(first_node)+','+str(second_node)
#        print link_list
#        print amatrix
        
    if len(link_list)==1:
        link_list.append(list(set(range(1,length+1)).difference(set(link_list[0]))))
    #find minicut
    if len(set(link_list[0]))<len(set(link_list[1])):
        short_list=list(set(link_list[0]))
    else:
        short_list=list(set(link_list[1]))
    
    for i in short_list:
        num_cut+=len(set(original[i-1]).difference(set(short_list)))
    if num_cut<min_cut:
        min_cut=num_cut
    print short_list
    print min_cut


        
        
        
        
