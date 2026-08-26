"""
추상 클랫그를 사용해 다형성 = 배송관련(일반, 퀵, 직접수령)

공통규격(틀) 클래스 : 모든 배송 클래스는 '배송비를 가져야한다'라는 규칙
"""
from abc import ABC, abstractmethod

class Delivery(ABC):
    @abstractmethod
    def get_fee(self,distance):
        #pass
        return 0

class NormalDev(Delivery):  #일반 배송
    def get_fee(self, distance):
        return 3000 #기본 배송비 3000원

class QuickDev(Delivery):  #퀵 배송
    def get_fee(self, distance):
        return 3000 + distance*1000 #거리 당 비용까지 고려

class Pickup(Delivery):  #직접 수령
    def get_fee(self, distance):
        return 0 #배송비 없음

class DeliveryUtil: #어떤 배송 객체든 배송비 출력 담당
    def print_fee(delivery,distance):
        fee = delivery.get_fee(distance)
        print('배송방식 : ',  delivery.__class__.__name__)
        print('배송거리 : ',  distance,'km')
        print('배송요금 : ',  fee,'원')

c1=NormalDev()
c2=QuickDev()
c3=Pickup()

DeliveryUtil.print_fee(c1,5) #c1이 DeliveryUtil로 넘어가서 객체의 이름 c1,c2,c3가 'delivery'로, 5가 'distance'에 전달됨 
print()
DeliveryUtil.print_fee(c2,5)
print()
DeliveryUtil.print_fee(c3,5)
