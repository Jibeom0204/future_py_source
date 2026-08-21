"""
클래스는 새로운 타입을 만들어 자원 공유가 목적
데이터(멤버 필드)와 기능(메서드)를 하나로 묶어 새로운 사용자 정의 타입을 만듬
객체마다 상태를 가지게 하거나 경우에 따라 공통 자원을 공유할 수 있다
"""

# class Singer:
#     print("Singer 클래스 원형에서 나옴")
#     print("")
#     title_song = "애국가" #이게 필드라고?

#     def sing(self):
#         print("sing 함수에서 나옴")
#         msg="노래는"
#         print(msg, self.title_song)


# ## 다르게 불러오는 방법
# ## 1번
# import test22singer
# bts =test22singer.Singer()
# ## 2번
from test22singer import Singer  #이걸로 다른 파일에 작성해놓은 클래스 호출 #외부 모듈의 멤버 로딩 -> 이 개념 모듈 복습해라

bts= Singer() #Singer 클래스를 가지는 bts 객체 생성
bts.sing()
print('bts의 타입 확인: ')
print(type(bts))
#########################################
print()
print("bts 다른 정보 입력")
bts.title_song ="작은 것들을 위한 시"
bts.co = '빅히트 엔터테이먼트'

print("bts 타이틀 곡")
bts.sing()
print("bts 소속사: ",bts.co)
#########################################
print()
print("=========다른 가수=========")
ive=Singer()#Singer 클래스를 가지는 ive 객체 생성
ive.sing()
print('ive의 타입 확인: ')
print(type(bts))
#print("bts 소속사: ",ive.co) #이건 따로 만들지도 않았으니 에러

#########################################
print()
print('타이틀곡 새로 선언')
print()
Singer.title_song = "뜨거운 여름밤은 가고"
print('아이브 노래')
ive.sing()
print()
print('bts 노래')
bts.sing()
#########################################

print()
niceGroup = ive #객체의 주소를 다른 변수에 담기 = 치환
print("niceGroup으로 새롭게 치환한 이름")
niceGroup.sing()