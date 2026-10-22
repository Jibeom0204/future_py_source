"""
말뭉치(코퍼스, Corpus)는 자연어 연구, 언어 분석, 인공지능(AI) 학습을 위해 다양한 분야의 언어 자료를
컴퓨터가 읽고 처리할 수 있도록 모아 놓은 대규모 텍스트·음성·영상 데이터 집합
=> 사람이 실제로 쓰고 말한 언어 자료를 수집,정제한 데이터
문법 연구, 번역 시스템, 책봇 등 다양한 언어 데이터 분석의 기초 자료로 활용.

형태소: 의미를 가지는 가장 작은 단위를 말함

불용어:자연어 처리(NLP)와 텍스트 마이닝에서 분석에 큰 의미가 없어 제거하는 단어
문장이나 문서에서 자주 등장하지만, 문서의 핵심 주제나 의미를 파악하는 데는 기여도가 낮은 단어
=========================================================================================================
Token: 자연어 처리(NLP)에서 토큰(Token)은 컴퓨터가 텍스트를 이해하고 연산할 수 있도록 쪼개는 최소 의미 단위
혹은 글자의 조각처럼 의미를 가진 최소 단위로 쪼갠 결과물을 의미

토근의 주요 유형:
단어 수준 토큰화 (Word-based), 문자 수준 토큰화 (Character-based),
형태소 수준 토큰화 (Morpheme-based - 한국어 등 교착어), 서브워드 토큰화 (Subword-based)

"""

# 영어 토크화
import nltk
from nltk.tokenize import word_tokenize

# 최초 실행 시 필요한 데이터 다운로드
nltk.download("punkt")
nltk.download("punkt_tab")

text="I am Ironman Bring me Thanos"

# 1. 토큰화
tokens =word_tokenize(text)
print("토큰 처리한 결과",tokens,'\n')#토큰 처리한 결과 ['I', 'am', 'Ironman', 'Bring', 'me', 'Thanos'] 
# 품사 태깅
pos_tags=nltk.pos_tag(tokens)
print("품사 태깅 결과",pos_tags,'\n')#품사 태깅 결과 [('I', 'PRP'), ('am', 'VBP'), ('Ironman', 'NNP'), ('Bring', 'NNP'), ('me', 'PRP'), ('Thanos', 'NNP')] 
# PRP 대명사 ...

print("\n\n===========한국어 토큰화===========\n\n")
# pip install JYpl
# 대표적인 한글 형태소 분석 라이브러리
from konlpy.tag import Okt,Kkma,Komoran

text= "나는 오늘 아침에 학교에 갔다. 갔는데 너무 졸려서 커피를 마셨다"

print('Okt==============')
okt=Okt()
print("okt 형태소: ", okt.morphs(text),'\n')
print("okt 품사 태깅: ", okt.pos(text),'\n')
print("okt 품사 태깅(어간 포함): ", okt.morphs(text,stem=True),'\n')
print("okt 명사 추출: ", okt.nouns(text),'\n')

print('Kkma==============')
kkma=Kkma()
print("kkma 형태소: ", kkma.morphs(text),'\n')
print("kkma 품사 태깅: ", kkma.pos(text),'\n')
print("kkma 명사 추출: ", kkma.nouns(text),'\n')

print('Komoran==============')
komoran=Komoran()
print("komoran 형태소: ", komoran.morphs(text),'\n')
print("komoran품사 태깅: ", komoran.pos(text),'\n')
print("komoran 명사 추출: ", komoran.nouns(text),'\n')