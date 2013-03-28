
def readfile(filename):
    # file()
    lines=[line for line in file(filename)]
    
    # example
    # str = "0000000this is string example....wow!!!0000000";
    # print str.strip( '0' );
    colnames=lines[0].strip().split('\t')[1:]
    rownames=[]
    data=[]
    
    for line in lines[1]:
        p=line.strip().split('\t')
        rownames.append(p[0])
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data

from math import sqrt
def pearson(v1,v2):
    sum1=sum(v1)
    sum2=sum(v2)
    
    sum1Sq=sum([pow(v1,2) for v in v1])
    sum2Sq=sum([pow(v2,2) for v in v2])
    
    pSum=sum([v1[i]*v2[i] for i in range(len(v1))])
    
    num=pSum-(sum1*sum2/len(v1))
    den=sqrt((sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v2)))
    if den==0: return 0
    
    return 1.0-num/den

class bicluster:
    def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
        self.left=left
        self.right=right
        self.vec=vec
        self.id=id
        self.distance=distance

def hcluster(rows, distance=pearson):
    distances={}
    currentclustid=-1
    
    clust=[bicluster(row[i], id=i) for i in range(len(rows))]
    
    # clust에 2개 이상의 리스트가 존재하면,
    while len(clust)>1:
        # 최저 좌표 한 쌍은 row=0, col=1
        lowestpair=(0,1)
        # class bicluste 중  __init__ 에서 미리 정의한 부분이 나옴
        closest=distance(clust[0].vec, clust[1].vec)
        
                