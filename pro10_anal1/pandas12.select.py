# css 셀렉터를 이용
from bs4 import BeautifulSoup

html_page="""
<html><body>

<div id="hello">
    <a href="https://www.naver.com"> naver </a><br/>

    <span>
    <a href="https://www.daum.net"> daum </a><br/>
    </span>

    <ul class="world">
    <li>ㅎㅇ</li>
    <li>ㅂㅇㅂㅇ</li>
    </ul>
</div>
<div id="hi" class="good">
    두번째 div
</div>
</body></html>
"""

soup=BeautifulSoup(html_page,"html.parser")
# aa=soup.select_one("div") # body 영역 내 div 태그 중 제일 첫번째
# aa=soup.select_one("div#hello")
aa=soup.select_one("div.good")
aa=soup.select_one("div#hello>a") # div의 직계 a 태그 중 첫번째 요소 검색
print("aa와 aa.string: ","aa : ",aa," ",aa.string,'\n')
# ....<li>ㅂㅇㅂㅇ</li>
# </ul>
# </div>

# bb=soup.select("div") # 반환값이 복수
# bb=soup.select("div#hello>ul.world") # 직계
#bb=soup.select("div#hello ul.world") # 자손
bb=soup.select("div#hello ul.world>li") # div의 hello 태그 자손 중 ul. ul의 world 클래스의 직계인 li
# > 있으면 직계 없으면 자손
print("bb: \n",bb) #[<div id="hello">]
for i in bb:
    print(i, " ",i.text)

# bb=soup.select("div") # 반환값이 복수
#     <div class="good" id="hi">
#     두번째 div
# </div>   
#     두번째 div

# bb=soup.select("div#hello>ul.world") # 직계
# bb: 
#  [<ul class="world">
# <li>ㅎㅇ</li>
# <li>ㅂㅇㅂㅇ</li>
# </ul>]
# <ul class="world">
# <li>ㅎㅇ</li>
# <li>ㅂㅇㅂㅇ</li>
# </ul>   
# ㅎㅇ
# ㅂㅇㅂㅇ

# bb=soup.select("div#hello ul.world") # 자손
# bb: 
#  [<ul class="world">
# <li>ㅎㅇ</li>
# <li>ㅂㅇㅂㅇ</li>
# </ul>]
# <ul class="world">
# <li>ㅎㅇ</li>
# <li>ㅂㅇㅂㅇ</li>
# </ul>   
# ㅎㅇ
# ㅂㅇㅂㅇ

# #bb=soup.select("div#hello ul.world>li") # div의 hello 태그 자손 중 ul. ul의 world 클래스의 직계인 li
# bb: 
#  [<li>ㅎㅇ</li>, <li>ㅂㅇㅂㅇ</li>]
# <li>ㅎㅇ</li>   ㅎㅇ
# <li>ㅂㅇㅂㅇ</li>   ㅂㅇㅂㅇ


print("==================위키 백과 이순신 자료 읽기==============\n")
import requests
wiki_url="https://ko.wikipedia.org/wiki/%EC%9D%B4%EC%88%9C%EC%8B%A0"
headers={"User-Agent":"Mozilla/5.0"}
wiki=requests.get(url=wiki_url,headers=headers)
# print(wiki.text[:300])
soup=BeautifulSoup(wiki.text,"html.parser")
result=soup.select("p#mwIA")
# print(result)
for s in result:
    for sup in s.find_all("sup"):
        sup.decompose() # 태그 삭제 함수
    print(s.get_text(strip=True,separator="")) # 태그를 제외하고 텍스트만 추출(공백)




print("\n\n==================교촌 치킨사이트에서 메뉴, 가격 자료 읽기==============\n")
import pandas as pd
c_url="https://www.kyochon.com/menu/chicken.asp"
headers={"User-Agent":"Mozilla/5.0"}
kyochon=requests.get(url=c_url, headers=headers)
print(kyochon.text)
soup2=BeautifulSoup(kyochon.text,"html.parser")

# 메뉴명 얻기
names=soup2.select("dl.txt>dt")
# print(names)
prices=[int(tag.text.strip().replace(",",""))
         for tag in soup2.select("p.money strong")] #웹사이트에서 검사 도구로 확인 가능한 가격 자손 태그 strong
# print(prices)
df=pd.DataFrame({"상품명":names, "가격":prices})
print(df.head(3))
print(f"가격 평균: {df["가격"].mean():.2f}",'\n')
print(f"가격 표준편차: {df["가격"].std():.2f}",'\n')
# 변동계수(cv. 표준편차를 산술 평균으로 나눈 값): 상대적 변동성 파악
cv=df["가격"].std()/df["가격"].mean()*100
print(f"가격 변동계수(cv): {cv:.2f}%")
# 가격 변동계수(상대적인 산포 정도)(cv): 24.85%이므로 평균대비 적당히 퍼져있는 편


print("\n\n==================증권 URL 바당오기==============\n")
asset_url="https://stock.naver.com/market/stock/kr"
headers={"User-Agent":"Mozilla/5.0"}
asset=requests.get(url=asset_url,headers=headers)
print(asset.text)
# soup2=BeautifulSoup(kyochon.text,"html.parser")

class="stock-name-container"