"""
sigmoid function 적용 연습
LogisticRegression algorithm은 선형 회귀 알고리즘을 기반으로 만들어진 알고리즘이므로, 선형 회귀 알고리즘과 동일하게 w와 b를 학습함.
LogissticRegression 모델은 wx+b를 logit변환한 값에 sigmoid function을 처리한 값

logit 변환: log(p/(1-p)) = wx+b
그러므로 z=wx+b --> sigmoid(z) --> p(0~1) : 이항 분류

logit이란 오즈비(odds ratio)의 로그를 취한 값으로, 확률 p를 오즈비로 변환한 후 로그를 취한 값임.
sigmoid function은 0~1 사이의 값을 출력하는 함수로, 로지스틱 회귀에서 이진 분류 문제를 해결하기 위해 사용됨.

logit과 sigmoid function은 서로 역함수 관계에 있음.
한마디로 LogisticRegression은 wx+b를 logit 변환한 값에 sigmoid function을 처리한 값으로, 0~1 사이의 확률값을 출력하는 이항 분류 알고리즘임.

wx+b와 오즈비의 관계는 아래와 같음.


■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
단순한게 설명하면 wx+b에 sigmoid를 적용한 값이 우리가 보는 값. 이항 분류 값.

    선형식               ==>  z = wx + b          ← 이 값이 logit (= 로그 오즈, log-odds). 범위: -∞ ~ +∞
sigmoid 적용             ==>  p = 1 / (1 + e^(-z))  ← 확률. 범위: 0 ~ 1
기준값(0.5)으로 자르기    ==> 클래스 = 1 if p ≥ 0.5 else 0   ← 이항 분류 결과
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""


# sigmoid function 수식에 의해 변환된 값
import math

def MysigmoidFunc(num):
    return 1/(1+math.exp(-num))

print(MysigmoidFunc(3))
print(MysigmoidFunc(1.5))
print(MysigmoidFunc(-5.0))
print(MysigmoidFunc(-10))
# 0.9525741268224334
# 0.8175744761936437
# 0.0066928509242848554
# 4.5397868702434395e-05

import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

print('\n========logit 변환된(가정)값으로 시그모이드 함수 통과 후 결과 시각화========\n')
x=np.linspace(-10,10,50) # 입력자료(연속형)
print(x)

# 선형 결합(이미 logit처리된 값)
w=1.5
b=-2
z=w*x+b

def OurSigmoidFunc(z): # z: logit 변환된 값이라고 가정
    return 1/(1+np.exp(-z))

p=OurSigmoidFunc(z)
print('P: \n',p)

# 일부만 보기
print('x[:3]:', np.round(x[:3],3)) #[-10.     -9.592  -9.184]
print('z[:3](logit): ',np.round(z[:3],3)) #[-17.    -16.388 -15.776]
print("p[:3](확률): ",p[:3]) # [4.13993755e-08 7.63639448e-08 1.40858451e-07]

# 시각화
plt.figure(figsize=(8,5))
plt.plot(x,p,label='sigmoid(z)',color='blue')
plt.axhline(0.5, c='red', ls='--')
plt.title("z=wx+b --> sigmoid --> 확률(이항)")
plt.xlabel("x(입력값)")
plt.ylabel("p(확률값)")
plt.grid(True)
plt.legend()
plt.show()

"""
로지스틱 회귀 분석은 독립변수와 범주형 종속 변수의 관계를 학습하여 분류를 수행하는 알고리즘
독립변수에 학습된 가중치와 절편을 적용하여 z=wx+b를 계산.
z=wx+b 계산된 값은 확률 자체가 아니라 로그 오즈(logit) 값으로, -무한대부터 +무한대까지의 범위를 가짐.
★★wx+b 자체가 이미 logit 값★★
이후 시그모이드 함수를 적용하여 0과 1 사이의 확률을 구하고 일반적으로 0.5 기준으로 클래스를 분류함

X -> wx+b(이미 로짓 값) -> sigmoid -> 확률 -> 클래스 분류
로지스틱 회귀는 wx+b를 계산하기 전에 선형 회귀의 추세선을 별도로 학습하는 것이 아니라
학습과정에서 분류에 적합한 가중치w와 절편 b를 직접 추정함
"""