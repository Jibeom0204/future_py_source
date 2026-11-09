import pandas as pd

items = {
    'apple':{'count':10, 'price':1500},
    'orange':{'count':5, 'price':800}
}

df = pd.DataFrame(items)
print(df)

# DataFrame 저장
# 클립보드로 저장
df.to_clipboard()  # 메모장 등으로 확인
print(df.to_html()) # 데이터 프레임을 html 형식으로 변환
print(df.to_json()) # 데이터 프레임을 json(키:밸류)형식으로 전환
# JSON은 데이터를 주고받기 위한 문자열(Text) 형식이고,
# 파이썬 딕셔너리(Dict)는 파이썬 메모리에서 데이터를 다루는 데이터 구조(자료형)

df.to_csv('result1.csv', sep=',')
df.to_csv('result2.csv', sep=',', index=False)
df.to_csv('result3.csv', sep=',', index=False, header=False)
print()
df2 = df.T
print(df2)
df2.to_csv('result4.csv', sep=',', index=False, encoding='utf-8-sig')
redata = pd.read_csv('result4.csv')
print(redata)

print('\n엑셀 관련 ------')
df3 = pd.DataFrame({
    'name':['Alice', 'Bob', 'Oscar'],
    'age':[24, 22, 29],
    'city':['seoul','suwon','incheon']
})
print(df3)

# 엑셀 파일 i/o
# 저장
df3.to_excel('result.xlsx', index=False, sheet_name='work1')

# 읽기
exdf = pd.ExcelFile("result.xlsx")
print(exdf.sheet_names)
df4 = exdf.parse("work1")
print(df4)