function sendData(product_id) {
    var bttn = document.getElementById("submitButton");
    var url_ = '/product/add/' + product_id;
    $.ajax({
        type: "GET",
        url: url_,
        data: {
            "value": $('div.active').index(),
        },
        dataType: "json",
        success: function (data) {
            // any process in data
            alert("successfull")
        },
        failure: function () {
            alert("failure");
        }
    });
}