""" 
처리 조건 : 

1) 급여액은 기본급 + 근속수당 

2) 수령액은 급여액 – 공제액

근무년수에 대한 수당표	
근무년수     근속수당
0~3년        150000
4~8년        450000
9년 이상    1000000

급여 상한액에 대한 공제세율표
급여액                공제세율
300만원 이상          0.5
200만원 이상          0.3
200만원 미만          0.15

[사번, 이름, 기본급, 입사년도]는 기본으로 입력하고
[사번  이름    기본급    근무년수  근속수당  공제액    수령액]

출력해라
"""

# 입력 함수 :  [사번, 이름, 기본급, 입사년도]
def inputfunc():
    datas = [
        [1, "강나루", 1500000, 2010],
        [2, "이바다", 2200000, 2018],
        [3, "박하늘", 3200000, 2005],
        [4, "이성계", 2700000, 2011]
    ]
    return datas #리턴을 datas로 안해도 되나? 만약 return을 info로 바꾼다면 이후 코드에서 어떤걸 바꿔야 하나

def processfunc(datas):
    print('처리함수 영역')
    #datas라는 매개변수를 받음 이것은 가인수 나중에 실제로 시행하는 함수에 진짜 값을 넣어줌
    #processfunc(real_data) 이런식으로
    # print('processfunc()내에서 작동하는 출력, 값이 input에서 넘어왔는지 확인\n',datas)
    #필요한 값
    # num=0; name={}; basicS=0; workY=0;
    #사번  이름    기본급    근무년수는 제공
    #내가 구할 거 => 근속 수당 공제엑 수령액


    def yearSalary(year):  #근속 수당 구하기 #근속 연수 받아오기
        thisYear=2026
        #현재 연도 자동으로 가져오는 라이브러리가 있음 이런거 써라
        #from datetime
        #thisYear=datetime.now().year
        yearsalary=0
        if thisYear-year<=3:
            yearsalary=150000
        elif thisYear-year<=8:
            yearsalary=4500000
        else: 
            yearsalary=1000000
        return yearsalary

       
        
    for row in datas:
        num=row[0]
        name=row[1]
        basic=row[2]
        workYear=row[3]
    
        if row[0]==1:#강나루
            print('강나루',row)
            yearsalary=yearSalary(workYear)
            if basic+yearsalary >= 3000000:
                total=(basic+yearsalary)-((basic+yearsalary)*0.5) # 기본급 + 근속 수당 - 기본+근속 합에 따른 세금 차 
            elif basic+yearsalary >= 2000000:
                total=(basic+yearsalary)-((basic+yearsalary)*0.3)
            else:
                total=(basic+yearsalary)-((basic+yearsalary)*0.15)
            print('사번:',num, "이름: ",name, '기본급: ',basic, '입사년도: ',workYear, '근속수당', yearSalary(workYear), '수령액',total)
            print("이걸 조건문으로 시작하여 하나씩 출력하려고 했는데 이거 하나 출력하고 elif문에서 모든 사람이 출력이 된다. 로직에 무슨 문제가 있는거지?")
            
            # name='강나루'
            # basic=1500000
            # workYear=2010
            print("\n")

        elif row[0]==2:#이바다
            #  print('이바다',row)
            yearsalary=yearSalary(workYear)
        if basic+yearsalary >= 3000000:
            total=(basic+yearsalary)-((basic+yearsalary)*0.5) # 기본급 + 근속 수당 - 기본+근속 합에 따른 세금 차 
        elif basic+yearsalary >= 2000000:
            total=(basic+yearsalary)-((basic+yearsalary)*0.3)
        else:
            total=(basic+yearsalary)-((basic+yearsalary)*0.15)
        print("이 코드에서 다 실행됨")
        print('사번:',num, "이름: ",name, '기본급: ',basic, '입사년도: ',workYear, '근속수당', yearSalary(workYear), '수령액',total)
        
    
    # print("임의의 사람?",row)
    # # 여기서 datas는 함수 선언 할 때 말한 인자 값이라 가인수임
    # # 나중에 processfunc(real_datas)로 "함수를 실행"할 때 real_datas를 받을 수 있는 가인수임
    #     # print("사번: ",{num}, "이름: ",{name}, "기본급: ",{basicS}, "근무년수: ",{workY})
    
    




datas = inputfunc() #datas라는 변수에 inputfunc의 결과를 저장
print('최종출력: ',processfunc(datas))

    






# def processfunc(datas):
#     inputfunc()

#     #근속 연수별 근속수당 구하기
#     thisYear=2026 #현재 연도
#     enterYear=0 #입사년도
#     workingYear=thisYear-enterYear
#     totSalary=0 #근속 수당

#     #근속 연차별 근속 수당
#     junior_Year_Salary=150000
#     senior_Year_Salary=450000
#     veteran_Year_Salary=1000000
    
