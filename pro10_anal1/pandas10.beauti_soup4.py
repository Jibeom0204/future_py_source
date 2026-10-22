# beautifulSoup 객체를 이용한 문서(HTML,XML) 처리
import requests
from bs4 import BeautifulSoup

baseurl="https://www.naver.com/"
headers={"User-Agent":"Mozilla/5.0"}

source=requests.get(baseurl,headers=headers)

print(source,type(source)) # <Response [200]> <class 'requests.models.Response'>
print(source.status_code) # 200
# print(source.text, type(source.text)) #.....bute("placeholder",l)}}()</script> </body> </html>  <class 'str'>
# print(source.content) # 이 내용들은 의미가 없는 값들 -> 안의 내용들을 beautiful 객체로 받아서 정제해야함

conv_data=BeautifulSoup(source.text,'html.parser')
print(conv_data,type(conv_data)) # ...",l)}}()</script> </body> </html>  <class 'bs4.BeautifulSoup'>

for atag in conv_data.find_all("a"): # BEAUTIFUL SOUP 객체로 받은 웹 정보들의 a태그만 추출
    href=atag.get("href")
    title=atag.get_text(strip=True)
    if title:
        print("href",href,'/n')
        print("title",title,'/n')
        print("==========",'/n')
# href #topAsideButton /n
# title 상단영역 바로가기 /n
# ========== /n
# href #shortcutArea /n
# title 서비스 메뉴 바로가기 /n
# ========== /n