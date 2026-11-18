"""
병합 정렬(Merge sort)
대표적인 분할정복 기반의 정렬 알고리즘

분할: 정렬할 전체 리스트를 원소가 1개또는 0개가 될 때까지 절반 (2개)으로 쪼갬
정복: 쪼개진 부분 리스트를 각각 재귀적으로 정렬
결합: 정렬된 두개의 부분 리스트를 하나의 정렬된 리스틀 병합.
"""

# 방법1: 이해 위주
# 전체 흐름
# 리스트를 반으로 나눔. 1개씩 남을 때까지.
# 각각 다시  merge sort 함수로 정렬
# 정렬된 두 리스트를 하나로 합친다(merge)
# 이때 합치면서 정렬된 상태를 유지한다.
def merge_sort(a):
    n=len(a)

    if n<=1: # 재귀함수 탈출하기 위함
        return a

    mid=n//2 # 중간을 기준으로 두 그룹으로
    #참고: 함수는 독립적인 공간을 가짐. 아래의 g1,g2는 서로 간섭x
    g1=merge_sort(a[:mid]) # 재귀
    print(f'g1 : {id(g1)}, {g1}')
    g2=merge_sort(a[mid:]) # 재귀
    print(f'g2 : {id(g2)}, {g2}')

    # 두 그룹을 하나로 병합하기 위한 기억장소를 별도로 사용
    result=[]
    while g1 and g2:
        print(g1[0], ' ', g2[0])
        if g1[0]<g2[0]:
            result.append(g1.pop(0))
        else:
            result.append(g2.pop(0))

    # g1과 g2 중 소진된 것은 skip
    while g1:
        result.append(g1.pop(0))
    while g2:
        result.append(g2.pop(0))  

    return result


d=[6,8,3,1,2,4,7,5]
print(merge_sort(d)) 
#6,8,3,1 // 2,4,7,5
# 6,8 // 3,1 // 2,4 // 7,5
# 6/8/3/1/2/4/7/5
# 작은것 부터 합치기 
# 68/13/24/57
# 1368/2457


print('\n==================================\n')

"""
방법2: 일반 알고리즘
재귀호출ㄹ이 정렬된 리스트를 반환
병합도 새 리스트를 만들어 반환
원본 리스트는 그대로이고 정렬된 결과는 새 리스트에 저장
"""

def merge_sort2(a):
    if len(a) <=1:
        return a

    mid=len(a)//2
    left=merge_sort2(a[:mid])
    print(f'left:{id(left)},{left}')
    right=merge_sort2(a[mid:])
    print(f'right:{id(right)},{right} \n')

    result=[]
    i=j=0

    # 병합
    while i < len(left) and j < len(right): # 자료가 있는 동안 계속 진행
        if left[i] < right[j]:
            result.append(left[i])
            i+=1
        else:
            result.append(right[i])
            j+=1

    # 남은 요소 추가
    result+=left[i:]
    result+=right[j:]
    return result

print('\n')
d=[6,8,3,1,2,4,7,5]
sorted_d=merge_sort2(d)
print(sorted_d) 