#     def workYear(): #근속 연수 구해서 근속 수당 금액 불러오기
#         if num == 1: #사원의 정보를 하나씩 떼오기 -> 분명 더 나은 방법이 있을 거임
#             enterYear= 2010 #입사년도
#             if thisYear-enterYear<=3:
#                 totSalary=salary+junior_Year_Salary
#             elif thisYear-enterYear<=8:
#                 totSalary=salary+senior_Year_Salary
#             else: 
#                 totSalary=salary+veteran_Year_Salary
#             return totSalary

#         elif num ==2:
#             enterYear= 2018
#             if thisYear-enterYear<=3:
#                 totSalary=salary+junior_Year_Salary
#             elif thisYear-enterYear<=8:
#                 totSalary=salary+senior_Year_Salary
#             else: 
#                 totSalary=salary+veteran_Year_Salary
#             return totSalary

#         elif num ==3:
#             enterYear= 2018
#             if thisYear-enterYear<=3:
#                 totSalary=salary+junior_Year_Salary
#             elif thisYear-enterYear<=8:
#                 totSalary=salary+senior_Year_Salary
#             else: 
#                 totSalary=salary+veteran_Year_Salary
#             return totSalary
#         else:
#              print('해당 사원 없음')



#     def realSalary():
#         workYear()
#         realsalary=0

#         if num == 1:
#             if totSalary < 2000000:
#                 totSalary=totSalary-(totSalary*0.15)
#             elif totSalary >= 2000000:
#                 totSalary=totSalary-(totSalary*0.3)
#             elif totSalary >= 3000000:
#                 totSalary=totSalary-(totSalary*0.5)
#             return realsalary

#         elif num==2:
#             if totSalary < 2000000:
#                 totSalary=totSalary-(totSalary*0.15)
#             elif totSalary >= 2000000:
#                 totSalary=totSalary-(totSalary*0.3)
#             elif totSalary >= 3000000:
#                 totSalary=totSalary-(totSalary*0.5)
#             return realsalary

#         elif num==3:
#             if totSalary < 2000000:
#                 totSalary=totSalary-(totSalary*0.15)
#             elif totSalary >= 2000000:
#                 totSalary=totSalary-(totSalary*0.3)
#             elif totSalary >= 3000000:
#                 totSalary=totSalary-(totSalary*0.5)
#             return realsalary
                
            
         
# print("|사번|   |이름|  |기본급|    |근속년수|  |근속수당|  |공제엑|    |실수령|")

# for num,name,salary,enterYear, totSalary, realsalary in processfunc():
#     print({num}, {name}, {salary},{enterYear},{totSalary},{realsalary})

# #타이핑해서 입력 받는거 아니다 그냥 내가 다 치는거다 쉽게 생각하자



# 교수님 풀이
# 문제 1 ---------------------------------
from datetime import datetime

# 직원 데이터 입력
def inputfunc():
    datas = [
        [1, "강나루", 1500000, 2010],
        [2, "이바다", 2200000, 2018],
        [3, "박하늘", 3200000, 2005],
    ]
    return datas


# 급여 처리
def processfunc(datas):
    # 현재 연도 자동으로 가져오기
    # current_year = datetime.now().year
    current_year = 2026

    # 직원별 급여 계산
    for data in datas:
        emp_no, name, base_pay, hire_year = data

        # 근무 연수 계산
        work_years = current_year - hire_year

        # 근속 수당 계산
        if work_years <= 3:
            bonus = 150000
        elif work_years <= 8:
            bonus = 450000
        else:
            bonus = 1000000

        # 총 급여
        salary = base_pay + bonus

        # 공제율 결정
        if salary >= 3000000:
            tax_rate = 0.5
        elif salary >= 2000000:
            tax_rate = 0.3
        else:
            tax_rate = 0.15

        # 공제액
        tax = int(salary * tax_rate)

        # 실수령액
        net_pay = salary - tax

        # 계산 결과 추가
        data.extend([  #extend를 사용해 만들어진 리스트에 항목을 추가한다
            work_years,
            bonus,
            tax,
            net_pay
        ])

    # 결과 출력
    print("사번  이름    기본급    근무년수  근속수당  공제액    수령액")
    print("-" * 70)

    for data in datas:
        print(
            f"{data[0]:<4} " #data[0]:<4 4칸 ㄸ=ㅢ우고 [0]값 출력
            f"{data[1]:<6} "
            f"{data[2]:<8} "
            f"{data[4]:<8} "
            f"{data[5]:<8} "
            f"{data[6]:<8} "
            f"{data[7]}"
        )

    print("-" * 70)
    print(f"처리 건수 : {len(datas)}건")


# 프로그램 실행
datas = inputfunc()
processfunc(datas)


    



    
     

    






    

