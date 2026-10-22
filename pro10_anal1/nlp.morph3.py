# 동아일보 웨에서 특정 단어 관련 문서를 검색 후 명사만 추출
# 워드 클라우드 그리기
# pip install pygame simplejson pytagcloud
# python -m pip uninstall -y pygame
# python -m pip install --upgrade pygame-ce 
# pip install lxml
from bs4 import BeautifulSoup
from urllib.parse import quote
import urllib.request
from konlpy.tag import Okt
from collections import Counter # 단어의 수를 세는 라이브러리
import pytagcloud
import matplotlib.pyplot as plt
import koreanize_matplotlib
import matplotlib.image as mpimg
import webbrowser
import pandas as pd
import numpy as np


# # searchWord=input("검색어")
# # print(quote(searchWord))

# searchWord='가을'
# target_url="https://www.donga.com/news/search?query="+quote(searchWord)
# source_code=urllib.request.urlopen(target_url)
# print("URL 받고 open한 소스코드 확인: ",source_code)
# soup=BeautifulSoup(source_code,'lxml',from_encoding='utf-8')
# # soup=BeautifulSoup(source_code,'html.parser',from_encoding='utf-8')
# print(soup)

# msg=""
# for title in soup.find_all("h4",class_="tit"): # 링크에서 tit 클래스 중 h4 태그들을 title에 저장
#     title_link=title.find("a") #title에 저장된 것중 a 를 찾음 (a 태그인 것들)
#     #print(title_link)
#     article_url=title_link["href"] # a태그에 href를 걸어 링크로 내보냄
#     #print(article_url)

#     try:
#         source_article=urllib.request.urlopen(article_url)
#         soup2=BeautifulSoup(source_article, 'lxml', from_encoding='utf-8')
#         #print(soup2)
#         contents=soup2.select("div.article.txt") # div 태그의 클래스인 aritlcle.txt 가져오기
#         #print(contents)
#         for imsi in contents:
#             item=str(imsi.find_all(string=False))
#             msg+=item

#     except Exception as e:
#         pass
#     #print(article_url)
#     #print(msg)

## 찬우 코드===============================
searchWord = "가을"
target_url = "https://www.donga.com/news/search?query=" + quote(searchWord)  #url을 가지고옴
source_code = urllib.request.urlopen(target_url)  #완성된 주소에 접속하고, 서버의 응답 객체를 source_code에 담아요
# print(source_code)
soup = BeautifulSoup(source_code,'lxml',from_encoding='utf-8')
print(soup)
#동아일보 가을까지만 검색 
msg = ""

#각각의 기사를 들어가서 글들을 가지고옴
for title in soup.find_all("h4", class_="tit"):        #class이름이 tit인것을 차음
    title_link = title.find("a")    #a 태그를 가지고옴
    # print(title_link)
    article_url = title_link["href"]   #title_link 속성중에 href만 가지고옴
    # print(article_url)   #url 링크가 나옴 https://www.donga.com/news/Society/article/all/20261022/134888448/1 이런식
    
    try:
        source_article = urllib.request.urlopen(article_url) #각각의 기사를 들어가기
        soup2 = BeautifulSoup(source_article,'lxml',from_encoding='utf-8')
        # print(soup2)
        contents = soup2.select("div.article_txt")   #div 태그의 article_txt 를 가지고온다
        # print(contents)
        for imsi in contents:  #string만 뽑아오기 
            item = str(imsi.find_all(string=True))
            msg += item
    except Exception as e:
        pass

    print(msg)

## 찬우 코드===============================

    okt=Okt()
    nouns=okt.nouns(msg)
    result=[]
    for n in nouns:
        if len(n)>1:
            result.append(n) # 두글자 이상의 단어만 저장
print(result[:20])

count=Counter(result) # 단어별 빈도 수
# print(count)
tag=count.most_common(50) # 가장 많이 나온 단어 50개
print(tag)

# 워드 클라우드
taglist =pytagcloud.make_tags(tag,maxsize=100)
print("taglist 출력",taglist,'\n') #.... {'color': (207, 137, 168), 'size': 49, 'tag': '여행지'}] 
print(len(taglist))
pytagcloud.create_tag_image(taglist, "nlp_word.png",
                            size=(1000,600),background=(0,0,0), fontname="korean", rectangular=False)
img=mpimg.imread("nlp_word.png")
plt.imshow(img)
plt.show()

#webbrowser.open("nlp_word.png")
print("===============")
df=pd.DataFrame(count.items(),columns=["단어","빈도수"])
print(df.head())

if not df.empty:
    print("\n 빈도수 기준 내림차순 정렬")
    df=df.sort_values(by="빈도수", ascending=False)
    df=df.reset_index(drop=True)
    print(df.head())

    print("\nPandas 기초 통계 : \n", df["빈도수"].describe())
    print("\n Numpy 기초 통계 : ")
    freq=df["빈도수"].to_numpy()
    print("전체 단어 출현 횟수 : ",np.sum(freq))
    print("평균 빈도수 : ",np.mean(freq))
    print("표준 편차 : ",np.std(freq),'\n')

    print("상위 단어 10개로 막대 그래프 : ")
    top10=df.head(10).sort_values(by="빈도수")
    plt.figure(figsize=(10,6))
    plt.barh(top10["단어"], top10["빈도수"])
    plt.xlabel("단어")
    plt.ylabel("빈도수")
    plt.show()

    df.to_csv("nlp_freq.csv",index=False,encoding='utf-8')
else:
    print("해석할 문장 데이터가 없다.")