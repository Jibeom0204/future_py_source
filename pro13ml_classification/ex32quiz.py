"""
xgb_roc_score2: 0.84268
예측값:  [0 0 0 0 0]
실제값:  [0 0 0 0 0]
분류 정확도:  0.9584319915811629
recall(재현율):  0.00473186119873817

RI	Na	Mg	Al	Si	K	Ca	Ba	Fe	
성분들의 종류에 따라 유리의 Type이 변경
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score,mean_squared_error
from sklearn.metrics import accuracy_score,classification_report,roc_auc_score
# pip install xgboost, lightgbm
import xgboost as xgb
from xgboost import XGBClassifier
from xgboost import plot_importance
from lightgbm import LGBMClassifier # xgboost 보다 성능은 우수하나 자료  적으면 과적합 발생
import lightgbm as lgb

data=pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/glass.csv")
print(data.head(2))
print(data.shape)
# RI     Na    Mg    Al     Si     K    Ca   Ba   Fe  Type
# 0  1.52101  13.64  4.49  1.10  71.78  0.06  8.75  0.0  0.0     1
# 1  1.51761  13.89  3.60  1.36  72.73  0.48  7.83  0.0  0.0     1
# (214, 10)

# feature / label 분리
x_features = data.iloc[:, :-1]   # 모든 행, 마지막 열(TARGET)을 제외한 모든 열
y_lab = data.iloc[:, -1]       # 모든 행, 마지막 열(TARGET) 하나 -> Series

# # XGBClassifier는 자동 레이블 변환 안되서 바꿔줘야함
# #Invalid classes inferred from unique values of `y`.  Expected: [0 1 2 3 4 5], got [1 2 3 5 6 7]
# from sklearn.preprocessing import LabelEncoder
# le = LabelEncoder()
# y_enco = le.fit_transform(y_lab) 
# print(le.classes_)                   

# train,test split
x_train,x_test,y_train,y_test=train_test_split(x_features,y_lab, test_size=0.2, random_state=0)
print("\n\n종속변수 형태",x_train.shape,x_test.shape) #(171, 9) (43, 9)

# 모델
xgb_clf=XGBClassifier(n_estimators=30, random_state=0,  eval_metric='mlogloss') # XGBClassifier 객체
xgb_clf.fit(x_train,y_train, eval_set=[(x_test,y_test)], verbose=True) # 모델 객체 학습 시키기
xgb_roc_score=roc_auc_score(y_test,xgb_clf.predict_proba(x_test), multi_class='ovr')
# 편향적인 데이터: roc_auc_score
# 고른 분포 데이터: accuracy score
# multi_class must be in ('ovo', 'ovr')

print(f'xgb_roc_score : {xgb_roc_score:.5f}')

pred=xgb_clf.predict(x_test)
print("예측값: ", pred[:7])
print("실제값: ", y_test[:7].values)
# .values: 표 껍데기(이름표, 인덱스)를 벗기고 안의 숫자만 numpy 배열로 꺼내는
print('분류 정확도: ', accuracy_score(y_test,pred))


# accuracy (정확도)

# 전체 샘플 중 모델이 맞힌 비율입니다. 맞힌 개수 ÷ 전체 개수
# 모델이 최종으로 낸 클래스 예측값(predict)과 정답을 비교합니다.
# 이진 분류에서 predict는 내부적으로 확률 0.5 같은 기준선(threshold)을 넘으면 1로 판단한 결과입니다.

# ROC AUC

# ROC 곡선 아래의 넓이입니다. ROC 곡선은 기준선(threshold)을 0에서 1까지 바꿔 가며, 가로축에 FPR(실제 0을 1로 잘못 판단한 비율), 세로축에 재현율(TPR, 실제 1을 1로 맞힌 비율)을 그린 곡선입니다.
# 모델이 낸 클래스가 아니라 확률(predict_proba)을 사용합니다.
# 값의 의미는 다음과 같습니다. 1.0은 완벽, 0.5는 무작위 수준입니다. 실제 1인 샘플과 실제 0인 샘플을 하나씩 뽑았을 때 1인 쪽의 점수가 더 높을 확률로 해석할 수도 있습니다.
# 2. 공통점
# 둘 다 분류 모델의 성능을 테스트 데이터로 평가하는 지표입니다.
# 둘 다 값이 클수록 좋고, 최대값이 1입니다.
# 둘 다 정답(y_test)과 모델의 출력을 비교해서 계산합니다.



#                                       accuracy                               ROC AUC
# 기준선(threshold)	                하나로 고정(보통 0.5)	         모든 기준선을 한꺼번에 고려
# 보는 것         	                     맞힌 비율	             1과 0을 얼마나 잘 구분해 순위를 매기는지
# 클래스 불균형	                       영향을 크게 받음	                 영향을 덜 받음
# 값이 높은데 쓸모없을 수 있나      있음 (불균형 데이터)	                 상대적으로 적음