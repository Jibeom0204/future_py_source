# 외국인(미,일,중)이 국내 관광지 5개 방문 관련자료 사용
# 나라별 관광지 상관관계 확인하기
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 산점도 그리기

def setScatterGraph(tour_table,all_table,tourPoint):
    print(tourPoint)
    print('tour_table 크기: ',tour_table.shape)
    print('all_table 크기: ',all_table.shape,'\n')
    
    # 현재 관광지 데이터만 추출
    # print("년월, 관광지명, 외국인방문 수,미일중 가공된 관광지명\n",tourPoint)
    

    # 계산할 관광지명에 해당하는 자료만 뽑아 tour에 저장 후 외국인 자료와 병합
    tour=tour_table[tour_table['resNm']==tourPoint] # 관광지 이름으로 for 돌려서 생긴 데이터와 관광지 이름이 동일한거 추출
    # print('관광지 방문 데이터 건수: ',len(tour),'\n')
    # print('외국인 방문 데이터 건수: ',len(all_table),'\n')
    print("tour 출력: ",tour)
    merge_table=pd.merge(tour,all_table,left_index=True,right_index=True)
    print("merge_table\n",merge_table,'\n')

    # 시각화 -상관계수
    fig = plt.figure()
    fig.suptitle(tourPoint+'상관관계 분석')

    # 중국인 시각화
    plt.subplot(1,3,1)
    plt.xlabel='중국인 방문 수'
    plt.ylabel='외국인 입장객 수'
    lamb1=lambda p:merge_table['china'].corr(merge_table['ForNum'])
    r1=lamb1(merge_table)
    print('r1 : ',r1) # 중국인 데이터 r1 :  -0.583421
    plt.title('r={:.5f}'.format(r1))
    plt.scatter(merge_table['china'],merge_table['ForNum'],alpha=0.7,s=6,c='black')

    # 일본인 시각화
    plt.subplot(1,3,2)
    plt.xlabel='일본인 방문 수'
    plt.ylabel='외국인 입장객 수'
    lamb2=lambda p:merge_table['japan'].corr(merge_table['ForNum'])
    r2=lamb2(merge_table)
    print('r2 : ',r2) # 일본인 데이터 r1 :  -0.583421
    plt.title('r={:.5f}'.format(r2))
    plt.scatter(merge_table['japan'],merge_table['ForNum'],alpha=0.7,s=6,c='red')
    
    # 일본인 시각화
    plt.subplot(1,3,3)
    plt.xlabel='미국인 방문 수'
    plt.ylabel='외국인 입장객 수'
    lamb3=lambda p:merge_table['usa'].corr(merge_table['ForNum'])
    r3=lamb3(merge_table)
    print('r2 : ',r2) # 일본인 데이터 r1 :  -0.583421
    plt.title('r={:.5f}'.format(r3))
    plt.scatter(merge_table['usa'],merge_table['ForNum'],alpha=0.7,s=6,c='blue')

    plt.tight_layout()
    plt.show()

    return [tourPoint,r1,r2,r3]





def processFunc():
    # 서울시; 관광지 정보 파일 읽기
    fname="서울특별시_관광지입장정보_2011_2016.json"
    jsonTP=json.loads(open(fname, mode='r', encoding='utf-8').read())
    # print("읽어온 json 파일 출력",jsonTP)

    tour_table=pd.DataFrame(jsonTP,columns=("yyyymm","resNm","ForNum")) # 년월, 관광지명, 외국인방문 수
    tour_table=tour_table.set_index('yyyymm') # 날짜를 인덱스로 바꿈
    #print("날짜, 관광지명, 외국인 방문 수\n",tour_table.head())   
    resNm=tour_table.resNm.unique()
    # print("관광지명",resNm[:5]) #['창덕궁', '운현궁', '경복궁', '창경궁', '종묘']

    # 중국인 관광지 정보 파일 읽기
    cdf= '중국인방문객.json'
    jdata=json.loads(open(cdf,mode='r',encoding='utf-8').read())
    china_table=pd.DataFrame(jdata,columns=('yyyymm','visit_cnt'))
    china_table=china_table.rename(columns={'visit_cnt':'china'})
    china_table=china_table.set_index('yyyymm')
    print("연도별 중국인 방문객 수\n",china_table[:2],'\n')

    # 일본인 관광지 정보 파일 읽기
    jdf= '일본인방문객.json'
    jdata=json.loads(open(jdf,mode='r',encoding='utf-8').read())
    japan_table=pd.DataFrame(jdata,columns=('yyyymm','visit_cnt'))
    japan_table=japan_table.rename(columns={'visit_cnt':'japan'})
    japan_table=japan_table.set_index('yyyymm')
    print("연도별 일본인 방문객 수\n",japan_table[:2],'\n')

    # 일본인 관광지 정보 파일 읽기
    udf= '미국인방문객.json'
    jdata=json.loads(open(udf,mode='r',encoding='utf-8').read())
    usa_table=pd.DataFrame(jdata,columns=('yyyymm','visit_cnt'))
    usa_table=usa_table.rename(columns={'visit_cnt':'usa'})
    usa_table=usa_table.set_index('yyyymm')
    print("연도별 미국인 방문객 수\n",usa_table[:2],'\n')
    
    # 모든 테이블 합치기. 구조가 같아서 가능
    all_table=pd.merge(china_table,japan_table,left_index=True, right_index=True) # 인덱스 기준으로 테이블 통합
    all_table=pd.merge(all_table,usa_table,left_index=True, right_index=True)
    print("통합 테이블 출력\n",all_table,'\n')

    r_list=[]
    for tourPoint in resNm[:5]:
        r_list.append(setScatterGraph(tour_table,all_table,tourPoint))

    print('\n\n======processFucn 영역======')
    # print('setScatterGraph() 함수 실행 결과 받아오기\n',r_list,'\n') # (setScatterGraph() 함수 실행 결과 받아오기

    r_df=pd.DataFrame(r_list,columns=('고궁 이름','중국','일본','미국'),)
    r_df=r_df.set_index('고궁 이름')
    print("산점도 처리결과 데이터 프레임 형식으로.\n\n",r_df,'\n')

    r_df.plot(kind='bar',rot=50)
    plt.show()


if __name__=="__main__":
    processFunc()