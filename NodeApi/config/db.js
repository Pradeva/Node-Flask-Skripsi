const mysql = require('mysql')
const conn = mysql.createPool({
    host: 'localhost',
    user:'root',
    password:'',
    database:'kuliah',
    charset:'utf8mb4',
    timezone:'+07:00'
})

conn.getConnection((err) => {
    if (err) throw err
    console.log("DB CONNECTED!")
})

module.exports = conn