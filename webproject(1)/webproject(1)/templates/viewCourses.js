


    // console.log();
    var mysql = require('mysql2');

var con = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "arsalHussain#10",
  database: "educateme"
});

function getResult(){
con.connect(function(err) {
  if (err) throw err;
  con.query("SELECT * FROM courses", function (err, result, fields) {
    // if (err) throw err;
    return result
  });
})
}

module.exports= getResult();

