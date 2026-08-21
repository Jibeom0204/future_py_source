"""
현재 모듈은 다른 package에 있는 모듈의 멤버(함수, 변수 등등)를 사용하여
실행을 통해 어떤 결과를 확인할 수 있는 실행파일

실행파일 => python 파일명.py   <== 이 파일은 main module
"""

print("사용자 정의 모듈 작성 후 호출 연습")
imsi =100 #뭔가 하는중
print('\n경로 지정 방법 1 : import 모듈명')
import pack1.mymod1
print('사용 가능 모듈의 목록:',dir(pack1.mymod1)) #사용 가능 모듈의 목록
print()
print('#경로 및 파일명 확인하기:',dir(pack1.mymod1.__file__)) #경로 및 파일 명 확인하기
print()
print('#모듈명 확인하기:',dir(pack1.mymod1.__name__)) #모듈명 확인하기
print()
#

list1 = [2,3]
list2 = [3,4,5]

print("패키지 호출해서 연산함: ",pack1.mymod1.listHap(list1,list2)) ##listHap = mod1에 들어가 있음  *ar로 호출해서 여러개 받음
#if __name__ == '__main__': 이거 실행 X
if __name__ == '__main__':
        print("나는 메인모듈이다")

##지금 test14가 메인 모듈이라
# if __name__ == '__main__':
#        print("나는 메인모듈이다")
#출력 가능

##mod1.py는 메인모듈이 아니라 그냥 함수들 모여 있는 모듈이라 메인모듈로 인식이 안됨
# if __name__ == '__main__':
#         print("나는 메인모듈이다")
# 그래서 이거 mod1 그냥 호출했을 때는 이거 출력이 안됨


###############################################################
print('\n경로 지정 방법 2 : from 모듈명 import 모듈멤버')
from pack1.mymod1 import kbsF  #사용할 kbsF만 불러오기
kbsF() # kbs 모듈 실행해서 그 안에 있는 함수들도 실행 ##kbs()자체가 함수임
#1박 2일

from pack1.mymod1 import mbcF,tot #사용할 mbcF,tot만 불러오기
mbcF()
print("tot 실행: ", tot)


####권장하지 않는 방법####
from pack1.mymod1 import * ##메모리 낭비가 심함


from pack1.mymod1 import kbsF as 케이비에스별명 ##메모리 낭비가 심함
print("패키지의 별명을 지정 가능, 별명은 케이비에스별명 : ",케이비에스별명())
##패키지의 별명을 지정 가능, 별명은 케이비에스별명 :  None => 왜 결과 none이 나오지?
###############################################################
 
###############################################################
print('\n경로 지정 방법 3 : import 하위패키지(여기서는 "subpack").모듈명.멤버')
import pack1.subpack.sbs
print("경로 3번 방법으로 호출해서 sbsF()실행")
pack1.subpack.sbs.sbsF()


### 별명 추가
import pack1.subpack.sbs as 에스비에스별명  ##이건 페키지의 경로에 대해 별명 부여
에스비에스별명.sbsF() #별명으로 경로 호출하고 함수 호츌
###############################################################

from pack1_other import mymod2
imsi = mymod2.Hap(3,4) #imsi 변수 미리 초기화한 값에 덮어 씌우기?
print(imsi)

from pack1_other.mymod2 import Cha as 빼기
print(빼기(10,1))
###############################################################

###############################################################
##lib 폴더는 path 설정이 되어있어서 패키지 호출을 따로 안해도 된다
##path 설정이 안되어 있는것들은 다 경로명 찍어야함
print('\n경로 지정 방법 4 : path설정이 된 폴더에 모듈이 저장된 경우')
#C:\Users\acorn\anaconda3\envs\myproject\lib\mymod3
import mymod3
print("mymod3 불러와 곱 연산 수행: ", mymod3.Gop(3,5))
###############################################################

import numpy
print(numpy.mean([3,5,7,9]))