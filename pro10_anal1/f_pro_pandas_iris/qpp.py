from flask import Flask, render_template,request
from pathlib import Path
import pandas as pd
import numpy as np
import seaborn as sns
import koreanize_matplotlib
import matplotlib
matplotlib.use('Agg') # Anti Grain Geometric
import matplotlib.pyplot as plt


app=Flask(__name__)
BASE_DIR=Path(__file__).resolve().parent # 현재 파일의 경로 확인. resolve가 뭐라고?
STATIC_DIR=BASE_DIR/ 'static'/'images'
STATIC_DIR.mkdir(parents=True, exist_ok=True) # 중간의 폴더 확인하고 있으면 그대로 사용. 없으면 만들어

df=sns.load_dataset("iris") # 불필요하게 show 호출할 때마다 부르지 않고 아예 한번만 호출함

@app.get("/")
def main():
    return render_template("main.html")


@app.get("/showdata")
def showdata():
    # df=sns.load_dataset("iris") # 매번 showdata 할때마다 iris 계속 불러와서 비효율적임
    # # 아예 밖으로 빼버리자. 이건 주석처리
    # print(df.head())
    irisdata=df.to_html()

    #pie chart 생성 및 저장(서버에서 자체출력 X)
    counts=df['species'].value_counts().sort_index()

    plt.figure()
    counts.plot.pie(autopct='%1.1f%%',startangle=90,ylabel=' ') #출력너비%1 1f = 소수1째자리까지 % 기호 추가
    plt.tight_layout()

    img_path=STATIC_DIR/'f_pro_pandas.png'
    plt.savefig(img_path,dpi=130) #dpi: 픽셀단위
    plt.close() # 메모리 자원 해제

    return render_template("show.html",
                           irisdata=irisdata,
                           piechart='images/f_pro_pandas.png')


@app.get("/showdata2")
def showdata2(): # 동적인 차트
    #pie chart 생성 및 저장(서버에서 자체출력 X)
        irisdata=df.to_html()
        counts=df['species'].value_counts().sort_index()

        #chart.js에 전달할 데이터
        labels=counts.index.to_list() # js에서 읽기 위함
        values=counts.tolist()

        return render_template("show2.html",
                                irisdata=irisdata,
                                labels=labels,
                                values=values)

if __name__=='__main__':
    app.run(debug=True)