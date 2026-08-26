"""
직원 급여 계산 예제
직원이라는 개념은 있지만 실제 급여 계산은 정규직과 아르바이트가 서로 다르다.
"""

from abc import ABC, abstractmethod
# 직원들의 공통 규격을 정의하는 추상 클랫 
class Employee(ABC):
    def __init__(self,name):
        self.name=name #(self,name)을 통해서 받은 name을 저장할 수 있는 객체 주소의 고유의 것 - 입력받은이름.name

    @abstractmethod
    def get_salary(self): #자식 클래스가 만드시 구현해야 하는 메서드
        pass

    def show_salary(self):#모든 직원이 공용하는 일반 메소드
        print('이름: ',self.name)
        print('급여: ',self.get_salary(),'원') #클래스에 따라 다른 결과(다형성 활용)
        print()

#정규직
class FullTimeEmployee(Employee): #추상 클래스 부모를 상속 -> 오버라이딩 안하면 얘도 추상클래스로 바뀜
    def __init__(self, name, monthly_salary):
        super().__init__(name)
        self.montly_salary = monthly_salary #인스턴스 변수,만들어진 객체에 귀속됨 self.montly_salary에 입력한 montly_salary를 저장

    def get_salary(self): # 부모 클래스의 메서드 오버라이딩 # 자식 클래스마다 기능이 다르다 -> 오버라이딩
        return self.montly_salary # 급여를 개산할 필요가 없으니 입력받은 montly_salary를 그냥 반환한다

    def showMe(self):
        print('나는 정규직')

#아르바이트
class PartTimeEmployee(Employee): #추상 클래스 부모를 상속 -> 오버라이딩 안하면 얘도 추상클래스로 바뀜
    def __init__(self, name,hours, hourly_pay):
        super().__init__(name)
        self.hours = hours # 생성자는 이렇게 초기화만 하는 공간
        self.hourly_pay = hourly_pay #인스턴스 변수,만들어진 객체에 귀속됨 self.hourly_salary에 입력한 hourly_salary를 저장
        
    def get_salary(self):# 부모 클래스의 메서드 오버라이딩 # 자식 클래스마다 기능이 다르다 -> 오버라이딩
        return self.hours * self.hourly_pay # 근무 시간과 시급을 넘겨받아 총 급여를 반환한다


emp1 = FullTimeEmployee("홍길동", 3500000)
emp2 = PartTimeEmployee("한국인",80,10500) #알바 -> 이름, 근무시간, 시급


print()
print('=====정규직 emp1.show_salary=====')
emp1.show_salary() # FullTimeEmpoly()클래스로 생성된 객체 emp1에서 showsalary()메서드를 호출
#먼저 FullTimeEmpoly()클래스 내에서 찾고 없으니까 부모 클래스에서 찾아서 호출함

print()
print('=====알바생 emp2.show_salary=====')
emp2.show_salary()# PartTimeEmpoly()클래스로 생성된 객체 emp2에서 showsalary()메서드를 호출
#먼저 PartTimeEmpoly()클래스 내에서 찾고 없으니까 부모 클래스에서 찾아서 호출함

"""
추상 클래스를 사용하는 이유는 한마디로 하면
여러 자식 클래스가 반드시 가져야할 공통 규칙을 정하고
구현을 강제하기 위함
"""