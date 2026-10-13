"""
편차가 큰 데이터에 대한 로그 변환
큰 값을 압축해서 데이터간 격차를 줄이는 변환이 가능함

ML에서 데이터 분석 시 log를 사용하면?
1) 스케일 차이를 축소해 준다 log(10)=1 log(100)=2 log(1000)=4
2) 로그 변환하면 치우친 데이터를 정규분포에 가깝게 변경 가능. 로지스틱, 시그모이드
3) 모델링에서 지수 관계를 선형 관계를 바꿔준다

a^x=ㅠ  => x =log(a)b
"""

import numpy as np
np.set_printoptions(suppress=True,precision=6)

def test():
    values=np.array([345,34.5,3.45,0.345,0.01,0.1,10,100])
    print("이진 로그 log2(3.45):",np.log2(3.45),"\n")
    print("십진 로그 log10(3.45):",np.log10(3.45),"\n")
    print("자연 로그 log(3.45):",np.log(3.45),"\n")

    print("원본값: ", values,"\n")
    log_values=np.log10(values)
    print("상용로그 log_values: ",log_values) # 상용로그
    ln_values=np.log(values)
    print("자연로그 ln_values: ",ln_values) # 자연로그: 밑이 e인 로그. Machine Learning에서 주로 사용

    # 서로 다른 스케일을 가진 특성(Feature)들을 일정한 기준으로 맞춰주는 피처 스케일링(Feature Scaling) 방법
    # 정규화: 데이터의 범위를 특정 구간(주로 0과 1 사이)으로 변환하는 방식
    # ==> (원본 데이터-최소값)/(최대값-최소값)
    min_val=np.min(values)
    max_val=np.max(values)
    normalized=(values-min_val)/(max_val-min_val)
    print('정규화 결과: : ', normalized,"\n")

    # 표준화: 0, 표준편차를 1이 되도록 변환하는 방식
    # ==> (데이터 - 평균) / 표준편차
    mymean=np.mean(values)
    mystd=np.std(values)
    standardized=(values-mymean)/mystd
    print("표준화 결과: ",standardized,"\n")


class LogTrans:
    # 편차가 큰 데이터를 로그 스케일로 변환하고 그 역변환을 제공하는 클래스
    def __init__(self,offset:float=1.0): # offset: 보정값(log(0)) 피하기
         self.offset=offset

    # 로그 변환 메소드
    def transform(self,x:np.ndarray)-> np.ndarray:
        return np.log(x+self.offset)

    # 역 변환 메소드
    def inverse_transform(self,x_log:np.ndarray)-> np.ndarray:
        return np.exp(x_log)-self.offset

def main():
    test()
    print("==========================================")

    data = np.array([0.001,0.01,0.1,1,10,100,1000,10000],dtype=float)
    logObj=LogTrans() # 클래스를 받아오는 객체 변수 선언

    data_log_scaled=logObj.transform(data) # 로그 변환
    reversed_data=logObj.inverse_transform(data_log_scaled) #역변환

    print("원본: ",data,'\n')
    print('로그 변환: ',data_log_scaled,'\n')
    print('역 변환: ',reversed_data,'\n')


if __name__ == "__main__":
    main()