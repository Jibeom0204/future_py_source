"""
지각횟수(x) = 1,2,3,4,5
판매횟수(y) = 8,7,6,4,5

"""

# import numpy as np
# late=np.array([1,2,3,4,5])
# sell=np.array([8,7,6,4,5])
# df=pd.DataFrame({
#     '지각': late,
#     '판매': sell
# })

# late_sales_corr=df.corr()
# print("상관관계:",late_sales_corr)


# """
#  다음 데이터는 어느 교육센터에서 실시하고 있는 파이썬 과정 중 두 명의 강사에 따른 성적에 대한 자료이다.
# 강사에 따라 성적에 차이가 있는지 평균 차이 검정을 하시오.

# 강사1 : 71 58 92 78 71 68 67 88 88 60 80 70 68 82 78
# 강사2 : 50 65 75 91 67 39 81 68 97 86 66 60 65 55 58

# ① 귀무가설 : 두 강사에 따른 성적 차이가 없다.
# ② 대립가설 : 두 강사에 따른 성적 차이가 있다.
# ③ 검정을 위한 소스 코드
# """
# import pandas as pd
# import numpy as np
# from scipy import stats


# # t 검정으로 검증
# t1=np.array([71, 58, 92, 78, 71, 68, 67, 88, 88, 60, 80, 70, 68, 82, 78])
# t2=np.array([50, 65, 75, 91, 67, 39, 81, 68, 97, 86, 66, 60, 65, 55, 58])
# data=pd.DataFrame({
#     '강사1':t1,
#     '강사2':t2
# })

# print('강사1 평균:', np.mean(t1))
# print('강사2 평균:', np.mean(t2),'\n')

# print('강사1 정규성:', stats.shapiro(t1).pvalue)
# print('강사2 정규성:', stats.shapiro(t2).pvalue,'\n')

# print("등분산성 검정",stats.levene(t1,t2).pvalue)
# # 0.3136 > 0.05: 등분산성 만족

# print("독립표본 t검정\n",stats.ttest_ind(t1, t2, equal_var=True))
# # statistic=np.float64(1.3273661364910396)
# # pvalue=np.float64(0.19510952906686385)
# # 0.195>0.05 귀무가설 채택. 선생마다 차이가 없음


# """
#  titanic data를 사용하여 아래의 지시문에 따라 의사결정나무분류 모델을 작성하고 결과를 출력하시오.

# 이하 소스 코드를 적으시오.
# 1) train_test_split (7:3), random_state=12
# 2) 의사결정나무 클래스를 사용해 분류 모델 작성
# 3) 예측결과로 분류 정확도를 출력
# """

# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import koreanize_matplotlib
# from sklearn.model_selection import train_test_split, cross_val_score
# from sklearn.metrics import r2_score,mean_squared_error
# from sklearn.metrics import accuracy_score,classification_report,roc_auc_score
# from sklearn.tree import DecisionTreeClassifier,plot_tree

# data = pd.read_csv(
#     'https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/titanic_data.csv',
#     usecols=['Survived', 'Pclass', 'Sex', 'Age', 'Fare']
# )
# data["Sex"] = data["Sex"].map({"male": 0, "female": 1})

# print(data["Sex"].dtype) 

# feature = data[["Pclass", "Sex", "Fare"]]   
# label = data["Survived"] 

# print(feature[:3])
# print(label[:3])

# x_train, x_test, y_train, y_test = train_test_split(
#     feature, label, test_size=0.3, random_state=12
# )

# model=DecisionTreeClassifier(criterion='gini',max_depth=3) # 트리 최대값
# model.fit(x_train,y_train)
# print("예측값: ",model.predict(x_test[:3]))
# print("실제값: ",y_test[:3])
# print("정확도: ",model.score(feature,label))


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score,mean_squared_error
from sklearn.metrics import accuracy_score,classification_report,roc_auc_score
from sklearn.linear_model import LinearRegression

df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/data/train.csv", parse_dates=['datetime'])

df['datetime'] = pd.to_datetime(df['datetime'])


df['year'] = df['datetime'].dt.year
df['month'] = df['datetime'].dt.month
df['day'] = df['datetime'].dt.day
df['hour'] = df['datetime'].dt.hour

df = df.drop(columns=['datetime', 'casual', 'registered'])

print(df.columns.tolist())  
 
print(df.isna().sum().sum())  