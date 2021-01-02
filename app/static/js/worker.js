// ENDPOINTS

var URL_poll = "/poll";
var URL_update = "/update";


$(document).ready(function () {
    get_server_date();
});


function get_tableId() {
    let tableId = document.getElementById('tableId');
    if (typeof (tableId) != 'undefined' && tableId != null) {
        return $("#tableId").text()
    }
}


function load_table() {
    $("#contend").load("/table");
    setTimeout(get_server_date, 5000);
}


function call_update() {
    $.ajax({
        method: 'GET',
        url: URL_update,
        success: function (response) {
                console.log(response);
            if (response === 'error') {
                document.getElementById('statusbar').innerHTML = ('<a>' + response + '<a/>');
            } else {
                document.getElementById('statusbar').innerHTML = ('<a>' + response + '<a/>');
                load_table();
                // setTimeout(get_server_date, 5000);
            }
        }
    })
}


var OK = '<i class=\"fas fa-check fa-sm\" style=\"margin-left:20px; color:green\"></i>';
var UNKNOWN = '<i class=\"fas fa-question fa-sm\" style=\"margin-left:20px;color:yellow\"></i>';
var ERROR = '<i class=\"fas fa-exclamation fa-sm\" style=\"margin-left:20px;color:red\"></i>';
var LOADING = '<i class=\"fas fa-spinner fa-spin\" style=\"margin-left:20px\"></i>';

function get_server_date() {
    let tableId = get_tableId();
    $.ajax({
        method: 'GET',
        url: URL_poll,
        success: function (response) {
            let ServerTimestamp = response;
            if (ServerTimestamp === tableId) {
                console.log('ServerTimestamp:' + ServerTimestamp);
                console.log('tableId:' + tableId);
                document.getElementById('statusbar').innerHTML = ('<a>' + 'STATUS: OK' + '<a/>' + OK);
                setTimeout(get_server_date, 5000);

            } else if (ServerTimestamp === 'noFile') {
                console.log('ServerTimestamp:' + ServerTimestamp);
                document.getElementById('statusbar').innerHTML = ('<a>' + 'GAME NOT RUNNING' + '<a/>' + UNKNOWN);
                setTimeout(get_server_date, 5000);

            } else if (ServerTimestamp !== tableId) {
                console.log('ServerTimestamp:' + ServerTimestamp);
                console.log('tableId:' + tableId);
                document.getElementById('statusbar').innerHTML = ('<a>' + 'LOADING NEW DATA' + '<a/>' + LOADING);
                console.log('calling update');
                call_update();
            }
        }
    })
}