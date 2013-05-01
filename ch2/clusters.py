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

# 가로줄 비교 통한 군집화
def hcluster(rows, distance = pearson):
    distances = {}
    currentclustid = -1
    
    # rows == data 블로그의 단어 출현수를 나타내는 rows들 
    # 변수 data에 저장한 값들을 bicluster class로 생성. clust[0].vec, clust[1].vec ...
    clust = [bicluster(rows[i], id = i) for i in range(len(rows))]
    
    # clust에 1개만 남을 때까지 반복,
    while len(clust) > 1:
        # 기본 1쌍을 설정해둠
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)
        
        # 가장 작은 거리값을 가지는 쌍을 찾는 루프. 
        for i in range(len(clust)):
            # len(clust) 는 0~99. 총 100개의 블로그이므로.
            # clust[i].vec = 각 단어들의 빈도 수 저장.   len(clust[i].vec) = 706개   
            # (0, 1), (0, 2), (0, 3), ... ,(0, 99). 
            # (1, 2), (1, 3), (1,4), ... , (1, 99)
            # (98, 99)
            for j in range(i + 1, len(clust)):
                if (clust[i].id, clust[j].id) not in distances:
                    # distances[(0,1)] = clust[0].
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)
                    d = distances[clust[i].id, clust[j].id]
                    if d < closest:
                        closest = d
                        lowestpair = (i, j)
        
        # loop 돌고나면 closest, lowestpair 값이 하나만 남게 됨. 가장 유사한 한 쌍. 
        # 그 한 쌍의 vec 값들을 가지고 평균계산하여 list에 저장
        mergevec = [(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) / 2.0 for i in range(len(clust[0].vec))]
        
        # 다시 그 한 쌍으로 새로운 군집을 생성. 그 군집을 다시 넣어 나머지 블로그들과 비교하기 위함. 그래서 mergevec 값을 구해둔 것임
        # left / right 값이 있음. (x, y)에서 lowestpair[0] == x, lowestpair[1] == y 
        newcluster = bicluster(mergevec, left = clust[lowestpair[0]], right = clust[lowestpair[1]], distance = closest, id = currentclustid)
        
        # 원래의 집합 안에 포함되지 않은 군집 id들은 음수임
        currentclustid -= 1
        # 최저 한 쌍으로 나온 값을 clust에서 삭제. while 구문 아래이므로.
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        #그리고 최저 한 쌍으로 새로 만든 군집을 clust에 삽입.
        clust.append(newcluster)
    
    # while 이 끝나면 최종으로 남은 하나의 군집을 return
    # 최종 남은 군집은 새로 묶어낸 가장 큰 군집이므로 id는 음수값을 가질 수 밖에 없음 
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

    
from PIL import Image, ImageDraw

def getheight(clust):
    if clust.left == None and clust.right == None: return 1
    
    return getheight(clust.left) + getheight(clust.right)

def getdepth(clust):
    if clust.left == None and clust.right == None: return 0
    
    return max(getdepth(clust.left), getdepth(clust.right)) + clust.distance

def drawdendrogram(clust, labels, jpeg='clusters.jpg'):
    h = getheight(clust) * 20
    w = 1200
    depth = getdepth(clust)
    
    scaling = float(w - 150) / depth
    
    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    draw.line((0, h/2, 10, h/2), fill = (255, 0, 0))
    
    drawnode(draw, clust, 10, (h/2), scaling, labels)
    img.save(jpeg, 'JPEG')
    
def drawnode(draw, clust, x, y, scaling, labels):
    if clust.id < 0:
        h1 = getheight(clust.left) * 20
        h2 = getheight(clust.right) * 20
        top = y - (h1 +h2 ) / 2
        bottom = y + (h1 + h2) / 2  
        
        ll =  clust.distance * scaling
        draw.line((x, top + h1/2, x, bottom - h2/2), fill = (255, 0, 0))
        draw.line((x, top + h1/2, x + ll, top + h1/2), fill = (255, 0, 0))
        draw.line((x, bottom - h2/2, x + ll, bottom - h2/2), fill = (255, 0, 0))
        
        drawnode(draw, clust.left, x + ll, top + h1/2, scaling, labels)
        drawnode(draw, clust.right, x + ll, bottom - h2/2, scaling, labels)
        
    else:
        draw.text((x + 5, y - 7), labels[clust.id], (0, 0, 0))
         
              
def rotatematrix(data):
    newdata = []
    for i in range(len(data[0])):
        newrow = [data[j][i] for j in range(len(data))]
        newdata.append(newrow)
    return newdata



import random

def kcluster(rows, distance = pearson, k = 4):
    # 가로줄마다에 들어있는 값 중 최대, 최소값을 구함, for 706 times(== 총 단어 수)
    ranges = [(min([row[i] for row in rows]), max([row[i] for row in rows])) for i in range(len(rows[0]))]
    # range "최대값 - 최소값"  *  랜덤값 것들의 리스트의 리스트
    # 임의로 k개의 중심점을 생성
    clusters = [[random.random() * (ranges[i][1] - ranges[i][0]) for i in range(len(rows[0]))] for j in range(k)]
    
    lastmatches=None
    for t in range(100):
        print 'Iteration %d' % t
        bestmatches = [[] for i in range(k)]
        
        #각 가로줄별로 가장 근접한 중심점 찾기
        for j in range(len(rows)):
            row = rows[j]
            bestmatch = 0
            for i in range(k):
                d = distance(clusters[i], row)
                if d < distance(clusters[bestmatch], row): bestmatch = 1
            bestmatches[bestmatch].append(j)
        
        # 이전과 같은 결과라면 완료시킴    
        if bestmatches == lastmatches: break
        lastmatches = bestmatches
            
            # 중심점을 멤버들의 평균으로 이동시킴
        for i in range(k):
            avgs = [0.0] * len(rows[0])
            if len(bestmatches[i]) > 0:
                for rowid in bestmatches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m] += rows[rowid][m]
                for j in range(len(avgs)):
                    avgs[j] /= len(bestmatches[i])
                clusters[i] = avgs
   
    # 결국 id를 반환하는 셈                 
    return bestmatches

            
            
