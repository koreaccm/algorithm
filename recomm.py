#-*- coding: utf-8 -*-
critics={'Lisa Rose': {'Lady in the Water':2.5, 'Snakes on a Plane':3.5, 'Just My Luck':3.0, 'Superman Returns':3.5, 'You, Me and Dupree':2.5, 'The Night Listener':3.0},
         'Gene Seymour': {'Lady in the Water':3.0, 'Snakes on a Plane':3.5, 'Just My Luck':1.5, 'Superman Returns':5.0, 'The Night Listener':3.0, 'You, Me and Dupree':3.5},
         'Michael Phillips': {'Lady in the Water':2.5, 'Snakes on a Plane':3.0, 'Superman Returns':3.5, 'The Night Listener':4.0},
         'Claudia Puig': {'Snakes on a Plane':3.5, 'Just My Luck':3.0, 'The Night Listener':4.5, 'Superman Returns':4.0, 'You, Me and Dupree':2.5},
         'Mick LaSalle': {'Lady in the Water':3.0, 'Snakes on a Plane':4.0, 'Just My Luck':2.0, 'Superman Returns':3.0, 'The Night Listener':3.0, 'You, Me and Dupree':2.0},
         'Jack Matthews': {'Lady in the Water':3.0, 'Snakes on a Plane':4.0, 'The Night Listener':3.0, 'Superman Returns':5.0, 'You, Me and Dupree':3.5},
         'Toby': {'Snakes on a Plane':4.5, 'You, Me and Dupree':1.0, 'Superman Returns':4.0}
         }

from math import sqrt

def sim_distance(prefs, person1, person2):
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1
        
    if len(si)==0: return 0
        
    sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item], 2) for item in prefs[person1] if item in prefs[person2]])
        
    return 1/(1+sqrt(sum_of_squares))


def sim_person(prefs, p1, p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item]=1

    n = len(si)

    if n==0: return 0
    
    # 이하는 피어슨 상관점수 공식
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    pSum = sum([prefs[p1][it]*prefs[p2][it] for it in si])

    num = pSum - (sum1*sum2/n)
    den = sqrt((sum1Sq - pow(sum1, 2)/n)*(sum2Sq - pow(sum2, 2)/n))

    r = num/den

    return r




def topMatches(prefs, person, n=5, similarity=sim_person):
    #[] 안에 for in 구문을 넣은 것 = 값이 여러 개 나온 것들을 List 형태로 정함. list 안의 각 값은 tuple 형태. (similarity(), other) is (숫자, key(사람이름))
    #List, Tuple, Dictionary 형태와 쓰임새 구분
    scores=[(similarity(prefs, person, other), other) for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]


def getRecommendations(prefs, person, similarity=sim_person):
    totals={}
    simSums={}
    
    #이하에서 other = 사람이름, item = 영화 
    for other in prefs:
        if other == person: continue
        # continue = break. if/while에서 모두 사용
        sim=similarity(prefs, person, other)
        if sim <= 0: continue
        
        #다른 사람들 영화평가가 있는 한
        for item in prefs[other]:
            #내가 보지 못한 영화거나 내 평점이 0점이면.
            if item not in prefs[person] or prefs[person][item] == 0: 
                #setdefault method.    
                #dict.setdefault(key, default=None)  해당 키 값이 없을 때 반환할 value

                #영화에 대한 합계들
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item]              
                simSums.setdefault(item, 0)
                simSums[item] += sim

    # items method
    # dict.items()    tuple pairs 형태로 반환
    rankings=[(totals/simSums[item], item) for item, totals in totals.items()]
                
    # 정렬기준 기본값은 오름차순
    rankings.sort()
    rankings.reverse()
    return rankings

def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            #물건과 사람 바꾸기는 대입해서 치환시켜 버리면 되는구나
            result[item][person] = prefs[person][item]

    return result



            

            
            
