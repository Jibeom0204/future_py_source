class Singer:
    print("Singer 클래스 원형에서 나옴")
    print("")
    title_song = "애국가" #이게 필드라고?

    def sing(self):
        print("sing 함수에서 나옴")
        msg="노래는"
        print(msg, self.title_song)

class Etc:
    pass

"""
여러개의 클래스나 함수 등을 선언하고 다른 파일에서 공유하도록 설정함
"""