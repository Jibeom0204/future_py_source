"""
어떤 데이터와 그 데이터를 철하는 기능이 서로 밀접하게 관련되어 있다면 하나로 묵어 처리할 수 있다.
이를 클래스로 구현 가능하다.

1. 두 점의 거리를 계산하기
- 좌표의 거리와 기울기는 단순한 수학 연ㅅ브이 아니라 나중에 에 머신러닝 작업시 등장
거리는 나중에 KNN k-means embedding 유사도 등과 연결됨
2. 기울기
- 기울기는 선형회귀를 거쳐 미분, Gradient Descent 딥러닝의 학습 원리로 연결됨
3. 로그처리
첨도, 왜도가 큰 데이터 등 편차가 큰 데이터를 로그 변환하면 분포개선 머위차이 축소등으로 인해 모델을 안정적으로 수행가능
-> 핵심: 큰 수를 작은 수로 압축 => 복잡한 연산을 단순화 시킴, 편향된 데이터를 보정해 데이터 정규성을 확보
"""

"""
두 점 사이 거리계산
"""

import math

class Calctest:

    def __init__(self, x1,y1,x2,y2, offset:float=1.0):#생성자 만들기 + 두점의 좌표 얻기
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2

        #로그는 0과 음수를 허용하지 않음으로 offset으로 초기값을 주어 대처함
        self.offset =offset
        #offset:float=1.0 => 3번 로그 풀 때 추가했음. 1,2번 할 때는 없었음

    #1. 두점 사이의 거리(유클리드 거리 계산식) a²+b² =c²
    #피타고라스 정리에 따라 두 점 사이의 직선 거리가 직각삼각형의 빗변이 된다.
    def distance(self):
        dx=self.x2-self.x1
        dy=self.y2-self.y1
        return math.sqrt(dx**2+dy**2)
    
    #2. 두 점 사이의 기울기(y 변화량 / x의 변화량)
    def slope(self):
        dx=self.x2 -self.x1
        dy=self.y2 -self.y1

        if dx ==0: #기울기 못구하니까 에러처리
            return None
        return dy/dx

    #3. 로그값 구하기
    def transform(self, x_list:list[float]): #로그 변환
        return [math.log(x+self.offset) for x in x_list] # 받는  x가 얼마인지는 몰라도 offset을 줘서 0과 음수를 방지하고 받은 x_list 수를 for로 계속 꺼냄

    def inverse_transe(self, x_list:list[float]): # 역변환
        return [math.exp(x_log)-self.offset for x_log in x_list]


def main():
    #1. 두점 사이의 거리
    ctest = Calctest(1,2,4,6) #Calctest의 클래스 형태를 딴 ctest라는 객체 생성.  1 2 4 6을 입력해서 값을 넘겨주기 -> self 다시 공부
    print('두 점 사이의 거리 : ', ctest.distance()) #객체ctest에 대해.으로 클래스내의 distance  호출 -> 이 개념이 맞나?(Y/N)
    ##두 점 사이의 거리 :  5.0
    print()

    #2. 두 점 사이의 기울기
    print('두 점 사이의 기울기 : ', ctest.slope())
    ##두 점 사이의 기울기 :  1.3333333333333333
    print()

    #3. 로그처리
    data = [10.0,100.0,1000.0,10000.,] #x_list[]에 넘겨줄 값들 // dp: 편차가 큰 자료들

    #3-1로그 변환 및 역변환
    # 거리,기울기,로그를 수행할 수 있는 기능들로 구성된 선언된 클래스를 바탕으로 ctest 객체가 만들어짐. 그 객체를 부르고 그 안에 기능을 .transform으로 불러옴
    data_log_scaled = ctest.transform(data) #위에 "data"를 넣어줌  => 그럼 self로 넘어감?
    print('원본 자료 : ', data)
    print('로그 변환 자료 : ', data_log_scaled)
    print()

    revese_data = ctest.inverse_transe(data_log_scaled)
    revese_data_round = [round(val,1) for val in revese_data]
    print('역변환 자료 : ', revese_data)
    print('반올림 역변환 자료 : ', revese_data_round)
    print()
        


if __name__=="__main__": #모듈의 이름이 메인이면
    main() #메인 함수 실행 => 여기서는 저 계산식 들어있는 함수가 main으로 선언되어서 저거 실행함