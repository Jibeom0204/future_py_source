"""
연습과제 선생님 풀이
"""

class CoinIn():
    def __init__(self):
        price=200

    def calc(self ,coint,cupCount):
        totalPrice=self.cupPrice*cupCount #self.cupPrice=멤버변수 cupCount지역변수

        if coin<totalPrice:
            return None,None
        else:
            change =coin-totalPrice
            return cupCount,change

class Machine():
    def __init__(self):
        self.coinIn=CoinIn()

    def showData(self):
        coin = int(input("동전을 입력하세요: "))
        cup = int(input("몇잔을 원하세요: "))
        cupCount, change= self.coinIn.calc(coin,cup)

        if cupCount is None:
            print('요금이 부족')
        else:
            print(f'커피 {cupCount}잔과 잔돈 {change}원')

if __name__=="__main__":
    # machine= Machine()
    # machine.showData()
    Machine().showData() # 위의 두줄과 같은 기능의 코드