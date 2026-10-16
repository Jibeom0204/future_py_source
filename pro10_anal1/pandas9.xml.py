# Pandas는 URL을 이용해 웹상의 csv 파일인 HTML표 데이터를 DataFrame으로 읽기 가능
# XML은 데이터를 태그 형태로 구조화 해서 저장 전송하느 문서 형식
# 
import xml.etree.ElementTree as etree

xmlfile=etree.parse("pandas9.my.xml")
print("XML 출력\n",xmlfile,'\n')

root=xmlfile.getroot()
print(root.tag) #items
print(root[0].tag) #item
print(root[0][0].tag) #name

myname=root.find('item').find("name").text

mytel=root.find('item').find("tel").text
print(myname+' '+mytel)

print("\n===============기상청 제공 xml 자료 읽기===============\n")
import requests
url="https://www.kma.go.kr/XML/weather/sfc_web_map.xml"
headers={"User-Agent":"Mozila/5.0"}

res=requests.get(url,headers=headers)
res.raise_for_status()
print(res.text,type(res.text)) #... <class 'str'>


root=etree.fromstring(res.text)
print(root)

# xml 파일에서 <current xmlns="current">같은 네임스페이스 제거하기
for elem in root.iter():
    if '}' in elem.tag: #태그에 }가 있으면
        elem.tag=elem.tag.split('}',1)[1] # 1번째 자리에서 }를 기준으로 잘라 태그명만 남김
        #{current}weather -> weather
weather=root.find("weather")
year=weather.get('year')
month=weather.get('month')
day=weather.get('day')
hour=weather.get('hour')

print(f"{year}년 {month}월, {day}일, {hour}시 현재 예보")

# 각 지역 순회
for local in weather.findall("local"): # local 태그 달린거 모두?? 맞나?
    name=local.text.strip() # 지역명(태그 안에 문자열)
    ta =local.get("desc") # 온도(요소의 ta 속성값)
    print(f"{name} 지역 온도는 {ta}")