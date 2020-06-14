// document.getElementById('comment').innerHTML = 'test';
// import CryptoJS from 'node_modules/crypto-js';
// import * as CryptoJS from 'node_modules/crypto-js';

// var CryptoJS = require('crypto-js');

// require('crypto-js')
console.log('HELLO MAIN.JS1')

var pwd = "password";

function Encrypt(word) {
    // return CryptoJS.AES.encrypt(word, pwd).toString();
    return String(CryptoJS.AES.encrypt(word, pwd));
}

function Decrypt(word) {
    // return CryptoJS.AES.decrypt(word, pwd).toString(CryptoJS.enc.Utf8);
    return CryptoJS.AES.decrypt(word, pwd).toString(CryptoJS.enc.Utf8);
}

// var origin = 'test';
// console.log(origin);
// var mm = Encrypt(origin);
// console.log(mm);
//
// var jm = Decrypt(mm);
// console.log(jm);
// document.querySelector('comment').text = jm

// var Crypto = require('cryptojs');
// Crypto = Crypto.Crypto;

var KEY = 'This is a key123';
var IV = 'This is an IV456';
var MODE = new CryptoJS.mode.CFB(CryptoJS.pad.ZeroPadding);

var plaintext = 'The answer is no';
var input_bytes = Crypto.charenc.UTF8.stringToBytes(plaintext);
var key = Crypto.charenc.UTF8.stringToBytes(KEY);
var options = {iv: Crypto.charenc.UTF8.stringToBytes(IV), asBytes: true, mode: MODE};
var encrypted = Crypto.AES.encrypt(input_bytes, key, options);
var encrypted_hex = Crypto.util.bytesToHex(encrypted);
console.log(encrypted_hex); // this is the value you send over the wire

output_bytes = Crypto.util.hexToBytes(encrypted_hex);
output_plaintext_bytes = Crypto.AES.decrypt(output_bytes, key, options);
output_plaintext = Crypto.charenc.UTF8.bytesToString(output_plaintext_bytes);
console.log(output_plaintext); // result: 'The answer is no'
