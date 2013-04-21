# -*- coding: utf-8 -*-
def readfile(filename):
    # file()
    lines = [line for line in file(filename)]
    
    # example
    # str = "0000000this is string example....wow!!!0000000";
    # print str.strip( '0' );
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    
    for line in lines[1:]:
        # p 는 tab를 구분기준으로 삼고 나누어 column(0 to end) 생성함
        p = line.strip().split('\t')
        rownames.append(p[0])
        # float()로 wordcount 숫자값을 str --> float으로 변환
        data.append([float(x) for x in p[1:]])
    # rownames = 블로그이름, colnames = 단어, data = 카운트
    # blogdata.txt를 rownames, colnames, data로 각각 저장해둔 셈 = 읽기만 했을 뿐임       
    return rownames, colnames, data

# !!중요: 공식을 외울 필요는 없고, 공식의 목적과 결과가 적합한지만 생각하면 된다.
# wordcount 값을 가지고 각 '블로그' 간의 correlation 값을 돌려받기 위함
from math import sqrt
def pearson(v1, v2):
    # v1과 v2의 Cov / (v1 표준편차 * v2 표준편차)

    # v1, v2 각각의 합
    sum1 = sum(v1)
    sum2 = sum(v2)
    # v1 * v2 의 합
    # v1, v2 중 어느 한 쪽이라도 기준을 잡아도 됨. 어차피 데이터 수가 더 많은 쪽을 기준으로 해도 한 쪽의 데이터가 없다면 결과값은 0 이므로.
    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])
    # 분자: v1과 v2의 공분산(Covariance)
    num = pSum - (sum1 * sum2 / len(v1))
    
    # v1, v2 제곱의 합
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])
    # 분모: v1 분산 * v2 분산(Variance)에 스퀘어루트 = Standard Deviation(표준편차)
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v2)))
    if den == 0: return 0
    
    # return 값을 두 항목간의 유사정도를 나타내는 거리 값으로 쓰기 위해 1에서 뺌.(유사할수록 가까우므로)
    return 1.0 - num/den

# 계층적 군집화 알고리즘에서 각 군집은 두 개의 브랜치를 가지는 트리의 한 점이거나 데이터 세트에서 실제 가로줄과 연계된 종점이다.
# 그래서 각 군집은 위치데이터를 가지고, 이는 종점인 가로줄 데이터 or 두 브랜치에서 병합된 데이터 중 하나이다.
# 계층구조 만들기 
class bicluster:
    def __init__(self, vec, left = None, right = None, distance = 0.0, id = None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance

def hcluster(rows, distance = pearson):
    distances = {}
    currentclustid = -1
    
    # 초기 군집들을 각 가로줄에서 생성함
    clust = [bicluster(rows[i], id = i) for i in range(len(rows))]
    
    # clust에 2개 이상의 리스트가 존재하면,
    while len(clust) > 1:
        # 최저 좌표 한 쌍은 row=0, col=1
        lowestpair = (0, 1)
        # class bicluster 중  __init__ 에서 미리 정의한 부분이 나옴
        # clust[0], [1] 사이의  pearson() 값 저장
        closest = distance(clust[0].vec, clust[1].vec)
        
        # 가장 작은 거리값을 가지는 쌍을 찾는 루프    
        for i in range(len(clust)):
            # clust[1] ~ 끝까지 
            for j in range(i + 1, len(clust)):
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)
                    d = distances[clust[i].id, clust[j].id]
                    if d < closest:
                        closest = d
                        lowestpair = (i, j)
        
        # 두 군집간 평균계산
        mergevec = [(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) / 2.0 for i in range(len(clust[0].vec))]
        
        # 새로운 군집을 생성
        newcluster = bicluster(mergevec, left = clust[lowestpair[0]], right = clust[lowestpair[1]], distance = closest, id = currentclustid)
        
        # 원래의 집합 안에 포함되지 않은 군집 id들은 음수임
        currentclustid -= 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)
        
    return clust[0]

def printclust(clust, labels = None, n = 0):
    # 들여쓰기
    for i in range(n): print '   ',
    if clust.id < 0:
        # id 값이 음수면, 트리의 브랜치임
        print '-'
    else:
        # id값이 양수면, 트리의 종점임
        # label 에는 blognames가 들어감
        if labels == None: print clust.id
        else: print labels[clust.id]
    
    # 우측과 좌측 브랜치를 출력
    if clust.left != None: printclust(clust.left, labels = labels, n = n + 1)
    if clust.right != None: printclust(clust.right, labels = labels, n = n + 1)
    
                        
                