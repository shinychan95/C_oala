REST API
=========

## REST에 대한 설명
```
REST는 representational state transfer의 약자
어떤 자원이 잇으면 그 자원의 정보를 주고 받는 모든 것을 의미
(==자원의 represent에 의한 상태 전달)

저 요소별로 말하면
그 소프트웨어가 관리하는 모든 문서, 데이터 등을 자원이라고 한다.
represent는 자원들을 지칭하기 위한 이름이다. 데이터 중 성적이 있으면 'grade'를 represent로 정한다. 
상태 전달이란 데이터가 요청될 때 자원의 상태를 전달하는 것이다.
```
## API란?
application programming interface의 약자
API는 어떤 program이 다른 program과 정보와 신호를 주고받을 수 있게 해 주는 것이다.
주로 server와 client 간 대화를 할 수 있게 한다.

```
REST를 요약하자면?
REST는 API를 만들 때 개발자들이 지키는 set of rules이다.
```

#request를 구체적으로 알아 보자

request는 A가 B에 무언가를 요청하는 것. 이 때 A는 client, B는 server일 때가 많다
주로 4가지로 구성되어 있다.

------------------------
## endpoint
  사용자가 request를 하는 시작지점의 API
   ```
   ex) github의 API의 endpoint는 https://api.github.com
   ```
### path는 사용자가 요청한 자원이 무엇인지를 결정한다.
 
```  
ex) https://www.smashingmagazine.com/tag/javascript/에서
       https://www.smashingmagazine.com/는 API
       /tag/javascript 는 path
```

```      
/users/:username/repos에서 colon(:)은 변수 앞에 온다.
즉, username 안에 여러가지를 넣을 수 있다는 소리다.
```      
```      
?query1=value1&query2=value2에서 물음표는 query parameters 앞에 온다.
key-value 쌍을 수정하기 편하게 하려고 도입함.
```

### *cURL은 API 문서들을 읽을 때 주로 사용하는 command line utility이다.


## method
method는 server에 요청하는 request의 종류이다.
종류에는 get, post, put, patch, delete가 있다.
이들은 server에 가서 CRUD(create, read, update, delete)라는 연산으로 바뀐다.

```
get - server에서 리소스를 얻어올 때
post - server에 새 리소스를 create할 때
put & patch - server에 있는 리소스를 update할 때
delete - server에 있는 리소스를 삭제할 때
```



## headers(사실 이게 잘 이해가 안 됨)
  client와 server에게 정보를 제공할 때 쓰인다.
  property : value의 쌍으로 가운데에 colon을 써서 표현한다.
  그리고, 쓸 때는 앞에 curl -H 또는 curl --header을 써야 한다.
  


## data(body)
  data는 "post, put, patch, delete" request로만 다룰 수 있다. 
  body라고도 한다.

### curl로 data를 보내고 싶을 떄, -d 혹은 --data를 사용한다.
```
curl -X POST <URL> -d property1=value
```
### 두 개의 data를 보내고 싶으면 -d를 두 번 써야 한다.
```
curl -X POST <URL> -d property1=value1 -d property2=value2
```
### 이렇게도 쓸 수 있다.
```
curl -X POST <URL> \
  -d property1=value1 \
  -d property2=value2
```









