# """
# 입력자료는 키보드 사용
# 커피는 한잔에 200원 
# 100원 넣고 커피 요구하면 부족 메세지
# 400원 넣고 2잔 요구하면 두잔 출력
# 500원 넣고 1잔 요구하면 300원 반납

# 출력 형태===
# 동전 입력: 
# 몇잔 원하세요? : 
# 커피 n잔과 잔돈 n원 

# machine 클래스
# CoinIn 클래스
# """

# class CoinIn:
#     coin=int
#     change:int
#     cupCount:int

#     def __init__(self, coin, cupCount):
#         self.coin=coin
#         self.cupCount=cupCount
#         self.change=0
#     ######Machin에서 값을 넘겨 받기#######

#     def cal(self,coin,cupCount):
#         if coin<cupCount*200:
#             print("요금이 부족합니다.")
#         else:
#             self.change=coin-(cupCount*200) #거스름돈=받은금액-주문수*커피금액(200)
#             print(f'커피'+str(cupCount)+'잔과'+'잔돈'+str(self.change)+'원')
        
#         return self.change

# class Machine:
   
#     def showData(self): 
#          #class CoinIn에 변수를 넘겨주기
#         mcoin=int(input("동전을 입력하세요: "))
#         mcupCount=int(input("몇잔을 원합니까?"))
            
#         need=CoinIn(coin=mcoin,cupCount=mcupCount).cal(mcoin, mcupCount)
       
#         #print(f'커피'+str(mcupCount)+'잔과'+'잔돈'+str(need)+'원')
#         return

# if __name__ == '__main__':
#     order = Machine()
#     order.showData()


"""
문제 2:  가채점 판독기
여러 개의 데이터를 한 번에 입력받아 복합적인 조건(평균 및 과락)을 통과하는지 판별하는 프로그램입니다. 매개변수가 늘어났을 때 클래스 간 데이터를 어떻게 넘길지 고민해 볼 수 있습니다.

[조건 사항]
국어 영어 수학 구축 세 과목의 점수를 각각 입력받습니다.
합격 기준은 세 과목 평균 60점 이상이며, 동시에 단일 과목 중 40점 미만이 없어야 합니다.
평균 60점 이상이더라도 한 과목이라도 40점 미만이면 최종 결과를 "불합격 (과락 발생)"으로 처리합니다.

[출력 형태]
1과목 점수 입력:
2과목 점수 입력:
3과목 점수 입력:
평균 점수: n점
최종 결과: 합격 (또는 불합격)

요구 클래스
ScoreValidator 클래스: 세 과목 점수를 받아 평균을 계산하고, 합격 여부를 boolean(True/False) 또는 문자열로 반환하는 역할
ExamSystem 클래스: 점수를 입력받고 ScoreValidator를 호출해 결과 텍스트를 구성하는 역할
"""

class ScoreValidator:#세 과목 점수를 받아 평균을 계산하고, 합격 여부를 boolean(True/False) 또는 문자열로 반환하는 역할
    kor=0
    eng=0
    math=0

class ExamSystem: #점수를 입력받고 ScoreValidator를 호출해 결과 텍스트를 구성하는 역할
    
    def scoreInput(self,kor, eng, math):
        print(input("국어 점수를 입력하시오: "))
        print(input("영어 점수를 입력하시오: "))
        print(input("수학 점수를 입력하시오: "))


if __name__ == '__main__':
    subject = ExamSystem()
    #test23처럼 클래스에 들어갈 인자값을 직접 줘도 괜찮다.
    #하지만 직접 입력을 하는 거면 클래스 안에 입력 가능한 코드를 작성하고 객체를 생성해서 인자를 별도로 입력받는다



    
  



