# LogisticRegresiion: 날씨 예보(비가 올지 안올지)
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import statsmodels.formula.api as smf

data= pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/weather.csv")
print(data.head(2),data.shape) #(366, 12)
print(data.info())
#  #   Column        Non-Null Count  Dtype  
# ---  ------        --------------  -----  
#  0   Date          366 non-null    str    
#  1   MinTemp       366 non-null    float64
#  2   MaxTemp       366 non-null    float64
#  3   Rainfall      366 non-null    float64
#  4   Sunshine      363 non-null    float64
#  5   WindSpeed     366 non-null    int64  
#  6   Humidity      366 non-null    int64  
#  7   Pressure      366 non-null    float64
#  8   Cloud         366 non-null    int64  
#  9   Temp          366 non-null    float64
#  10  RainToday     366 non-null    str    
#  11  RainTomorrow  366 non-null    str  
# 0과 10는 다음날 비오는데 영향을 미치는 요소가 아니니 삭제
# 1~9까지의 요소를 분리해서 독립변수로 사용

df=pd.DataFrame()
df=data.drop(['Date','RainToday'],axis=1) #data 데이터 프레임에서 컬럼 삭제. axis는 뭐지?
df["RainTomorrow"]= df['RainTomorrow'].map({'Yes':1,'No':0}) # map()?
print(df.head(2),df.shape)#(366, 10)
print(df['RainTomorrow'].unique())#[1 0]
# RainTomorrow: 종속변수(class) 범주형 / 나머지열:ㅡ독립변수(feature)

print('데이터 분리: 학습용(train dataset), 검증용(test dataset)')
# 모델의 성능을 객관저긍로 파악하기 위함. - 과적합 방지
train, test = train_test_split(df, test_size=0.3, random_state=42) # 다들 동일한 결과를 출력하기 위해 난수고정
print("train.shape, test.shape 출력\n",train.shape, test.shape)
print("train 3개", train.head(3))
print("test 3개", test.head(3))

# 모델 생성
col_select="+".join(train.columns.difference(['RainTomorrow'])) # 일일이 다 타이핑 하기 귀찮으니 Raintomorrow를 제외한 나머지 문자열 묶어주기
print("Tomorrow 제외한 컬럼들 ",col_select)
my_formula="RainTomorrow~"+col_select

model=smf.logit(formula=my_formula,data=train).fit()
print("모델 결과 ols처럼", model.summary()) # 각 변수별 p-value >0.05보다 큰 경우 제거 고민
print("모델 결과 파라미터", model.params,'\n\n')
print("예측값: ",np.rint(model.predict(test)[:5].values))
print("실제값: ",test["RainTomorrow"][:5].values)

# ####분류 정확도
# pred_table() # 기본적으로 모델 학습에 사용한 train 데이터만 대상으로 혼동행렬 생성 가능하기에 np rint와 같이 사용이 안됨
# logit이 pred_table은 지원하지만 confusio은 지원안해서 별도의 모듈을 불러와야 함
pred_mat=model.pred_table()
print(pred_mat)
print('train 분류 정확도(Accuracy): ',(pred_mat[0][0] + pred_mat[1][1])/ len(train),'\n\n') # 실제 맞춘 값, 1,4사분위 값만 사용
# 내부에 보정값 없음
# train으로 혼돈행렬 만들어서 정확도 확인한 것
# test로는 혼돈행렬을 만들 수 없음



from sklearn.metrics import accuracy_score,confusion_matrix
pred=model.predict(test)

conf_mat=confusion_matrix(test['RainTomorrow'],np.rint(pred)) # 실제값, 예측값
print("confusion의 결과\n",conf_mat)
print('confusion을 이용한 test 분류 정확도1: ',(conf_mat[0][0] + conf_mat[1][1])/ len(test)) # test를 사용하려면 confusion 써야함

# pred_table, confusion 둘 다 혼동행렬을 구하는 방식인데 pred는 train을 이용해서, confusion은 test를 이용하는 것
# 기본적으로 정확도는 test를 통해 구한다.
# train, test로 구분되어 있을 때 accuracy_score는 test만 이용해서 정확도를 검정한다.

# 

print('Accuracy를 이용한 test 분류 정확도2: ',accuracy_score(test['RainTomorrow'],np.rint(pred))) # 내부에 보정값 들어감
print('Accuracy를 이용한 test 분류 정확도3: ',accuracy_score(test['RainTomorrow'],(pred>=0.5).astype(int))) 
#(pred>=0.5).astype(int)의 역할이 np.rint(pred)=np.around(). 셋다 동일
# train의 정확도 결과와 test 정확도 결과가 유사하지 않으면 과적합 or 과소적합


# sklearn과의 차이

# 구분	                     model.pred_table()	                         confusion_matrix(y_true, y_pred)
# 출처	                        statsmodels	                                           sklearn
# 입력	             없음 (모델이 가진 학습 데이터 사용)	                실제값, 예측값을 직접 전달
# 평가 대상	                  학습 데이터(train)	                        넘겨주는 데이터 아무거나 (test 가능)
# 확률 → 0/1 변환	            자동 (threshold)	                                  직접 해야 함