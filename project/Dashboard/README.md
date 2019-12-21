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