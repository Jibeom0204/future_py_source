# beautifulSoup 객체 메소드 이해
import requests
from bs4 import BeautifulSoup

html_page="""
<html><body>

<h1> 제목 태그 </h1>
<p>웹 문서 연습</p>
<p>원하는 자료 읽기</p>

</body></html>
"""

print("html_page 타입)",type(html_page),'\n') # <class 'str'> 
soup=BeautifulSoup(html_page,'html.parser')
print('soup의 타입',type(soup),'\n') # <class 'bs4.BeautifulSoup'> 

h1=soup.html.body.h1
print("h1 : ",h1.string)
p1=soup.html.body.p #최초의 p태그
print("p1 : ",p1.string)
p2=p1.next_sibling.next_sibling # DOM을 이용한 접근
print("p2 : ",p2.string) # next.sibling 2개 써서 둘다 출력. 
# html > body >h=p --> h와p는 동일한 계급으로 서로 next_sibling과 previos_sibling의 관계를 가짐 

# p1 :  웹 문서 연습.
# p1의 next_sibling은 </p>의 >
# p1의 next_sibling의 next_siblingdms <p>원의 <이다

print('\n =====find() method 사용')
html_page2="""
<html><body>

<h1 id="title"> 제목 태그 </h1> <!-- 제목 <b>태그</b> 출력-->
<p>웹 문서 연습</p>
<p id="my" class="our">원하는 자료 확인</p>

</body></html>
"""
soup2=BeautifulSoup(html_page2,'html.parser')
#find(tag명, attrs, recursive, string) #recursive:자손태그
print(soup2.p,' ',soup2.p.string,'\n')
#soup2.p: 태그까지 같이 가져옴 => <p>웹 문서 연습</p>
#soup2.p.string: 내용만 가져옴 => 웹 문서 연습
print("find로 p태그 찾기:",soup2.find("p").string)
print("find로 h태그 찾기:",soup2.find(["p","h1"]).string) # 두 태그 중 먼저 나오는 태그 출력(단일 문자열 출력). h1을 뒤에 썼지만 h1 태그만 출력됨

print("find로 h태그 찾기:",soup2.find(["p","h1"]).get_text())
#get_text(): 하위 태그에 있는 텍스트까지 추출


print("find, id로 찾기:",soup2.find("p",id="my").string)
print("find, id로 찾기:",soup2.find(id="title").string)

print("find, class로 찾기:",soup2.find(class_="our").string)
print("find, class로 찾기:",soup2.find(attrs={"class":"our"}).string)
print("find, class로 찾기:",soup2.find(attrs={"id":"my"}).string)



print('\n =====find all() method 사용')
html_page3="""
<html><body>

<h1 id="title"> 제목 태그 </h1>
<p>웹 문서 연습3</p>
<p id="my" class="our">원하는 자료 확인</p>

<div>
    <a href="https://www.naver.com"> naver </a><br/>
    <a href="https://www.daum.net"> daum </a><br/>
</div>


</body></html>
"""
soup3=BeautifulSoup(html_page3,'html.parser')
print("a 태그 출력(링크들): \n",soup3.find_all(["a"]),'\n')
print("a태그 p태그 둘다 잡기. find는 둘중하나: \n",soup3.find_all(["a","p"]),'\n')
links=soup3.find_all("a")
print("links 출력 ",links,'\n')

for i in links:
    href=i.attrs["href"]
    text =i.text # i.string
    print(href," ",text)
    # https://www.naver.com    naver 
    # https://www.daum.net    daum 


print('\n =====정규 표현식 사용')
import re
links2=soup3.find_all(href=re.compile(r"^https"))
print("links2 출력: ",links2)
for k in links2:
    print(k.attrs["href"])

print('\n =====bugs 사이트 음악 순위 읽기')
import requests
url="https://music.bugs.co.kr/chart"
response=requests.get(url)
print(response.text)
bsoup=BeautifulSoup(response.text,'html.parser')
musics=bsoup.find_all("td",class_="check")
# print(musics)
for idx,music in enumerate(musics):
    print(f"{idx+1}위 {music.input["title"]}") # 인덱스 0이라 1로 시작하기