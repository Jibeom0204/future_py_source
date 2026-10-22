# 웹 문서를 읽어 형태소 분석: 위키백과
# 단어 출현 횟수를 DataFrame에 저장

import requests
from bs4 import BeautifulSoup
import pandas as pd
from konlpy.tag import Okt
from urllib import parse # 한글 인코딩

okt=Okt()

#url="https://ko.wikipedia.org/wiki/%EC%9D%B4%EC%88%9C%EC%8B%A0"
para=parse.quote("이순신")
url="https://ko.wikipedia.org/wiki/"+para
print(url)#https://ko.wikipedia.org/wiki/이순신
# para=parse.quote("이순신") => https://ko.wikipedia.org/wiki/%EC%9D%B4%EC%88%9C%EC%8B%A0
# 한글 적을 때는 인코딩 해줘야함

headers={"User-Agent":"Mozila/5.0"}
response = requests.get(url=url, headers=headers)
if response.status_code==200: # URL 정보 받아온 값이 서버 정상적(200)이면
    page=response.text
    #print(page,type(page)) # ....20131598)"}</script></body></html> <class 'str'>
    # str 타입이라 html 태그랑 불필요한 거 많음 => soup으로 변환
    soup=BeautifulSoup(page, 'html.parser')

    wordlist=[] # 형태소 분석을 통해 명사만 기억

    for item in soup.select("#mw-content-text p"):
        #print(item.string)
        if item.string !=None:
            wordlist += okt.nouns(item.string)

    print('wordlist: ',wordlist,'\n')
    print("중복 포함한 단어 수 :",len(wordlist))
    print('set에 넣어 중복 제거 후 단어 수:',len(set(wordlist)),'\n')

    word_dict={} # 단어의 발생횟수를 Dict로 저장
    for i in wordlist:
        if i in word_dict: #word dict에 1번이라도 들어간적이 있다면
            word_dict[i]+=1
        else:
            word_dict[i]=1
    print('word_dict : ',word_dict)

    print('Series로 출력 ---')
    seri_list=pd.Series(wordlist)
    print(seri_list[:3],'\n')# 모든행의 3열까지?
    print(seri_list.value_counts()[:5],'\n')

    seri_dict=pd.Series(word_dict)
    print(seri_dict[:3],'\n')# 모든행의 3열까지?
    print(seri_dict.value_counts()[:5],'\n\n')

    print('DF로 출력 ---')
    df1=pd.DataFrame(wordlist,columns=['단어'])
    print("DF로 출력",df1.head(),'\n')
    df2=pd.DataFrame([word_dict.keys(),word_dict.values()])
    df2=df2.T
    df2.columns=['단어','빈도수']
    print("DF로 출력",df2.head(),'\n')

    result=df2[df2['빈도수']>5] # 5회 등장 이상 단어만
    print("5회 이상 등장 단어: ",result,'\n')
    print("전체 단어 빈도수: ",df2['빈도수'].sum(),'\n')
    print("평균 출현 빈도수: ",df2['빈도수'].mean(),'\n')