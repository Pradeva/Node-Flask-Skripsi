const express = require('express')
const app = express()
const conn = require('./config/db')
const bodyParser = require('body-parser')

const CryptoJS = require('crypto-js')

const host = '0.0.0.0'
const port = 3000

app.use(bodyParser.json())

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
app.post('/login', function (req, res) {
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
            if (results.length === 0) {
                res.status(200).json({
                    "success": false,
                    "message": 'Data tidak ada',
                    "data": results
                })
            } else {
                res.status(200).json({
                    "success": true,
                    "message": 'Sukses menampilkan data',
                    "data": results
                })
            }
            
        }
    })
})

// MASTER DATA

// CREATE DATA

app.post('/master/data/add', function (req, res) {
    const param = req.body
    const account_id = param.account_id
    const name = param.name
    const description = param.description


    const queryStr = "INSERT INTO data (account_id, name, description) VALUES (?, ?, ?)"

    const values = [account_id, name, description] // Panggil encryptedPassword sebagai fungsi

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

// READ DATA

app.get('/master/data/list/:account_id', function (req, res) {
    const param = req.params
    const account_id = param.account_id


    const queryStr = "SELECT * FROM data WHERE account_id = ? AND deleted_at IS NULL"
    const values = [account_id]

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

// DELETE DATA
app.post('/master/data/delete/:data_id', function (req, res) {
    const param = req.params
    const data_id = param.data_id

    const currentDate = new Date();

    // Mendapatkan tanggal dalam format YYYY-MM-DD
    const currentDateString = currentDate.toISOString().split('T')[0];

    // Mendapatkan waktu dalam format HH:MM:SS
    const currentTimeString = currentDate.toTimeString().split(' ')[0];

    // Mendapatkan tanggal dan waktu dalam format YYYY-MM-DD HH:MM:SS
    const currentDateTimeString = currentDateString + ' ' + currentTimeString;

    const queryStr = "UPDATE data SET deleted_at = ? WHERE id = ?"
    const values = [currentDateTimeString, data_id]

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
                "message": "Sukses hapus data",
                "data": results
            })
        }
    })
})

// MATER NATURAL LANGUAGE

// GET NATURAL LANGUAGE

app.get('/master/NL/list/:data_id', function (req, res) {
    const param = req.params
    const data_id = param.data_id


    const queryStr = "SELECT * FROM natural_language WHERE data_id = ? AND deleted_at IS NULL"
    const values = [data_id]

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

//DELETE NATURAL LANGUAGE
app.post('/master/NL/delete/:NL_id', function (req, res) {
    const param = req.params
    const NL_id = param.NL_id

    const currentDate = new Date();

    // Mendapatkan tanggal dalam format YYYY-MM-DD
    const currentDateString = currentDate.toISOString().split('T')[0];

    // Mendapatkan waktu dalam format HH:MM:SS
    const currentTimeString = currentDate.toTimeString().split(' ')[0];

    // Mendapatkan tanggal dan waktu dalam format YYYY-MM-DD HH:MM:SS
    const currentDateTimeString = currentDateString + ' ' + currentTimeString;

    const queryStr = "UPDATE natural_language SET deleted_at = ? WHERE id = ?"
    const values = [currentDateTimeString, NL_id]

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
                "message": "Sukses hapus data",
                "data": results
            })
        }
    })
})

app.post('/master/NL/add', function (req, res) {
    const param = req.body
    const id_data = param.id_data
    const condition = param.condition
    const action = param.action


    const queryStr = "INSERT INTO natural_language (data_id, kondisi, aksi) VALUES (?, ?, ?)"

    const values = [id_data, condition, action] // Panggil encryptedPassword sebagai fungsi

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

app.listen(port, host, () => {
    console.log(`Server berjalan di http://${host}:${port}`);
});

// GET
// app.get('/get-mahasiswa', function (req, res) {
//     const queryStr = "SELECT * FROM mahasiswa WHERE deleted_at IS NULL"
//     conn.query(queryStr, (err, results) => {
//         if (err) {
//             console.log(err)
//             res.status(500).json({
//                 "success": false,
//                 "message": err.sqlMessage,
//                 "data": null
//             })
//         } else {
//             res.status(200).json({
//                 "success": true,
//                 "message": 'Sukses menampilkan data',
//                 "data": results
//             })
//         }
//     })
// })

// // POST
// app.post('/post-mahasiswa', function (req, res) {
//     const param = req.body
//     const name = param.name
//     const jurusan = param.jurusan
//     const now = new Date()

//     const queryStr = "INSERT INTO mahasiswa (name, jurusan, created_at) VALUES (?, ?, ?)"
//     const values = [name, jurusan, now]

//     conn.query(queryStr, values, (err, results) => {
//         if (err) {
//             console.log(err)
//             res.status(500).json({
//                 "success": false,
//                 "message": err.sqlMessage,
//                 "data": null
//             })
//         } else {
//             res.status(200).json({
//                 "success": true,
//                 "message": "Sukses menyimpan data",
//                 "data": results
//             })
//         }
//     })
// })

// // GET by id
// app.get('/get-mahasiswa-by-id', function (req, res) {
//     const param = req.query
//     const id = param.id

//     const queryStr = "SELECT * FROM mahasiswa WHERE deleted_at IS NULL AND id = ?"
//     const values = [id]

//     conn.query(queryStr, values, (err, results) => {
//         if (err) {
//             console.log(err)
//             res.status(500).json({
//                 "success": false,
//                 "message": err.sqlMessage,
//                 "data": null
//             })
//         } else {
//             res.status(200).json({
//                 "success": true,
//                 "message": "Sukses menampilkan data",
//                 "data": results
//             })
//         }
//     })
// })

// // UPDATE
// app.post('/update-mahasiswa', function (req, res) {
//     const param = req.body
//     const id = param.id
//     const name = param.name
//     const jurusan = param.jurusan

//     const queryStr = "UPDATE mahasiswa SET name = ?, jurusan = ? WHERE id = ? AND deleted_at IS NULL"
//     const values = [name, jurusan, id]

//     conn.query(queryStr, values, (err, results) => {
//         if (err) {
//             console.log(err)
//             res.status(500).json({
//                 "success": false,
//                 "message": err.sqlMessage,
//                 "data": null
//             })
//         } else {
//             res.status(200).json({
//                 "success": true,
//                 "message": "Sukses update data",
//                 "data": results
//             })
//         }
//     })
// })