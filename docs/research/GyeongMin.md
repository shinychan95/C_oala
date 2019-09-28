REST API
=========
-----------
# REST란?
```
REST는 representational state transfer의 약자
어떤 자원이 잇으면 그 자원의 정보를 주고 받는 모든 것을 의미
(==자원의 represent에 의한 상태 전달)

저 요소별로 말하면
그 소프트웨어가 관리하는 모든 문서, 데이터 등을 자원이라고 한다.
represent는 자원들을 지칭하기 위한 이름이다. 데이터 중 성적이 있으면 'grade'를 represent로 정한다. 
상태 전달이란 데이터가 요청될 때 자원의 상태를 전달하는 것이다.
```
### 장점```
기존 HTTP 프로토콜과 웹의 기술들을 그대로 활용한다. 
>>웹(HTTP)의 장점을 활용할 수 있다.
>>별도로 인프라 구축이 필요 없다.
```
### 단점```
표준이 없다
사용할 수 있는 Method가 적다.
```

# REST 사용
HTTP URI(uniform resource identifier) - 자원 이름 정하기
HTTP Method - 해당 자원에 대한 CRUD Operation 적용하는 것.
CRUD Operation

Create | 생성 | Post
Read | 조회 | Get
Update | 수정 | Put
Delete | 삭제 | Delete
Head | header정보 조회 | Head
(맨 오른쪽 것은 HTTP method)


# REST가 돌아가는 법
모든 자원에는 고유 ID가 존재하고, 자원은 Server에 있다.
이 때 ID는 HTTP URI이다.
Client는 URI를 이용해 자원을 지정하고, 상태 조작을 server에 요청한다.

HTTP 프로토콜은 get, pos, put, delete같은 Method를 제공한다.

Client의 상태 조작 요청이 들어오면 server는 응답을 보낸다.
REST에서 하나의 자원은 여러 형태의 representation으로 표현된다.
```JSON- key/value의 형태를 가진 데이터 포맷
XML - markdown처럼 마크업 언어의 일종
RSS - markdown처럼 마크업 언어의 일종```




# API(application programming interface)
응용 프로그램 프로그래밍 인터페이스
앱에서 사용할 수 있도록, OS나 컴파일 언어가 제공하는 기능을 제어할 수 있게 만든 인터페이스


# REST API
REST를 기반으로 만든 API
HTTP를 기반으로 구현하기 떄문에, HTTP를 지원하는 언어를 사용
###리소스 원형들```
document - 객체시간에 배운 instance같은 거
컬렉션 - 서버에 있는 디렉터리
스토어 - 클라이언트에 있는 리소스 저장소
```
