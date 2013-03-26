#-*- coding: utf-8 -*-
import feedparser
import re

def getwordcounts(url):
    d=feedparser.parse(url)
    wc={}
    
    # 모든 게시글별로 루프 돌림
    # entry 객체 아래 내용에 게시물 관련 내용들이 나옴. xml 샘플 참조. 
    # 일부 feedlist 에서 'title'이 없어 feedparser가 에러남. feedlist의 RSS 형태를 열어보고 feedparser로 해결방법 찾아보기. 
    # 결론: 8번째 feed가 잘못 된거였음
     
    for e in d.entries:
        if 'summary' in e: summary=e.summary
        else: summary=e.description
        
        # getwords는 아래에서 정의 
        words=getwords(e.title+' '+summary)
        # title과 summary의 내용만 검토할 경우 
        for word in words:
            wc.setdefault(word, 0)
            wc[word]+=1
    return d.feed.title, wc

def getwords(html):
    # HTML 태그 제거가 목적. [^>]: > 첫 문자열이 >인 것은 제외.
    # .sub?
    txt=re.compile(r'<[^>]+>').sub('', html)
    
    words=re.compile(r'[^A-Z^a-z]').split(txt)
    return [word.lower() for word in words if word!='']

# 각 단어가 나온 블로그 수. wc는 블로그 내에서 해당 단어가 나타난  
apcount={}
#wordcount는 왜 만들었는지 잘 모르겠음. {'제목': wc} 형태로 정리해서 파일출력 때 활용하려고. 
wordcounts={}
feedlist=[]
for feedurl in file('feedlist.txt'):
    feedlist.append(feedurl)
    title,wc=getwordcounts(feedurl)
    wordcounts[title]=wc
    for word,count in wc.items():
        apcount.setdefault(word, 0)
        #wc 안의 key값인 count의 value 1이라도 있다면. 
        if count>=1:
            apcount[word]+=1

wordlist=[]
for w,bc in apcount.items():
    frac=float(bc)/len(feedlist)
    if frac>0.1 and frac<0.5: wordlist.append(w)

out=file('blogdata.csv', 'w')
out.write('Blog')
for word in wordlist: out.write('\t%s' % word)
out.write('\n')
# blog == title
for blog,wc in wordcounts.items():
    out.write(blog)
    # wordlist에는 wc에 담긴 정보 중 필요한 범위만큼만 있으므로.
    for word in wordlist:
        if word in wc: out.write('\t%d' % wc[word])
        else: out.write('\t0')
    out.write('\n')
    
    
