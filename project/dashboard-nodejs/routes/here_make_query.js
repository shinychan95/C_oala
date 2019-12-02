///////////////////////우리가 만들어야 할 데이터//////////////////////
//1. 학과별 논문수
//2. 연도별 논문수
//3. 학과별 키워드
//
//

var mysql = require('mysql');
var conn = mysql.createConnection({
    host            : '52.79.166.26',
    port            : 3306,
    user            : 'csed232',
    password        : 'csed232',
    database        : 'postech'
});

var sql = 'SELECT year FROM postech.nonmoon';


var exports = module.exports = {};

exports.qq = conn.query(sql, function(err, results){

    var yoman = new Object;
    var rows = results;
    var x = 0;

    rows.sort(function(a, b){
        return a.year < b.year ? -1 : a.year > b.year ? 1 : 0;
    })
    yoman.min = rows[0];
    yoman.gap = rows[-1] - rows[0];
    yoman.list = new Array();
    for(var i = 1; i < yoman.gap; i++){yoman.list[i] = 0;}
    yoman.list[0] = yoman.list[0] + 1;
    for(var i = 1; i < results.length; i++)
    {
        if(rows[i] > rows[i-1]){x++;}
        yoman.list[x] = yoman.list[x] + 1;
    }

    return yoman;
})