function post(route, jsonData, successCallback, errorCallback) {
    var jsonDataString = JSON.stringify(jsonData);

    $.ajax({
        url: "http://127.0.0.1:5000/" + route,
        method: "POST",
        data: jsonDataString,
        contentType: "application/json",
        success: function(data) {
            if (successCallback) {
                successCallback(data);
            }
        },
        error: function(xhr, status, error) {
            if (errorCallback) {
                errorCallback(xhr.responseText);
            } else {
                alert("Error: " + xhr.responseText);
            }
        }
    });
}

function add_html(html) {
    $('#working').html(html);
}

function get_creds(email=0) {
    out = []
    if (email == 1) {
        out.push($("#email").val());
    }
    out.push($("#username").val());
    out.push($("#password").val());
    return out
}

function write_login(html) {
    add_html(html);
    $("#loginBtn").bind("click", function () {
        post("./login", get_creds(), add_token)
    })
}

function getLogin() {
    post("./getLogin", [], write_login);
}

function write_register(html) {
    add_html(html);
    $("#registerBtn").bind("click", function () {
        post("./register", get_creds(1), add_token)
    })
}

function getRegister() {
    post("./getRegister", [], write_register)
}

function get_html(route, content=[]) {
    post(route, content, add_html);
}

function add_token(token) {
    localStorage.setItem('token', token);
    add_html("");
    
}

function req_token() {
    return localStorage.getItem('token');
}

function del_token() {
    localStorage.removeItem('token');
}
