function addItemToTable(content) {

}

function displayError(content) {
    alert("error")
    divTag = document.getElementById("errors")
    errors = content.split(";")
    errorsFormated = ""
    for e in errors {
        errorsFormated += "<span style='font-size:150%;margin-left: 30px'>" + e + "</span><br>"
    }
    divTag.innerHTML =
        "<div class='alert alert-danger' style='text-align: left'>"
        + "<img src='/static/images/error.png' height='55px'>"
        + "<strong style='font-size:150%;margin-left: 20px'>ERROR!</strong>"
        + errorsFormated
        + "</div>"
}

function addItem() {
    alert("start")
    var buyer = document.getElementById("buyer").value;
    var what = document.getElementById("what").value;
    var price = document.getElementById("price").value;

    alert(buyer + what + price)

    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState != 4)
            return;
        content = xhttp.responseText
        if (this.status == 200)
            addItemToTable(content);
        else if (this.status == 409)
            displayError(content)
    }
    xhttp.open("POST", "/month");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    alert("sending")
    xhttp.send(
        "action=add&" +
        "buyer=" + encodeURI(buyer) + "&" +
        "what=" + encodeURI(what) + "&" +
        "price=" + encodeURI(price)
    )
}