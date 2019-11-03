# 참고 링크
https://statkclee.github.io/nlp2/regex-import-text.html  
https://wikidocs.net/33520  
https://ratsgo.github.io/from%20frequency%20to%20semantics/2017/03/11/embedding/  

# PDF to Text 변환
한글 문서의 경우 pdfminer 패키지를 사용하면 pdf를 텍스트로 변환할 수 있다.

# 단어 임베딩 – word2vec, GloVe, FastText
## word2vec
word2vec은 단어의 의미를 어떠한 벡터로 나타내어, 궁극적으로는 여러 단어 벡터 간에 유사도를 비교하는 등의 벡터 연산을 응용하는 것. 이러한 Word2Vec의 방식에는 CBOW와 Skip-gram 2가지가 있는데, 둘은 어떤 Sliding Window 안에서 주변 단어로 가운데 단어를 유추하는가, 혹은 가운데 단어로부터 주변 단어를 유추하는가의 차이. Python의 gensim 패키지 등에 구현됨.
## GloVe
글로브(Global Vectors for Word Representation, GloVe)는 카운트 기반과 예측 기반을 모두 사용하는 방법론으로 2014년에 미국 스탠포드대학에서 개발한 단어 임베딩 방법론. 앞서 학습하였던 기존의 카운트 기반의 LSA(Latent Semantic Analysis)와 예측 기반의 Word2Vec의 단점을 지적하며 이를 보완한다는 목적으로 나왔고, 실제로도 Word2Vec만큼 뛰어난 성능을 보여줌. 현재까지의 연구에 따르면 단정적으로 Word2Vec와 GloVe 중에서 어떤 것이 더 뛰어나다고 말할 수는 없고, 이 두 가지 전부를 사용해보고 성능이 더 좋은 것을 사용하는 것이 바람직함.
## FastText
페이스북에서 개발, gensim에 포함됨. 단어를 부분 단어의 벡터로 표현한다는 점 외에는 word2vec과 유사함.

# 파이썬 자연어 처리 라이브러리
## NLTK
말뭉치, 토큰 생성, 형태소 분석, 품사 태깅을 할 수 있는 파이썬 패키지
## koNLPy
한국어 형태소 분석/품사 태깅 등이 가능한 라이브러리.