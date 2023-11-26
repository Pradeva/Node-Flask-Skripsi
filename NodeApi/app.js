const express = require('express')
const app = express()
const conn = require('./config/db')
const bodyParser = require('body-parser')

const CryptoJS = require('crypto-js')

const host = '192.168.1.12'
const port = 3000

app.use(bodyParser.json())

// GET
app.get('/get-mahasiswa', function (req, res) {
    const queryStr = "SELECT * FROM mahasiswa WHERE deleted_at IS NULL"
    conn.query(queryStr, (err, results) => {
        if (err) {
            console.log(err)
            res.status(500).json({
                "success": false,
                "message": err.sqlMessage,
                "data": null
            })
        } else {
            res.status(200).json({
                "success": true,
                "message": 'Sukses menampilkan data',
                "data": results
            })
        }
    })
})

// POST
app.post('/post-mahasiswa', function (req, res) {
    const param = req.body
    const name = param.name
    const jurusan = param.jurusan
    const now = new Date()

    const queryStr = "INSERT INTO mahasiswa (name, jurusan, created_at) VALUES (?, ?, ?)"
    const values = [name, jurusan, now]

    conn.query(queryStr, values, (err, results) => {
        if (err) {
            console.log(err)
            res.status(500).json({
                "success": false,
                "message": err.sqlMessage,
                "data": null
            })
        } else {
            res.status(200).json({
                "success": true,
                "message": "Sukses menyimpan data",
                "data": results
            })
        }
    })
})

// GET by id
app.get('/get-mahasiswa-by-id', function (req, res) {
    const param = req.query
    const id = param.id

    const queryStr = "SELECT * FROM mahasiswa WHERE deleted_at IS NULL AND id = ?"
    const values = [id]

    conn.query(queryStr, values, (err, results) => {
        if (err) {
            console.log(err)
            res.status(500).json({
                "success": false,
                "message": err.sqlMessage,
                "data": null
            })
        } else {
            res.status(200).json({
                "success": true,
                "message": "Sukses menampilkan data",
                "data": results
            })
        }
    })
})

// UPDATE
app.post('/update-mahasiswa', function (req, res) {
    const param = req.body
    const id = param.id
    const name = param.name
    const jurusan = param.jurusan

    const queryStr = "UPDATE mahasiswa SET name = ?, jurusan = ? WHERE id = ? AND deleted_at IS NULL"
    const values = [name, jurusan, id]

    conn.query(queryStr, values, (err, results) => {
        if (err) {
            console.log(err)
            res.status(500).json({
                "success": false,
                "message": err.sqlMessage,
                "data": null
            })
        } else {
            res.status(200).json({
                "success": true,
                "message": "Sukses update data",
                "data": results
            })
        }
    })
})

// ---------------------------------------------------------------------------------------

//REGISTER ACCOUNT
app.post('/add-account', function (req, res) {
    const param = req.body
    const Username = param.Username
    const Password = param.Password

    const encryptedPassword = (Password) => {
        return CryptoJS.enc.Base64.stringify(CryptoJS.enc.Utf8.parse(Password))
    }

    const queryStr = "INSERT INTO account (Username, Password) VALUES (?, ?)"

    const values = [Username, encryptedPassword(Password)] // Panggil encryptedPassword sebagai fungsi

    conn.query(queryStr, values, (err, results) => {
        if (err) {
            console.log(err)
            res.status(500).json({
                "success": false,
                "message": `Username ${Username} tidak tersedia`,
                "data": null
            })
        } else {
            res.status(200).json({
                "success": true,
                "message": "Sukses menyimpan data",
                "data": results
            })
        }
    })
})

//LOGIN
app.get('/login', function (req, res) {
    const param = req.body
    const Username = param.Username
    const Password = param.Password

    const encryptedPassword = (Password) => {
        return CryptoJS.enc.Base64.stringify(CryptoJS.enc.Utf8.parse(Password))
    }

    const queryStr = "SELECT * FROM account WHERE Username = ? AND Password = ?"
    const values = [Username, encryptedPassword(Password)]

    conn.query(queryStr, values,  (err, results) => {
        if (err) {
            console.log(err)
            res.status(500).json({
                "success": false,
                "message": err.sqlMessage,
                "data": null
            })
        } else {
            res.status(200).json({
                "success": true,
                "message": 'Sukses menampilkan data',
                "data": results
            })
        }
    })
})

app.listen(port, host, () => {
    console.log(`Server berjalan di http://${host}:${port}`);
  });
