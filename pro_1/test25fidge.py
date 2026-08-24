"""
냉장고 객체에 음식 개체 저장
"""
class FoodData: #음식 객체(냉장고에 보관)
    #self.name=name #이걸 밖에 쓰면 프로토타입
    def __init__(self,name,expiry_date): #생성자로 이름과 유통기한 받기
        self.name = name # 음식이름 def안에 썼으니까 프로토 타입 아님 FoodData를 바탕으로 만든 객체 안에 들어감
        self.expiry_date = expiry_date

class Fridge:
    isOpened = False
    foods =[] # 음식 많으니까 리스트로\  #한 파일에서 외부에 생성할 클래스를 안으로 부름
#생성자 생략
    def open(self):
        self.isOpened=True
        print('냉장고 문이 열림')

    def close(self):
        self.isOpened =False
        print('냉장고 문이 닫힘')

    def foodList(self): #냉장고 문이 열린 경우 음식물 확인 메소드
        for f in self.foods:
            print(f" - {f.name} {f.expiry_date}")
        print()

    def put(self,thing):
        if self.isOpened:
            self.foods.append(thing)
            print(f"냉장고에 {thing.name} 넣음")
            self.foodList()
        else:
            print("냉장고 문이 닫혀있음")


fObj = Fridge() #냉장고 객체 생성
apple = FoodData("사과","2026-9-6") #FoodData의 생성자가 def __init__(self,name,expiry_date): 이거 이기에 name과 expiry_date에 들어갈 값을 넣어주고  apple 객체에 저장
fObj.put(apple) # put 하기 전이라 냉장고 문이 닫혀있음
#Fooddata()로 생성된 객체 apple이 Fridege()로 생성된 냉장고 객체 fObj()의 self로 전달되고 foods[] 리스트에 이름과 유통기한이 저장됨? (N -> 맨 아래 Gemini 해설)
fObj.open()
fObj.put(apple)
fObj.close()
print()

cola=FoodData('콜라','2027-5-5')
fObj.put(cola) # put 하기 전이라 냉장고 문이 닫혀있음
fObj.open()
fObj.put(cola)
fObj.close()
print()

"""
N (아닙니다. 주신 주어 설명 중 일부가 객체지향 개념과 실제 코드 동작과 다릅니다.)
근거 및 상세 설명

###self가 전달되는 대상의 오류
주석에서 apple 객체가 fObj()의 self로 전달된다고 하셨으나, self는 냉장고 객체 자신(fObj)을 가리키는 파라미터입니다.
파이썬에서 fObj.put(apple)을 호출하면, put 메서드의 self에는 fObj가 들어가고, thing 파라미터로 apple 객체가 전달됩니다.

###리스트에 저장되는 형태
foods[] 리스트에 이름과 유통기한이라는 문자열 데이터가 각각 따로 들어가는 것이 아니라, FoodData 객체 자체(apple 인스턴스)가 그대로 통째로 append()됩니다.
따라서 리스트 안에는 apple 객체가 들어가 있고, 나중에 f.name과 f.expiry_date 형태로 접근해서 그 안의 속성값을 가져오게 됩니다.

###올바른 동작 과정
fObj.put(apple)이 실행되면 thing이라는 이름으로 apple 객체가 전달됩니다.
self.isOpened가 참(True)일 때, self.foods.append(thing)에 의해 fObj의 foods 리스트에 apple 객체(참조값)가 추가됩니다.
이후 f.name, f.expiry_date를 통해 사과의 이름과 유통기한을 출력할 수 있게 됩니다.

(추측하건대, 객체가 통째로 리스트에 들어간다는 점과 self가 메서드를 호출한 객체 자신을 의미한다는 점을 헷갈리신 것으로 보입니다.)
"""

