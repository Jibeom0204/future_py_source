# 최소 제곱 문제를 행렬 방정식으로 표현하고
# 수치 선형대수 연산을 통해 최적의 회귀계수(w,b) 구하기 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

x=np.array([0,1,2,3])
y=np.array([0-1, 0.2, 0.5, 2.1])
# plt.scatter(x,y)
# plt.grid(True)
# plt.show()
A=np.vstack([x,np.ones(len(x))]).T
print(A)

# 본래 데이터를 직성느로 표현하기 어려운 선형대수학 이용에 y=wx+b의 w,b 구하기
import numpy.linalg as lin
weight,bias=lin.lstsq(A,y)[0] #최소 제곱법 연산
print(weight, ' ',bias,'\n') #0.96   -0.9899999999999998

# 회귀식 y^=0.96 *-0.9899  => y=mx+b
print(0.96 *0 + -0.9899) # 실제값 -1, 예측값 -0.9899. 실제값과 예측값 사이의 차를 cost, 손실이라고 함. 추후 잔차가 딘다
print(0.96 *1 + -0.9899) # 실제값 0.2, 예측값-0.0299000
print(0.96 *2 + -0.9899) # 실제값 0.5, 예측값 0.93009
print(0.96 *3 + -0.9899) # 실제값 .1, 예측값 1.8901

plt.scatter(x,y,marker='o',label='실제값')
plt.plot(x,weight*x + bias,'r',label='최적화 된 선형직선')
plt.grid(True)
plt.show()


# 경험하지 못한 x값에 대한 예측값 y는?
new_x=7.5
yhat=weight*new_x +bias #0.96 *.5 + -0.9899
print("\nyhat 예측결과1: ",yhat) #6.20999. 신빙성있는 추론 결과로 미래의 의사결정을 위한 참고값으로 활용 가능

new_x=1.2345678
yhat=weight*new_x +bias
print("yhat 예측결과2: ",yhat) #0.1951

print('\n=============================\n')
print("선형회귀 모델 추세식 계산(최소제곱법) 클래스")
class MySimpleLinearRegression:
    def __init__(self):
        self.w=None
        self.b=None

    def fit(self,x:np.ndarray,y:np.ndarray):
        x_mean=np.mean(x)
        y_mean=np.mean(y)

        # 최소 제곱법 공식 적용
        bunja=np.sum((x-x_mean)*(y-y_mean))
        bunmo=np.sum((x-x_mean)**2)
        
        self.w=bunja/bunmo # 기울기
        self.b=y_mean-(self.w * x_mean) # 절편(편향)

    def predict(self,new_x:np.ndarray):
        # 추정된 w,bㄹㄹ 이용ㅇ해 새로운 x에 대한 예측값 반환
        return self.w * new_x + self.b

# 실행단 - 임의의 성인 50명의 키, 몸무게 데이터 생성 후, 이를 바탕으로 추세선 만들기
np.random.seed(42)
x_height=np.random.normal(175,5,50) #(정규분포(평균), 표준편차, 데이터 수) 키
y_weight=np.random.normal(70,10,50) #(정규분포(평균), 표준편차, 데이터 수) 몸무게
print("키'\n",x_height,'\n')
print("몸무게\n",y_weight,'\n')

# 모델 생성
model=MySimpleLinearRegression()
model.fit(x_height,y_weight) # 키가 독립, 몸무게가 종속. 기존 데이터를 이용해 회귀 계수 w,b를 학습. 인공신경망의 학습과 다르다
print("추정된 w(기울기)\n",model.w,'\n')
print("추정된 b(절편)\n",model.b,'\n')
# yhat= 0.2061 34.3337

y_pred=model.predict(x_height) # 기존 데이터 예측값 확인. 위의 모델에서 예측한 예측값 확인
# 학습된 회귀계수를 이용해 새로운 키에 대한 몸무게를 추정
for i in range(len(x_height)):
    print(f"키:{x_height[i]:.2f}cm의 실제 몸무게:{y_weight[i]:.2f}kg, 예측 몸무게: {y_pred[i]:.2f}")

#새로운 키에 대한 몸무게 예측
new_height=np.array([198]) # 평균키 175로 구한 예측값을 바탕으로 198의 키의 몸무게 구함
# 학습할 때 nd.array로 구했기 때문에 새 값 입력할 땍도 nd.array로 줘야함
new_weight=model.predict(new_height)
print(f'\n키{new_height}cm인 경우 몸무게는 {new_weight}kg')

# 시각화
plt.figure(figsize=(9,6))
plt.scatter(x_height,y_weight,color='blue',label='실제 데이터')
x_line=np.linspace(x_height.min(),x_height.max(),100) # 가운데 선 긋기
y_line=model.predict(x_line)
plt.plot(x_line,y_line,color='red',linewidth=2,label='회귀직선')
plt.xlabel('키(cm)')
plt.ylabel("몸무게(kg)")
plt.title('키에 따른 몸무게 선형회귀 분석')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()