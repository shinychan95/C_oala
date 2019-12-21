## Installation

1. You need `Node.js` (at least 10.x version) installed on your machine, if you don't have it, you should install it - download [link](https://nodejs.org/en/download/)
2. `cd` to Dashboard folder
4. Install necessary dependencies:
    - **Via node `npm` package manager** - Run `npm install` on the project root
    - **Via `yarn` package manager** - Run `yarn install` on the project root
    - **module들을 설치하는데 git이 필수이므로 git이 사전에 설치되어 있어야 한다.**

## Configuration for MySQL database
현재 MySQL Config가 프로젝트를 진행하면서 사용했던 AWS EC2로 설정되어 있는데, 계속 열려 있으므로 설정을 우선 그대로 두면 된다.


## Run the application

1. For starting the application, the following script (defined in `package.json` under `scripts`) must be called:
    - via **npm**: `npm run start` or `npm run dev` for starting the development environment, which has livereload enabled;
    - via **yarn**: `yarn start` or `yarn dev` for starting the development environment, which has livereload enabled;


## Usage

Register a user or login using **admin@argon.com**:**secret** and start testing the preset (make sure to run the migrations and seeds for these credentials to be available).

Besides the dashboard and the auth pages this preset also has an edit profile page.
**NOTE**: _Keep in mind that all available features can be viewed once you login using the credentials provided above or by registering your own user._


## For the Front-end side:

##### Templates

- You can find all the templates in `views` folder where you will find:
1. The `layout.ejs` file, the main template layout.
2. A `pages` folder with all the page templates
3. A `partials` folder with the common components (header, footer, sidebar)



## File Structure

```
├── README.md **작업한 것**
├── app.js **작업한 것**
├── bin
│   └── www **작업한 것**
├── config
│   └── config.json **작업한 것**
├── env-files
│   └── development.env **작업한 것**
├── gulpfile.js
├── haproxy.cfg
├── logger.js
├── package.json
├── public
│   ├── css
│   │   ├── argon.css
│   │   └── argon.min.css
│   ├── fonts
│   │   └── nucleo
│   ├── img
│   │   ├── brand
│   │   ├── icons
│   │   └── theme
│   ├── js
│   │   ├── argon.js
│   │   └── argon.min.js
│   ├── scss
│   │   ├── argon.scss
│   │   ├── bootstrap
│   │   ├── core
│   │   └── custom
│   └── vendor
├── models
│   ├── index.js **작업한 것**
│   └── user.js **작업한 것**
├── passport
│   ├── index.js **작업한 것**
│   ├── kakaoStrategy.js **작업한 것**
│   └── localStrategy.js **작업한 것**
├── routes
│   ├── auth.js **작업한 것**
│   ├── file.js **작업한 것**
│   ├── index.js **작업한 것**
│   └── middlewares.js **작업한 것**
├── uploads **작업한 것**
├── views
│   ├── layout.ejs
│   ├── pages
│   │   ├── 404.ejs
│   │   ├── dashboard.ejs **작업한 것**
│   │   ├── icons.ejs **작업한 것**
│   │   ├── login.ejs **작업한 것**
│   │   ├── maps.ejs **작업한 것**
│   │   ├── profile.ejs
│   │   ├── register.ejs
│   │   ├── reset-password.ejs
│   │   ├── tables.ejs
│   │   └── uploads.ejs **작업한 것**
│   └── partials
│       ├── auth
│       │   ├── footer.ejs
│       │   ├── header.ejs
│       │   └── navbar.ejs
│       ├── dropdown.ejs **작업한 것**
│       ├── footer.ejs **작업한 것**
│       ├── header.ejs **작업한 것**
│       ├── navbar.ejs **작업한 것**
│       └── sidebar.ejs **작업한 것**
└
```


## Resources
- Demo: <https://argon-dashboard-nodejs.creative-tim.com/?ref=adn-readme>
- Download Page: <https://www.creative-tim.com/product/argon-dashboard-nodejs?ref=adn-readme>
- Documentation: <https://argon-dashboard-nodejs.creative-tim.com/docs/getting-started/overview.html?ref=adn-readme>
- License Agreement: <https://www.creative-tim.com/license>
- Support: <https://www.creative-tim.com/contact-us>
- Issues: [Github Issues Page](https://github.com/creativetimofficial/argon-dashboard-nodejs/issues)
- **Dashboards:**
| HTML | NODEJS |
| --- | --- |
| [![Argon Dashboard HTML](https://s3.amazonaws.com/creativetim_bucket/products/96/original/opt_ad_thumbnail.jpg)](https://demos.creative-tim.com/argon-dashboard/index.html?ref=adn-readme) | [![Argon Dashboard Node](https://s3.amazonaws.com/creativetim_bucket/products/148/original/opt_ad_node_thumbnail.jpg)](https://argon-dashboard-nodejs.creative-tim.com/?ref=adn-readme)


## License

[MIT License](https://github.com/laravel-frontend-presets/argon/blob/master/license.md).



## Useful Links

- [Tutorials](https://www.youtube.com/channel/UCVyTG4sCw-rOvB9oHkzZD1w)
- [Affiliate Program](https://www.creative-tim.com/affiliates/new) (earn money)
- [Blog Creative Tim](http://blog.creative-tim.com/)
- [Free Products](https://www.creative-tim.com/bootstrap-themes/free) from Creative Tim
- [Premium Products](https://www.creative-tim.com/bootstrap-themes/premium?ref=adn-readme) from Creative Tim
- [React Products](https://www.creative-tim.com/bootstrap-themes/react-themes?ref=adn-readme) from Creative Tim
- [Angular Products](https://www.creative-tim.com/bootstrap-themes/angular-themes?ref=adn-readme) from Creative Tim
- [VueJS Products](https://www.creative-tim.com/bootstrap-themes/vuejs-themes?ref=adn-readme) from Creative Tim
- [More products](https://www.creative-tim.com/bootstrap-themes?ref=adn-readme) from Creative Tim
- Check our Bundles [here](https://www.creative-tim.com/bundles??ref=adn-readme)




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