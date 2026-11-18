
# Tree : 노드들이 나무가지 처럼 연결된 계층적 비선형 자료 구조
# 시작점이 1개이고 순환이 없다.

# 회사 조직도 구조 Tree로 표현

company = {
    'CEO':['개발팀장','기획팀장','영업팀장'],
    '개발팀장':['백엔드', '프론트엔드'],
    '기획팀장':['서비스기획'],
    '영업팀장':['국내영업','해외영업'],
    '백엔드':[],
    '프론트엔드':[],
    '서비스기획':[],
    '국내영업':[],
    '해외영업':[]
}

# 트리 구조 함수
def showTree(node, level):
    print(' ' * level + ' - ' + node)
    # 현재 노드의 자식 출력
    for child in company[node]:
        showTree(child, level + 1)  # 재귀

print('회사 조직도')
showTree('CEO', 0)

# Binary Tree(이진트리) - 자식이 둘 이하(차수가 2이하)인 노드로 구성된 트리
# 노드 방문 방법 3가지 : pre-order(전위), in-order(중위), post-order(후위)
# 이진트리 순회는 DFS(깊이 우선 탐색) 기반

tree = {
    'A':('B', 'C'),
    'B':('D', 'E'),
    'C':(None, None),
    'D':(None, None),
    'E':(None, None)
}

# 전위순회
def preOrder(node):
    if node is None:
        return
    print(node, end=' ')
    left, right = tree[node]
    preOrder(left)  # 재귀
    preOrder(right)

# 중위순회
def inOrder(node):
    if node is None:
        return
    left, right = tree[node]
    inOrder(left)  # 재귀
    print(node, end=' ')
    inOrder(right)

# 후위순회
def postOrder(node):
    if node is None:
        return
    left, right = tree[node]
    postOrder(left)  # 재귀
    postOrder(right)
    print(node, end=' ')

print('전위 순회 결과 : ')
preOrder('A')
print('\n')
print('중위 순회 결과 : ')
inOrder('A')   # BST(Binary Search Tree) 오름차순 정렬 가능
print('\n')
print('후위 순회 결과 : ')
postOrder('A')