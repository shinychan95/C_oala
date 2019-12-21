const express = require('express');
const path = require('path');
const expressLayouts = require('express-ejs-layouts');
const cookieParser = require('cookie-parser');
const morgan = require('morgan');
const flash = require('connect-flash');
const session = require('express-session');
const MySQL = require('express-mysql-session')(session);
const passport = require('passport');
require('dotenv').config();

const pageRouter = require('./routes/index');
const authRouter = require('./routes/auth');
const fileRouter = require('./routes/file');
const { sequelize } = require('./models');
const passportConfig = require('./passport');
const indexRouter = require('./routes');

const MySQLStoreConfig = {
  host: '52.79.166.26',
  port: 3306,
  database: 'postech',
  user: 'csed232',
  password: 'csed232'
};


const sessionStore = new MySQL(MySQLStoreConfig);   

const staticFolder = process.env.NODE_ENV === 'development' ? 'public' : 'dist';
const app = express();

sequelize.sync();
passportConfig(passport);

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
app.set('port', process.env.PORT || 8001);

app.use(expressLayouts);
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser(process.env.COOKIE_SECRET));
app.use(express.static(path.join(__dirname, staticFolder)));

const { COOKIE_EXPIRATION_MS } = process.env;
app.use(
  session({
    store: sessionStore,
    secret: process.env.COOKIE_SECRET,
    name: process.env.SESSION_COOKIE_NAME,
    resave: false,
    saveUninitialized: true,
    cookie: {
      httpOnly: true,
      secure: false,
      expires: Date.now() + parseInt(COOKIE_EXPIRATION_MS, 10),
      maxAge: parseInt(COOKIE_EXPIRATION_MS, 10),
    },
  })
);

app.use(flash());

// initAuthMiddleware(app);

// Middleware used for setting error and success messages as available in _ejs_ templates
app.use((err, req, res, next) => {
  if (req.session) {
    res.locals.messages = req.session.messages;
    res.locals.userInfo = req.session.userInfo;
    res.locals.error = req.app.get('env') === 'development' ? err : {};
    res.status(err.status || 500);
    res.render('error');  
  }
  next();
});

app.use(passport.initialize());
app.use(passport.session());

app.use('/', pageRouter);
app.use('/auth', authRouter);
app.use('/files', fileRouter);



// catch 404 and forward to error handler
app.use((req, res) => {
  res.status(404).render('pages/404');
});


module.exports = app;
