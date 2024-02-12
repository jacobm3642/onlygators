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
