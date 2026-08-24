"""
로또 번호 출력기
45개의 넘버링된 볼 객체 생성 후 섞고 난 후 6개의 공을 출력
"""
import random

class LottoBall:
    def __init__(self, num):
        self.num=num

class LottoMachine:
    def __init__(self):
        self.ballList = []
        for i in range(1,46):
            self.ballList.append(LottoBall(i)) # 클래스 포함관계 #위에서 선언한 LottoBall 가져오기

    def selectBalls(self):
        # for a in range(45):
        #     print(self.ballList[a].num,end =' ') 
        print('\n')
        random.shuffle(self.ballList) #볼 섞기
        # for a in range(45):
        #             print(self.ballList[a].num,end =' ')

        # print('여섯 개만 출력', self.ballList[0:45]) #num 안찍으면 6개 객체 주소만 나옴
        return self.ballList[0:6] #섞은 볼 중 6개만 리턴

class LottoUI:
    def __init__(self):
        self.machine = LottoMachine() #클래스 포함

    def playLotto(self):
        input ("로또를 시작하려면 엔터를 누르셈: ") #input으로 키를 받음 -> scanf()
        selectedballs=self.machine.selectBalls()
        #LottoMachine()으로 만들어진 machine. .으로 LottoMachine 안에 있는 selectBalls 호츌? 그걸 selectedBalls에 저장?(Y/N)
        for ball in selectedballs:
            print(ball.num)

if __name__ == '__main__':
    # machine =LottoMachine()
    # machine.selectBalls()
    lot = LottoUI() #lottoUI  객체 가지고 playLooto를 쓰기위함
    lot.playLotto()
    #LottoUI().playLotto()  #이거 위의 두줄 49,50줄이랑 같은 실행결과를 가지는 코드
