"""
랜덤 포레스트는 분류, 회귀, 모두 가능. sklearn 모듈은 대게 그러하다.
캘리포니아 주텍 가격데이터로 회귀분석
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score,mean_squared_error
from sklearn.datasets import fetch_california_housing
from sklearn.metrics import accuracy_score

hosuing=fetch_california_housing(as_frame=True)
print("집 관련 데이터 출력", hosuing.DESCR)
pd.set_option("display.max_columns",None)
df=hosuing.frame
print(df.head(3))
print(df.info())

x=df.drop('MedHouseVal',axis=1)
y=df['MedHouseVal']

train_x,test_x,train_y,test_y=train_test_split(x,y, test_size=0.3, random_state=42)
rfmodel=RandomForestRegressor(n_estimators=200,random_state=42)
rfmodel.fit(train_x,train_y)

# 예측 및 평가
y_pred=rfmodel.predict(test_x)
print(f'MSE : {mean_squared_error(test_y,y_pred):.3f}')
print(f'R2(결정계수): {r2_score(test_y,y_pred):.3f}')

# 변수 중요도 시각화
impo=rfmodel.feature_importances_
indices=np.argsort(impo)[::-1]
plt.figure(figsize=(8,5))
plt.bar(range(x.shape[1]),impo[indices], align='center')
plt.xticks(range(x.shape[1]), x.columns[indices],rotation=45)
plt.xlabel('feature name')
plt.ylabel('feature importance')
plt.tight_layout()
plt.show()

ranking=pd.DataFrame({
    'feature':x.columns[indices], 'importance':impo[indices]
})
print(ranking)