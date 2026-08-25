"""
다형성 퀴즈
"""
class ElecProduct: #부모 클래스
    volume =0
    def volumeControl(self):
        print("이건 부모 클래스의 volumeControl")
        

#자식 클래스
#################################################
class ElecTV(ElecProduct):
    def Tv(self):
                print("무한도전") # 이건 그냥 실행되는 알림

    def volumeControl(self): #ElecProduct()클래스에 만들어진 volumeControl()과 이름은 같지만 기능은 다른 오버라이딩
        print("텔레파시 특집")
        
    
#################################################

#################################################
class ElecRadio(ElecProduct):
    def Rad(self):
        print("하하의 슈퍼라디오")

    def volumeControl(self):
        print("이무진 서비스")
        
#################################################

def volumeControl(volumeAddr):
    volumeAddr.volumeControl() #순서1-3== volumeAddr 인자로 넘겨받은 tv의 주소값에 저장된 상위 클래스의 메서드인 volumeControl() 호출
    # 각 자식 클래스의 이름으로 선언된 객체안에 있는 ElecProduct()클래스의 volumeControll()메서드를 호출함
    print("부모 클래스의volumeControl() 메서드 호출")
    print()


#################################################
if __name__ =="__main__":
    tv=ElecTV()  #순서 1-1== #Tv객체 생성
    rad=ElecRadio()#라디오 객체 생성
    origin=ElecProduct()

    #함수에다가 각 객체의 주소 넣어주기
    volumeControl(tv) ##순서 1-2== volumeControl() 함수의 인자 volumeAddr에 tv를 넣어줌
    #Tv 넣고 함수에서 Tv 객체안에 있는 ElecProduct()클래스의 volumeControll()메서드를 호출함
    volumeControl(rad)
    volumeControl(origin)