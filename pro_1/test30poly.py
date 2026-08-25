"""
메서드 오버라이딩을 통한 polymorphism(다형성) 구현
카드결제, 현금결제 ,포인트 결제 클래스에서 결제 메서드를 오버라이딩 하기
이거 UML로 그림 그려보기
"""

class Payment: #부모 클래스 : 결제라는 공통 기능 pay()를 정의
    def pay(self,amount):
        print(f"{amount}원 결제를 진행함")
        #pass #내용 없이 만들 수도 있음

#이하 자식 클래스
class CardP(Payment):  #Payment 클래스를 상속받는 자녀 클래스: 카드 수수료 2%를 계산하여 결제
    def abc():
        print("CardP 클래스의 고유 메서드")

    def pay(self, amount): #Payment()클래스의 pay메서드를 메서드 오버라이드 -> 강요는 아님. 선택적
        fee = amount*0.02
        total = amount +fee
        print(f"[카드결제]")
        print(f"상품 금액: {amount}원")
        print(f"수수료: {fee}원")
        print(f"최종 결제 금액: {total}원")
class CashP(Payment): #현금 결제 클래스 #현금으로 결제하면 할인 5%
    def pay(self, amount):
        discount = amount*0.05
        total = amount - discount
        print(f"[현금결제]")
        print(f"상품 금액: {amount}원")
        print(f"할인 금액: {discount}원")
        print(f"최종 결제 금액: {total}원")
class PointP(Payment): #포인트 결제 클래스: 금액만큼 포인트를 사용
    def pay(self, amount):
        print(f"[포인트결제]")
        print(f"{amount} 포인트를 사용함")

#클래스 공통처리 함수: 전달 받은 객체의 pay()를 호출
def process_payment(paymentAddr:Payment,amount:int): #payment와 ints는 넘겨받는 실인수의 타입에 대한 힌트만 나타냄. 없어도 무관
    #이 함수를 호출할때 넘겨주는 값 2개를 payment와 amount라는 가인수로 받응
    paymentAddr.pay(amount) #넘겨 받은 인자를 함수 내부의 변수 paymentAddr와 amount로 저장? paymentAddr2 amount2이런식으로 쓰면 안되나? 이건 실인수의 이름이 달라도 되는 부분인가?
    #paymentAddr의 넘겨 받은 카드,현금,포인트 결제 클래스로 생성된 각 객체들의 주소 안에 저장된 pay()메서드를 실행함
    #각 pay()메서드는 이름은 같지만 클래스별 선언된 내부 멤버들이 다르다

if __name__ =="__main__":
    p1=CardP()
    p2=CashP()
    #p3=PointP()

    process_payment(p1,10000) #process_payment()함수에 카드,현금,포인트 결제 클래스로 생성된 각 객체들의 주소를 인수로 넘겨줌
    print()
    process_payment(p2,10000)
    print()
    process_payment(PointP(),10000) #47줄 대신 이렇게도 사용 가능
