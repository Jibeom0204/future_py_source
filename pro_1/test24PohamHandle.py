"""
핸들 클래스
어딘가엣 필요한 부품 - > 오토바이, 자동차, 자전거 등등..
"""

class PohamHandle:  #포함으로 쓰거나 상속으로 쓰거나 다 가능. 연습으로 포함으로 쓰자
    quantity=0 #핸들의 회전량 #클래스 내 전역변수. 다른 함수에서 사용 가능. 클래스의 프로토 타입

    def leftTurn(self,quantity):
        self.quantity=quantity
        return "좌회전"
    
    def rightTurn(self,quantity):
        self.quantity=quantity
        return "우회전"
