from abc import ABC, abstractmethod
class Employee(ABC):
    name='이름'
    age='나이'
    def __init__(self,name,age):
        self.name=name
        self.age=age

    @abstractmethod
    def abstract_pay(self): #추상 메서드
        pass
    @abstractmethod
    def abstract_data_print(self):#추상 메서드
        pass

    def name_age_print(self):
        #def name_age_print(self,name,age):
        #=>TypeError: Employee.name_age_print() missing 2 required positional arguments: 'name' and 'age'
        #같은 클래스의 멤버변수에 저장된 것을 불러오기 때문에
        # 같은 클래스 내부 메서드의 인자에, 다른 클래스로 생성된 객체의 인자를 넣지 말아라 (Y/N)
        #print("=====Employee 클래스의 name_age_print() 출력===== ")
        print("이름:",self.name,"나이: ",self.age)
        print()

#일용직 직원 클래스
class Temporary(Employee): #Employee를 상속받는다. 추상 메서드인 abstract_pay(),abstract_data_print()를 반드시 오버라이딩 할 것
    def abstract_pay(self): #("=====Temp에서 실행하는 abstract_pay 오버라이딩=====")
        return self.day*self.pay
    def abstract_data_print(self): #("=====Temp에서 실행하는 abstract_data_print 오버라이딩=====")
        print(f'월급: {self.abstract_pay()}')

    def __init__(self, name, age, day, pay): #이름 나이 근무일수 일당\
        super().__init__(name,age)    
        self.day=day
        self.pay=pay 
        ##Temporary()클래스로 생성한 객체 x에 입력한 이름 나이 근무일수 일당을 객체의 고유 공간에 저장       
    def temShow(self):
        print("=====self.abstract_pay()     ||      self.abstract_data_print()출력=====")
        self.abstract_pay() #생성된 객체 고유에 저장된 abstract_pay()
        self.abstract_data_print() #생성된 객체 고유에 저장된 abstract_data_print()
        print("=====Tempory에서 받은 이름 나이 일수 일당 출력=====\n",self.name,self.age,self.day,self.pay)

#일용직 직원 클래스
class Regular(Employee): #Employee를 상속받는다. 추상 메서드인 abstract_pay(),abstract_data_print()를 반드시 오버라이딩 할 것
    def abstract_pay(self):#("=====Regular에서 실행하는 abstract_pay 오버라이딩=====")
        return self.salary
    def abstract_data_print(self):#("=====Regular에서 실행하는 abstract_data_print 오버라이딩=====")
       print(f'급여: {self.abstract_pay()}')

    def __init__(self, name, age, salary): #이름 나이 급여\
        super().__init__(name,age)
        self.salary=salary
       
        ##Regular()클래스로 생성한 객체 x에 입력한 이름 나이 월급을 객체의 고유 공간에 저장       
    def temShow(self):
        print("=====self.abstract_pay()     ||      self.abstract_data_print()출력=====")
        self.abstract_pay() #생성된 객체 고유에 저장된 abstract_pay()
        self.abstract_data_print() #생성된 객체 고유에 저장된 abstract_data_print()
        print("=====Regular에서 받은 이름 나이 월급 출력=====\n",self.name,self.age,self.salary)

#영업직 직원 클래스
class Salesman(Regular,Employee): #Regular와 Employee를 상속받는다. Regular()를 우선적으로 받는다
    sales=0 #실적 건수
    commision=0 #수수료율

    def abstract_pay(self):#=====Salesman에서 실행하는 abstract_pay 오버라이딩=====
        return self.salary+(self.sales*self.commision)
    def abstract_data_print(self):#=====Salesman에서 실행하는 abstract_data_print 오버라이딩=====
        print(f'급여: {self.abstract_pay()}')

    def __init__(self, name, age, salary, sales,commision): #이름 나이 근무일수 일당\
        super().__init__(name,age,salary) #Regular()가 맞선임이라 Regular()에게 전달해준다.
        #self.salary=salary #기본급 # 혼자 힘으로 디버깅 성공 => salary는 Regular에서도 사용하기 때문에 이름,나이와 같이 올린다
        self.sales=sales #판매건수 입력 해주기
        self.commision=commision# 수수료율
        ##Regular()클래스로 생성한 객체 x에 입력한 이름 나이 기본급 판매건수 수수료율을 객체의 고유 공간에 저장     
        
    def temShow(self):
        print("=====self.abstract_pay()     ||      self.abstract_data_print()출력=====")
        self.abstract_pay() #생성된 객체 고유에 저장된 abstract_pay()
        self.abstract_data_print() #생성된 객체 고유에 저장된 abstract_data_print()
        print()
        print("=====Sales에서 받은 이름 나이 기본급 판매건수 수수료율 출력=====\n",self.name,self.age,self.salary)
        print()
        print("=====실제 SalesMan의 이름 나이 실수령액 출력=====\n",self.name,self.age,self.abstract_pay())
        print()


t=Temporary("서지범",27,8,10000)
t.name_age_print()
t.temShow()

r=Regular("김나박이",28,3000000)
r.name_age_print()
r.temShow()

s=Salesman("최무선",29,2000000,20,0.25)
s.name_age_print()
s.temShow()

print('\n\n\n')
print("=====나 혼자 다형성 구현해보기=====")

#다형성 구현방식 1 #권장하지 않음 -> 너무 길어짐
many=t
many.name_age_print()
many=r
many.name_age_print()
many=s
many.name_age_print()

#다형성 구현방식 2 # 권장 방식 -> 훨씬 편함
employees = [t, r, s]
for emp in employees:
    emp.name_age_print()

# many=t
# many=r
# many=s
# many.name_age_print()
# many.name_age_print()
# many.name_age_print()
# =====나 혼자 다형성 구현해보기=====
# =====Employee 클래스의 name_age_print() 출력===== 
# 이름: 박 나이:  29

# =====Employee 클래스의 name_age_print() 출력===== 
# 이름: 박 나이:  29

# =====Employee 클래스의 name_age_print() 출력===== 
# 이름: 박 나이:  29

#이러면 맨 마지막 s에만 저장이 되니까 이따구로 하지말고 한줄씩 선언해라