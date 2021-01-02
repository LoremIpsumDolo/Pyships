function get_log() {
    $.post("/status", {
            request: "get_log"
        },
        function (response, status) {
            console.log(response);
            document.getElementById('LogBox').innerHTML = ("");
            $.each(response, function (k, v) {
                document.getElementById('LogBox').innerHTML += ('<ul>' + k + ':	' + v + '</ul>')
            });
        });
}

function update_database() {
    $("#database_status").removeClass("green");
    $("#database_status").removeClass("red");
    $.post("/update_db", {
            request: "update_db"
        },
        function (response, status) {
            console.log(response);
            if (response === 'invalid') {
                document.getElementById('database_status').innerHTML = (response);
                $("#database_status").addClass("green");
            } else {
                document.getElementById('database_status').innerHTML = (response);
                $("#database_status").addClass("red");
            }
        });
}


function get_status() {
    $.post("/status", {
            request: "get_status"
        },
        function (response, status) {
            let AppID_status = response['AppId'];
            let ReplayDir_status = response['ReplayDir'];
            let db_status = response['DB_Version'];
            console.log(response);

            if (ReplayDir_status === 'valid') {
                document.getElementById('ReplayDirstatus').innerHTML = (ReplayDir_status);
                $("#ReplayDirstatus").addClass("setting-green");
            } else {
                document.getElementById('ReplayDirstatus').innerHTML = (ReplayDir_status);
                $("#ReplayDirstatus").addClass("setting-red");
            }

            if (AppID_status === 'valid') {
                document.getElementById('AppIDstatus').innerHTML = (AppID_status);
                $("#AppIDstatus").addClass("setting-green");
            } else {
                document.getElementById('AppIDstatus').innerHTML = (AppID_status);
                $("#AppIDstatus").addClass("setting-red");
            }

            if (db_status === 'valid') {
                document.getElementById('database_status').innerHTML = (db_status);
                $("#database_status").addClass("setting-green");
            } else {
                document.getElementById('database_status').innerHTML = (db_status);
                $("#database_status").addClass("setting-red");
            }
        });
}

//
// validate_ReplayDir
//

function validate_ReplayDir() {
    $("#ReplayDirstatus").removeClass("setting-green");
    $("#ReplayDirstatus").removeClass("setting-red");
    $("#validate_ReplayDirButton").hide();
    document.getElementById('ReplayDirstatus').innerHTML = ("Checking...");

    let inputValue = $('#ReplayDir').val();
    $.post("/ReplayDir", {
            request: "validate_ReplayDir",
            value: inputValue
        },
        function (response, status) {
            console.log(response);
            if (response === 'valid') {
                document.getElementById('ReplayDirstatus').innerHTML = ("valid");
                $("#save_ReplayDirButton").show();
                $("#ReplayDirstatus").addClass("setting-green");
            } else {
                document.getElementById('ReplayDirstatus').innerHTML = ("invalid");
                $("#validate_ReplayDirButton").show();
                $("#ReplayDirstatus").addClass("setting-red");
                $('input[type="text"],textarea').val('');
            }
        });
}

//
// save_ReplayDir
//

function save_ReplayDir() {
    $("#ReplayDirstatus").removeClass("setting-green");
    $("#ReplayDirstatus").removeClass("setting-red");
    $("#save_ReplayDirButton").hide();
    document.getElementById('ReplayDirstatus').innerHTML = ("saving...");

    let inputValue = $('#ReplayDir').val();
    $.post("/ReplayDir", {
            request: "save_ReplayDir",
            value: inputValue
        },
        function (response, status) {
            console.log(response);
            if (response === 'valid') {
                document.getElementById('ReplayDirstatus').innerHTML = ("saved");
                $("#validate_ReplayDirButton").show();
                $("#ReplayDirstatus").addClass("setting-green");
                $('input[type="text"],textarea').val('');
                get_log();
            } else {
                document.getElementById('ReplayDirstatus').innerHTML = ("invalid");
                $("#validate_ReplayDirButton").show();
                $("#ReplayDirstatus").addClass("setting-red");
                $('input[type="text"],textarea').val('');
            }
        });
}

//
// validate_AppID
//

function validate_AppID() {
    $("#AppIDstatus").removeClass("setting-green");
    $("#AppIDstatus").removeClass("setting-red");
    $("#validate_AppIDButton").hide();
    document.getElementById('AppIDstatus').innerHTML = ("Checking...");

    let inputValue = $('#AppID').val();
    $.post("/AppID", {
            request: "validate_AppID",
            value: inputValue
        },
        function (response, status) {
            console.log(response);
            if (response === 'valid') {
                document.getElementById('AppIDstatus').innerHTML = ("valid");
                $("#save_AppIDButton").show();
                $("#AppIDstatus").addClass("setting-green");
            } else {
                document.getElementById('AppIDstatus').innerHTML = (response);
                $("#validate_AppIDButton").show();
                $("#AppIDstatus").addClass("setting-red");
                $('input[type="text"],textarea').val('');
            }
        });
}

//
// save_AppID
//

function save_AppID() {
    $("#AppIDstatus").removeClass("setting-green");
    $("#AppIDstatus").removeClass("setting-red");
    $("#save_AppIDButton").hide();
    document.getElementById('AppIDstatus').innerHTML = ("saving...");

    let inputValue = $('#AppID').val();
    $.post("/AppID", {
            request: "save_AppID",
            value: inputValue
        },
        function (response, status) {
            console.log(response);
            if (response === 'valid') {
                document.getElementById('AppIDstatus').innerHTML = ("saved");
                $("#save_AppIDButton").show();
                $("#AppIDstatus").addClass("setting-green");
                $('input[type="text"],textarea').val('');
                get_log();
            } else {
                document.getElementById('AppIDstatus').innerHTML = (response);
                $("#validate_AppIDButton").show();
                $("#AppIDstatus").addClass("setting-red");
                $('input[type="text"],textarea').val('');
            }
        });
}