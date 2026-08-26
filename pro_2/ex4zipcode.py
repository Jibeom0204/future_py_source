### 우편정보 파일 자료 읽기
### 키보드에서 입력한 동이름으로 해당 주소 정보 출력

def zipProcess():
    dongIrum = input('동 이름 입력: ')
    print(dongIrum)

    # dongIrum='중계동'
    with open(r'zipcode.txt', mode='r',encoding='utf-8')as f:

        # line = f.read() #전체 행 읽기
        line = f.readline() #한행 읽기
        #print(line) # 135-806 서울    강남구  개포1동 경남아파트

        # 주소 문자열 자르기
        # lines = line.split('\t')#tab으로 구분#['135-806', '서울', '강남구', '개포1동 경남아파트', '', '1\n']
        # #split()dptj \t 을 써서 탭을 기준으로 잘라서 리스트로 반환

        # lines=line.split(chr(9)) #\t 말고 아스키코드(10진수)로 tap을 나타내는 chr(9)으로 자르기
        # ['135-806', '서울', '강남구', '개포1동 경남아파트', '', '1\n']
        # print(lines) 

        while line:
            lines=line.split(chr(9))
            if lines[3].startswith(dongIrum):
                #print(lines)
                print(f'우:{lines[0]} {lines[1]} {lines[2]} {lines[3]}')

            line = f.readline()

if __name__ =='__main__':
    zipProcess()