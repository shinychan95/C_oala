const express = require('express');
const { isLoggedIn, isNotLoggedIn } = require('./middlewares');

const router = express.Router();




var mysql = require('mysql');
var pool  = mysql.createPool({
  connectionLimit : 10,
  host            : '52.79.166.26',
  port            : 3306,
  user            : 'csed232',
  password        : 'csed232',
  database        : 'postech'
});


/* GET home page. */
var rake = "SELECT * FROM postech.RAKE;" //제일 처음 header에서 받아오던 데이터
var sql_1 = "SELECT * FROM postech.paper WHERE degree='Doctor' ORDER BY year DESC limit 10;"
var sql_2= "SELECT * FROM postech.paper WHERE degree='Master'ORDER BY year DESC limit 10;"



//서영 그래프 수정한 것
function get_total_number(responseData, res)
{
  //total year
  var sql = "SELECT year, COUNT(*) AS 'totalnum' FROM paper GROUP BY year order by year;";
  pool.query(sql, function(err,rows){
      if(err) throw err;
      if(rows){
        for(var i=0; i<rows.length; i++){
          responseData.year_num[i]=rows[i].totalnum;
        }
        get_ma_doc_number(responseData, res);
      }
      else{
        responseData.year_num = "";
      }
    });
}

  //doctor랑 master를 구분하여 배열에 넣음
function get_ma_doc_number(responseData, res){
  var sql = "SELECT degree, year, COUNT(year) AS 'num' FROM paper GROUP BY year, degree order by year;";
  pool.query(sql, function(err,rows){
    if(err) throw err;
    if(rows[0]){
      var year1=rows[0].year;
      for(var i=0; i<rows.length; i++)
      {
        if(rows[i].degree=='Doctor')
        {
          if(year1 != rows[i].year)
            {responseData.year_doctor.push(0); year1++}
          responseData.year_doctor.push(rows[i].num);
          year1++;
        }
        if(rows[i].degree=='Master')
        {
          responseData.year_master.push(rows[i].num);
        }
      }
      res.json(responseData); 
    }
    else
    {
      responseData.year_master = "";
    }
  });
}

router.get('/', isLoggedIn, (req, res) => {
  pool.query(sql_1, function(err1, results){
    pool.query(sql_2, function(err2, rows){
      pool.query(rake, function(err3, rake){
        res.render('pages/dashboard', {
          data:rake,
          doctor:results,
          master:rows,
          user:req.user,
        }); 
      })
    });
  });
});

router.post('/', function(req, res){
  var responseData = {};
  responseData.year = [];
  responseData.year_num = [];
  responseData.year_doctor = [];
  responseData.year_master = [];
  pool.query("SELECT DISTINCT year from postech.paper order by year ", (err,rows) => { 
    if(err) throw err;
    if(rows){
      for(var i=0; i<rows.length; i++){
        responseData.year[i] = rows[i].year;
      }
      get_total_number(responseData, res)
    }
    else{
      responseData.year = "";
    }
  })
});


router.get('/register', isNotLoggedIn, (req, res) => {
  res.render('pages/register', {
    title: '회원가입',
    user: req.user,
    joinError: req.flash('joinError'),
  });
});

router.get('/login', isNotLoggedIn, (req, res) => {
  res.render('pages/login',{
    user: req.user,
    loginError: req.flash('loginError'),
  });
});

router.get('/mysql', function (req, res) {
  var sql = 'select * from nonmoon';
  var rows;
  pool.query(sql, function (err, results) {
    if(err) {
      console.log(err);
      return;
    }
    rows = JSON.stringify(results);
    res.send(results);
  })

});



//여기부터 바꿈(경민)
router.get('/icons', (req, res) => {
  pool.query("select RAKE.*, crf.keyword As 'crf_keyword', TF_IDF.key1 AS 'tf_key1', TF_IDF.key2 AS 'tf_key2', TF_IDF.key3 AS 'tf_key3', TF_IDF.key4 AS 'tf_key4', TF_IDF.key5 AS 'tf_key5', paper.abstract from RAKE INNER JOIN crf join TF_IDF join paper ON RAKE.title = crf.title and crf.title = TF_IDF.title and crf.title = paper.title;", function(err, results){//RAKE crf, tf_idf의 모든 column이 다 필요함
    pool.query(rake, function(err3, rake){
      res.render('pages/icons', {results : results, data : rake, user: req.user});
    })
  });
});


var WCdata = [];//word frequency 데이터를 wordCloud에 넣을 형식으로 받을 배열을 선언.
router.get('/maps', (req, res) => {
  pool.query("select * from postech.WORD_FREQ", function(err, results){
    for(var i = 0; i < results.length; i++){
      WCdata[i] = {"x": results[i].word, "value": results[i].countss, category: "CSED"};//results에서 데이터를 받는다.
    }
    pool.query(rake, function(err3, rake){
      res.render('pages/maps', {WCdata : WCdata, data : rake, user: req.user})
    })
  });
});
//여기까지 바꿈(경민)

router.get('/tables', (req, res) => {
  pool.query(sql, function(err, results){
    res.render('pages/tables');
  });
});

router.get('/uploads', isLoggedIn, (req, res) => {
  res.render('pages/uploads', {user: req.user});
});



module.exports = router;
