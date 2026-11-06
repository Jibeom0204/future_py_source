"""
ROC Curve는 모든 분류
임계값에서 분류 모델의 성능을 보여주는 그래프로 x축이 FPR(1-특이도), y축이 TPR(민감도)인 그래픔
즉 민감도와 특이도 관꼐를 표현한 그래프
AUC(그래프 아래 면적)을 이요해 모델의 성능을 평가함
AUC가 클수록 정확히 분류함을 의미
특이도가 변할 때 민감도가 얼마나 반응하는지 확인
"""

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

x,y=make_classification(n_samples=100, n_features=2, n_redundant=0,random_state=123)
# n_redundant=독립변수 중 다른 독립변수의 선형 조합으로 나타내는 성분 수
print("x 배열 크기\n",x[:3], x.shape,'\n')# shape: 배열의 크기를 튜플로 표현
print("y 배열 크기\n", y[:3], y.shape,'\n')

# plt.scatter(x[:,0],x[:,1])
# plt.show()
model=LogisticRegression().fit(x,y)
y_hat=model.predict(x)
print("예측값 10개: ",y_hat[:10]) #[0 0 0 1 1 1 0 0 0 1]
print("실제값 10개: ",y[:10])     #[1 0 0 1 0 1 0 1 0 1]

# ROC Curve의 판별 경계선 설정용 결정함수 데이터
f_value=model.decision_function(x)
print('f_value : ',f_value[:10])
df=pd.DataFrame(np.vstack([f_value,y_hat,y]).T, columns=['f','y_hat','y'])
print("데이터프레임 출력\n",df.head(),'\n')

# 모델 성능 파악
from sklearn.metrics import confusion_matrix
print("실제값, 예측값 교차 검증\n",confusion_matrix(y,y_hat),'\n')
# [[44  4]
# [ 8 44]]

accuracy=(44+44) /100    # TP + TN / 전체수 => 정확도
recall= 44 / (44+4)      # TP / (TP+FN) => 재현율
precision = 44 / (44+8)  # TP / (TP+FP) => 정밀도
specificity= 44 / (8+44) # TN / (FP+TN) => 특이도
fallout= 8 / (8+44)      # FP / (FP+TN) => 위양성률(fpr)
print("정확도: ",accuracy) #0.88
print("재현율: ",recall) #0.9166
print("정밀도: ",precision) #0.8461
print("특이도: ",specificity,'\n') #0.8461
print("위양성: ",fallout) #0.1538
print("산술식으로 구하는 위양성(1-특이도): ",1-specificity,'\n\n') #0.1538

# 일일이 구하는 건 번겁로움
from sklearn import metrics
accuracy_score= metrics.accuracy_score(y,y_hat)
print("메서드 써서 구한 정확도: ",accuracy_score)

cl_rep=metrics.classification_report(y,y_hat)
print("분류 모델 성능평가 보고서:\n",cl_rep)
#                precision    recall  f1-score   support

#            0       0.85      0.92      0.88        48
#            1       0.92      0.85      0.88        52

#     accuracy                           0.88       100
#    macro avg       0.88      0.88      0.88       100
# weighted avg       0.88      0.88      0.88       100
# --------------------------------------------------------
# precision: 모델이 0이라고 예측한 것중 85%가 0         예측한 것 중 맞힌 비율
# recall: 실제 0인 48개 중 92%를 제대로 찾음            실제 정답 중 찾아낸 비율
# f1-score: 전체 100개 중 정확하게 찾은게 88개. 88%     precision과 reacall의 조화 평균
# macro avg: 단순평균 0.85+0.92 평균은 0.88             클래스 별 성능의 단순 평균
# weighted avg: 가중평균 support가 추가됨               클래스 별 데이터 개수를 고려한 가중평균
# support                                             실제 클래스별 데이터 개수
# Accuracy                                            전체 데이터 중 올바르게 분류한 비율
#=================================================================

fpr,tpr,thresholds=metrics.roc_curve(y,model.decision_function(x))
# thresholds: 분류 결정 임계값(결정수값)
plt.plot(fpr,tpr,'o-',label='LogisticRegression')
plt.plot([0,1],[0,1],'k--',label='random classifier line(AUC:0.5 지점)')


#### 특정값 보고 싶을 때 쓰는것들#####
#plt.plot([fallout],[recall],'ro',ms=6) # 위양성률 재현율 출력

# 위 명령대신 특정 임계값에 해당하는 ROX 좌표로 표시. 그래프만 보고 싶으면 이것도 주석처리 ㅐㅐ
i=3
plt.plot([fpr[i]],[tpr[i]],'ro',ms=6,label="선택한 임계값")
#####=============#####

plt.xlabel('fpr')
plt.ylabel('tpr')
plt.title("ROC Curve")
plt.legend()
plt.show()

print('AUC: ROC 커브의 밑면적. 1에 근사할수록 좋은 모델')
print("AUC: ", metrics.auc(fpr,tpr)) #0.95472
# fpr: 실제 값이 '음성(Negative)'인 것들 중에서, 모델이 '양성(Positive)'이라고 잘못(False) 예측한 비율
# tpr: 실제 값이 '양성(Positive)'인 것들 중에서, 모델이 '양성(Positive)'이라고 바르게 예측한 비율