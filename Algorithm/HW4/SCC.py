#==============================================================================
# Read Data 
#==============================================================================
source='C:\Users\J046314\Documents\IPython Notebooks\Algorithm\Hw4-SCC\Test1.txt'
def getG(source):
    G={}
    Grev={}
    for i in range(1,N+1):
        G[i]=[]
        Grev[i]=[]
    fin=open(source)
    for line in fin:
        v1=int(line.split()[0])
        v2=int(line.split()[1])
        G[v1].append(v2)
        Grev[v2].append(v1)
    fin.close()
    return G, Grev



#define global variable

def _init_(N):
    finish=dict(zip(range(1,N+1),[0]*N))
    leader=dict(zip(range(1,N+1),[0]*N))
    visited=dict(zip(range(1,N+1),[0]*N))
    return finish,leader,visited
    
def dfs_loop(G):
    global t
    global s
    t=0
    s=0
    for i in range(N,0,-1):
        if not visited[i]:
            s=i
            dfs(G,i)    
            
def dfs(G,i):     
    global t
    visited[i]=1
    leader[i]=s
    if i in G.keys():
        for j in G[i]:
            if not visited[j]:
                dfs(G,j)
        t=t+1
        finish[i]=t
    
G,revG=getG(source)
N=9
finish,leader,visited=_init_(N)
dfs_loop(revG)

newGraph={}
for i in range(1,N+1):
    temp=[]
    for x in g[i]: temp.append(finish[x])
    newGraph[finish[i]]=temp

finish,leader,visited=_init_(N)    
dfs_loop(newGraph)
print sorted([leader.values().count(i) for i in set(leader.values())],reverse=True)[:5]

    

