"""
과적합 방지 방법의 이해
K-Fold: 안정적 평가
GridSearchCV: 최적의 하이퍼파라미터 검색

iris dataset 사용
"""

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeRegressor,DecisionTreeClassifier
from sklearn.metrics import accuracy_score

iris=load_iris()
print(iris.keys())

train_data=iris.data #입력값(특성). 꽃받침 길이·너비, 꽃잎 길이·너비 4개
train_label=iris.target #정답 라벨(레이블) 배열 setosa,versicolor,virginica
print(train_data[:3])
print(train_label[:3])

# 분류 모델
df_clf =DecisionTreeClassifier()
df_clf.fit(train_data,train_label)
pred= df_clf.predict(train_data) # 학습 데이터로 검증
print("예측값: ",pred)
print("실제값: ",train_label)
print('분류 정확도: ',accuracy_score(train_label,pred))

print("\n\n==============과적합 방지 목적 처리1: train/test split==============\n")
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(iris.data,iris.target,test_size=0.3, random_state=0)
df_clf.fit(x_train,y_train) # 시험용 데이터, 그 실험 데이터의 결과
pred2 =df_clf.predict(x_test) # test로 학습 -> 검증 목적

print("예측값(split)\n", pred2)
print("실제값(split)\n", y_test)
print("분류 정확도(split)\n", accuracy_score(y_test,pred2))


print("\n\n==============과적합 방지 목적 처리2: Cross Validation(교차검증)==============\n")
# K-폴드 교차 검증은 머신러닝 모델의 일반화 성능을 객관적으로 평가하기 위해
# train 데이터를 K개의 부분집합(Fold)으로 나누어 학습과 검증을 반복하는 방법.
# train dataset= train / validation Dataset으로 나누어 모델을 학습
# train dataset을 여러 개로 나눈다
from sklearn.model_selection import KFold
import numpy as np

features=iris.data
label=iris.target
df_clf2=DecisionTreeClassifier(criterion='gini',max_depth=3, random_state=12)
kfold=KFold(n_splits=5) # k:5회 접기
cv_acc=[] # 각 1회 마다 정확도 저장용
print('iris shape : ', features.shape) 

# KFold 학습시 전체 150행이 학습데이터(4/5, 120개), 검증 데이터(1/5,30개)로 분할되어 학습함
n_iter=0
for train_index, test_index in kfold.split(features):
    # print('n_iter(반복수): ', n_iter)
    # print('train_index(120개로 학습): \n',train_index) 
    # print('test_index(30개로 검정): \n',test_index) # 실제 검정 결과가 출력된 것이 아니다. 검정 결과를 낼 수 있는 데이터라는 뜻.
    # n_iter +=1
    # print()
    xtrain, xtest=features[train_index],features[test_index] 
    ytrain,ytest=label[train_index], label[test_index]
    
    # 학습 및 예측
    df_clf2.fit(xtrain,ytrain) # train으로 학습
    pred =df_clf2.predict(xtest) # 모델 생성을 위한 학습 도중 예측 - 검증목적
    n_iter+=1

    # 반복할 때마다 정확도 출력
    accuracy=np.round(accuracy_score(ytest,pred),5)
    train_size=xtrain.shape[0]
    test_size=xtest.shape[0]
    print(f'반복수:{n_iter}, 교차검증 정확도:{accuracy}, \
          학습 데이터 크기:{train_size}, 검증크기:{test_size} ')
    print(f'반복수:{n_iter}, 검증 데이터 인덱스_ 아래 30개 데이터로 검증 : \n{test_index}')

    cv_acc.append(accuracy)
    print()

print('cs_acc 결과: ',np.array(cv_acc).astype(float))
print('평균 검증 정확도: ',np.mean(cv_acc))

# 참고: StratifiedKFold- 불균형한 분포도를 가진 레이블 데이터 집합을 처리하기 위한 KFold방식
# 예를 들어 대출 사기 데이터인 경우, 대부분은 정상 사기 레이블은 극히 일부


print("\n\n==============과적합 방지 목적 처리2-1: 교차검증 단순화 함수 사용==============\n")
# cross_val_score를 이용해 교차 검증을 간단히 수행
from sklearn.model_selection import cross_val_score
data=iris.data # 데이터
label=iris.target # 데이터에 의한  결과

score=cross_val_score(df_clf2, data, label, scoring='accuracy', cv=5)
print("교차 검증별 정확도 : ",np.round(score,3))
print("교차 검증별 정확도 : ",np.round(np.mean(score),3))


print("\n\n==============과적합 방지 목적 처리3: GridSearchCV==============\n")
# 과적합 방지 간접 방법
# 최적의 파라미터 찾기(내부적으로 KFold를 사용해 과적합을 줄이는데 도움을 준다)
from sklearn.model_selection import GridSearchCV
# class DecisionTreeClassifier(
    
#     criterion: Literal['gini', 'entropy', 'log_loss'] = "gini",
#     splitter: Literal['best', 'random'] = "best",
#     max_depth: Int | None = None,
#     min_samples_split: float = 2,
#     min_samples_leaf: float = 1,
#     min_weight_fraction_leaf: Float = 0,
#     max_features: float | Literal['auto', 'sqrt', 'log2'] | None = None,
#     random_state: Int | RandomState | None = None,
#     max_leaf_nodes: Int | None = None,
#     min_impurity_decrease: Float = 0,
#     class_weight: Mapping | str | Sequence[Mapping] | None = None

## 이 중 몇가지 파라미터만 사용
# max_depth: 노드의 최대 깊이
# min)samples_split: 노드 분할을 위한 최소한의 샘플 수(과적합 제어와 관련)

parameters={'max_depth':[1,2,3], 'min_samples_split':[2,3]}
grid_dtree=GridSearchCV(estimator=df_clf2,param_grid=parameters,cv=3,refit=True) # 측정할 대상은 df_clf2
grid_dtree.fit(x_train,y_train)
# 내부적으로 복수 개의 모형을 생성하고 이를 실행시켜 최적의 파라미터를 찾아줌

import pandas as pd
pd.set_option('display.max_columns',None)
scores_df=pd.DataFrame(grid_dtree.cv_results_) #gridsearch클래스로 생성된 모델 객채의 결과를 score_df에 저장
print("모델결과\n",scores_df,'\n') # 전체 출력
print("GridResaechCV 최적 파라미터:", grid_dtree.best_params_)
print("GridResaechCV 최적 정확도:", grid_dtree.best_score_)

# 추천된 파라미터로 최적의 모델을 생성(직접 생성 또는 best_estimator_사용)
bestModel=grid_dtree.best_estimator_
print("\n추천된 최적의 파라미터로 만들어진 모델",bestModel,'\n')
best_pred=bestModel.predict(x_test)
print("최고 모델 예측 결과: \n",best_pred)
print("최고 모델과 비교한 정확도: ",accuracy_score(y_test,best_pred))

# 과적합 방지 방법 기타: 불필요한 변수 제거, 정규화(L1,L2), 학습 데이터 증가, 조기종료