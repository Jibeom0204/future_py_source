# 계층적 군집 분석: 학생 10명의 시험점수 사용
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage,dendrogram,fcluster
#linkage: 데이터를 가까운 순서대로 병합하고, 그 병합 기록을 표(배열)로 반환
#fcluster: linkage가 만든 트리(Z)를 특정 기준으로 잘라서, 각 데이터가 어느 클러스터에 속하는지 번호를 붙여 주는 함수
students=['s1','s2','s3','s4','s5','s6','s7','s8','s9','s10']
scores=np.array([76,95,65,85,60,92,55,88,83,72]).reshape(-1,1)
print('점수: ',scores)
linked=linkage(scores,method='ward')

# 시각화
plt.figure(figsize=(10,6))
dendrogram(linked,labels=students)
plt.title('학생들 점수 군집')
plt.xlabel('학생명')
plt.ylabel('거리')
plt.axhline(y=25,color='red',linestyle='--',label='cut at 25')
plt.legend()
plt.grid(True)
plt.show

# 계층적 군집 분석 결과를 3개의 군지븡로 나누기
clusters=fcluster(linked,t=3,criterion='maxclust')
print('학생 군집 결과')
for stu,cluster in zip(students,clusters):
    print(f'{stu} : cluster {cluster}')

print()
# 군집별 점수와 이름 확인
cluster_info={}
for student, cluster,score in zip(students,clusters,scores.flatten()):
    if cluster not in cluster_info:
        cluster_info[cluster]={"students":[], "scores":[]}
    cluster_info[cluster]["students"].append(student)
    cluster_info[cluster]["scores"].append(score)
print(cluster_info)

print('\n==================군집별로 평균 점수와 이름 출력==================\n')
for cluster_id,info in sorted(cluster_info.items()):
    # 메서드	돌려주는 것
    # d.keys()	키만
    # d.values()	값만
    # d.items()	(키, 값) 쌍
    # sorted(): 반복 가능한 객체를 받아 정렬된 새 리스트
    
    avg_score=np.mean(info["scores"])
    student_list=",".join(info["students"])
    print(f'군집 {cluster_id}: 평균점수={avg_score:.2f}, 학생들={student_list}')


# 군집별 시각화
x_position=np.arange(len(students))
y_scores=scores.ravel() # 차원하강 = flatten()
colors={1:'red',2:'blue',3:'green'}
plt.figure(figsize=(10,6))
for i,(x,y,cluster) in enumerate(zip(x_position,y_scores,clusters)):
    plt.scatter(x,y,color=colors[cluster],s=100)
    plt.text(x,y+1.5,students[i],fontsize=12,ha='center')

plt.xticks(x_position,students)
plt.xlabel('Students')
plt.ylabel('Scores')
plt.title('Score cluster')
plt.grid(True)
plt.show()