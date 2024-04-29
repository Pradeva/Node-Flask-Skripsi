const express = require('express');
const bodyParser = require('body-parser');
const httpProxy = require('http-proxy');

const app = express();
const proxy = httpProxy.createProxyServer();

const port = 8001;
const host = '0.0.0.0';

// Middleware untuk mengurai body permintaan HTTP
app.use(bodyParser.json());

// Middleware untuk menangkap permintaan dan meneruskannya ke backend yang sesuai
app.all('/add-account', (req, res) => {
    proxy.web(req, res, { target: 'http://10.237.56.38:3000' });
});

app.all('/login', (req, res) => {
    proxy.web(req, res, { target: 'http://10.237.56.38:3000' });
});

app.all('/master/data/add', (req, res) => {
    proxy.web(req, res, { target: 'http://10.237.56.38:3000' });
});

app.all('/master/data/list/:account_id', (req, res) => {
    proxy.web(req, res, { target: 'http://10.237.56.38:3000' });
});

app.all('/master/data/delete/:data_id', (req, res) => {
    proxy.web(req, res, { target: 'http://10.237.56.38:3000' });
});

app.all('/master/NL/list/:data_id', (req, res) => {
    proxy.web(req, res, { target: 'http://10.237.56.38:3000' });
});

app.all('/master/NL/delete/:NL_id', (req, res) => {
    proxy.web(req, res, { target: 'http://10.237.56.38:3000' });
});

// ---------------------------------------------------------------
// Menangkap permintaan ke API Flask
app.all('/get/ner', (req, res) => {
    // Meneruskan permintaan ke server Flask yang berjalan di port 8001
    proxy.web(req, res, { target: 'http://10.237.56.38:8000' });
});


// Menangkap kesalahan jika terjadi
proxy.on('error', function (err, req, res) {
    // Menangani kesalahan yang terjadi saat meneruskan permintaan ke server Flask
    console.error(err);
    res.status(500).send('Proxy Error');
});


// Menjalankan server API Gateway
app.listen(port, host, () => {
    console.log(`Server berjalan di http://${host}:${port}`);
});
