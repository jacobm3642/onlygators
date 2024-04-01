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

function get_creds() {
    username = $("#username").val();
    password = $("#password").val();
    return [username, password]
}

function write_login(html) {
    add_html(html);
    $("#loginBtn").bind("click", function () {
        post("./login", get_creds(), add_token)
    })
}

function login() {
    post("./getLogin", [], write_login);
}

function get_html(route, content=[]) {
    post(route, content, add_html);
}

function add_token(token) {
    localStorage.setItem('token', token);
}

function req_token() {
    return localStorage.getItem('token');
}

function del_token() {
    localStorage.removeItem('token');
}
