# C_oala
CSED232 OOP Team Project<br>
**텍스트마이닝을 활용한 대시보드 개발**

## Team Member

|Name|Role|Passion|GitHub ID|Special|
|----|----|-------|---------|-------|
|김찬영|조장|High|shinychan95|18학점+수영+유급연구참여+스터디+내리사랑|
|김진모|미정|High|JinmiKIM1012|19학점+UGRP+동아리3개+BUSY사랑|
|엄태규|미정|Hidium|yongs118|17학점+고기사랑|
|이상윤|미정|High|lyunm1206|14학점+애드립+중집위+연기사랑|
|최서영|미정|High|seoyeong74|21학점+한울림+오케스트라+음악사랑|
|하경민|미정|High|edrakin|19학점+POSCAT+알골즘사랑(?)|


## Meeting Date and Time

```
Weekly : Tuesday 12:15 ~ 13:15
```

## Role
- 김찬영: 조장, 전체적인 프로그램 구조 설계 및 개발, 서버 개발 
- 최서영: 프론트 개발, 웹 개발, 페이지 기능 및 구조 설계
- 하경민: API 서버 개발, 데이터베이스 설계 및 개발
- 이상윤: 텍스트마이닝 관련 알고리즘 개발. 전처리 프로세스 설계 및 개발
- 엄태규: 텍스트마이닝 관련 알고리즘 개발. 전처리 프로세스 설계 및 개발
- 김진모: 텍스트마이닝 관련 알고리즘 개발. 전처리 프로세스 설계 및 개발


## Materials
- [github 사용법](https://milooy.wordpress.com/2017/06/21/working-together-with-github-tutorial/)
- [웹 개발, 프론트 백 풀스택 개발자](https://medium.com/code-states/%EA%B0%9C%EB%B0%9C%EC%9E%90-%EC%A7%81%EA%B5%B0-%ED%8C%8C%ED%97%A4%EC%B9%98%EA%B8%B0-1-%ED%94%84%EB%A1%A0%ED%8A%B8-front-%EB%B0%B1-back-%ED%92%80%EC%8A%A4%ED%83%9D-full-stack-%EA%B0%9C%EB%B0%9C%EC%9E%90-f6c2f53e5b3b)
- [게임 개발자](https://medium.com/code-states/%EA%B0%9C%EB%B0%9C%EC%9E%90-%EC%A7%81%EA%B5%B0-%ED%8C%8C%ED%97%A4%EC%B9%98%EA%B8%B0-2-%EA%B2%8C%EC%9E%84-%EA%B0%9C%EB%B0%9C%EC%9E%90-9d1898d12f3f)
- [블록체인 개발자](https://medium.com/code-states/%EA%B0%9C%EB%B0%9C%EC%9E%90-%EC%A7%81%EA%B5%B0-%ED%8C%8C%ED%97%A4%EC%B9%98%EA%B8%B0-3-%EB%B8%94%EB%A1%9D%EC%B2%B4%EC%9D%B8-%EA%B0%9C%EB%B0%9C%EC%9E%90-9d7b2840ff6f)


## Objectives
* Fun


## File Structure in Project Folder

```
├── Algorithm
│   ├── stoplist **단어 처리할 때 불용어 모음**
│   ├── CRF.py **CRF keyword Extraction 코드, DB에서 데이터 가져와서 알고리즘 적용 후 DB 저장**
│   ├── LDA.py **LDA keyword Extraction 코드, DB에서 데이터 가져와서 알고리즘 적용 후 DB 저장**
│   ├── Rake.py **Rake keyword Extraction 코드, DB에서 데이터 가져와서 알고리즘 적용 후 DB 저장**
│   ├── TFIDF.py **TFIDF keyword Extraction 코드, DB에서 데이터 가져와서 알고리즘 적용 후 DB 저장**
│   └── WF.py **WF keyword Extraction 코드, DB에서 데이터 가져와서 알고리즘 적용 후 DB 저장**
├── Dashboard
│   ├── README.md **프로그램 실행을 위해 읽어야 할 파일**
│   ├── app.js **서버의 설정을 담아놓은 파일이라고 생각하면 된다. 웹 어플리케이션 서버에 설정할 모듈을 포함시키면 된다.**
│   ├── bin
│   │   └── www **main 함수가 담겨있는 파일이라고 생각하면 된다. www에서 프로젝트를 실행해야한다.**
│   ├── config
│   │   └── config.json **DB Config**
│   ├── env-files
│   │   └── development.env **DB Config**
│   ├── gulpfile.js
│   ├── haproxy.cfg
│   ├── logger.js
│   ├── package.json **프로젝트가 어떤 모듈에 의존성을 가지는 지 정리해둔 파일**
│   ├── public **서버가 public으로 제공할 정적 파일들, 예를 들어 js파일, css파일, 이미지 파일 등을 저장해놓는 디렉토리**
│   ├── models
│   │   ├── index.js **DB 모델. sequence 모듈을 통해 서버 실행 시 DB를 자동으로 만든다.**
│   │   └── user.js **user DB 속성이 담긴 코드**
│   ├── passport **로그인 모듈 시 인증으로써 필요한 기능. 프로토콜 메세지 내 passport가 담겨 인증에 이용된다.**
│   │   ├── index.js 
│   │   ├── kakaoStrategy.js **카카오 로그인의 경우 passport-kakao 모듈을 이용하여 카카오 passport 구현**
│   │   └── localStrategy.js 
│   ├── routes **서버가 라우팅 할 url path에 대한 로직들을 저장해놓는 디렉ㅌ호리**
│   │   ├── auth.js **로그인 및 로그아웃에 대해서 POST 호출이 들어올 때 처리하는 로직이 담겨 있다.**
│   │   ├── file.js **사용자가 웹 페이지 내에서 PDF 파일을 업로드 할 때 파일을 저장하고 자동으로 파이썬 코드를 실행하도록 하는 파일**
│   │   ├── index.js **전체적인 라우터 기능을 담고 있는 파일**
│   │   └── middlewares.js **로그인 되었는지 아닌지에 따라 처리해주는 함수가 담긴 파일**
│   ├── uploads **PDF 업로드 시 임시로 머무는 폴더**
│   └── views **서버가 렌더링하는 템플릿들을 저장해놓는 디렉토리**
│       ├── layout.ejs
│       ├── pages
│       │   ├── 404.ejs
│       │   ├── dashboard.ejs **작업한 것**
│       │   ├── icons.ejs **작업한 것**
│       │   ├── login.ejs **작업한 것**
│       │   ├── maps.ejs **작업한 것**
│       │   ├── profile.ejs
│       │   ├── register.ejs
│       │   ├── reset-password.ejs
│       │   ├── tables.ejs
│       │   └── uploads.ejs **작업한 것**
│       └── partials
│           ├── auth
│           │   ├── footer.ejs
│           │   ├── header.ejs
│           │   └── navbar.ejs
│           ├── dropdown.ejs **작업한 것**
│           ├── footer.ejs **작업한 것**
│           ├── header.ejs **작업한 것**
│           ├── navbar.ejs **작업한 것**
│           └── sidebar.ejs **작업한 것**
├── DataPreprocessing
│   ├── exception **60개의 논문 중 처리되지 않는 논문들**
│   ├── input **input으로 들어가는 논문 PDF**
│   └── pre_processing.py **전처리하는 코드. 논문을 TEXT로 바꾸고 DB에 저장**
└
```
