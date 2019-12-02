var mooerhalga = require('./here_make_query');
var mooerhalga2 = mooerhalga.qq;

const express = require('express');

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
var sql = "SELECT * FROM postech.nonmoon limit 5";
pool.query(sql, function(err, results){
router.get('/', (req, res) => {
  res.render('pages/dashboard', {data : results, yoman : mooerhalga2});
  })
});




router.get('/mysql', function (req, res) {
  var sql = 'select * from paper';
  var rows;
  pool.query(sql, function (err, results) {
    if(err) {
      console.log(err);
      return;
    }
    rows = JSON.stringify(results);
    res.send(rows);
  })

});

router.get('/icons', (req, res) => {
  res.render('pages/icons');
});

router.get('/maps', (req, res) => {
  res.render('pages/maps');
});

router.get('/tables', (req, res) => {
  res.render('pages/tables');
});

module.exports = router;
