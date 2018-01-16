function removeErrors() {
    document.getElementById("errors").innerHTML = ""
}

function displayErrors(rawErrors) {
    var divTag = document.getElementById("errors");
    var errors = rawErrors.split(";");
    var errorsFormatted = "";
    for (var i = 0; i < errors.length; i++) {
        errorsFormatted += "<span style='font-size:150%;margin-left: 30px'>" + errors[i] + "</span><br>"
    }
    divTag.innerHTML =
        "<div class='alert alert-danger' style='text-align: left; margin-top: 30px'>" +
        "<table><tr><td>" +
        "<img src='/static/images/error.png' height='55px'>" +
        "<strong style='font-size:150%;margin-left: 20px'>ERROR!</strong>" +
        "</td><td style='font-size: 90%'>" +
        errorsFormatted +
        "</td></tr></table></div>"
}

function addItemToTable(buyerKey, price) {
    // get info
    var buyer_name = document.getElementById(buyerKey).innerText;
    var what = document.getElementById("what").value;
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1;
    var yyyy = today.getFullYear();
    if (dd < 10) dd = "0" + dd;
    if (mm < 10) mm = "0" + mm;
    var date = dd + "/" + mm + "/" + (yyyy % 1000);

    // add item to table
    var trTag = "<tr><td style='text-align:center'>" +
        date + "</td><td>" +
        buyer_name + "</td><td>" +
        what + "</td><td style='text-align:right'>" +
        price + "</td></tr>";
    document.getElementById("items").innerHTML += trTag;

    // clear old item info
    document.getElementById("buyer").value = "";
    document.getElementById("what").value = "";
    document.getElementById("price").value = "";
}

function updateSummarize(itemPrice) {
    var totalField = document.getElementById("total");
    var total = parseInt(totalField.innerHTML.replace(/\s/g, '')) + itemPrice * 1000;
    var average_int = Math.floor(total / numberOfPeople);
    var average_float = (total / numberOfPeople - average_int).toString();
    var i = average_float.indexOf(".");
    if (i === -1)
        average_float = "00";
    else
        average_float = (average_float + "00").slice(i + 1, i + 3);

    totalField.innerHTML = total.toLocaleString().replace(/,/g, " ");
    document.getElementById("average").innerHTML = average_int.toLocaleString().replace(/,/g, " ") + ".";
    document.getElementById("average-float").innerHTML = average_float;
}

function updateMoneyUsages(buyerKey, price) {
    // update for buyer
    var buyerSpend = document.getElementById("spend-" + buyerKey);
    var buyerMoneyToPay = document.getElementById("pay-" + buyerKey);
    buyerSpend.innerHTML = (parseInt(buyerSpend.innerHTML) + price).toString();
    buyerMoneyToPay.innerHTML = (parseInt(buyerMoneyToPay.innerText) - price).toString();

    // update for others
    var avgPrice = price / numberOfPeople;

    for (var i = 0; i < people.length; i++) {
        var moneyToPay = document.getElementById("pay-" + people[i]);
        var roundup = document.getElementById("roundup-" + people[i]);
        var nml = document.getElementById("nml-" + people[i]);

        var mtp = parseInt(moneyToPay.innerText) + avgPrice;
        var ru = Math.ceil(mtp / 10) * 10;

        moneyToPay.innerHTML = mtp.toFixed(2).toString();
        roundup.innerHTML = ru.toString();
        nml.innerHTML = (ru - mtp).toFixed(2).toString()
    }
}

function addSuccess() {
    var buyerKey = document.getElementById("buyer").value;
    var price = eval(document.getElementById("price").value);

    addItemToTable(buyerKey, price);
    updateSummarize(price);
    updateMoneyUsages(buyerKey, price);

    removeErrors();
}

function add() {
    var buyer = document.getElementById("buyer").value;
    var what = document.getElementById("what").value;
    var price = document.getElementById("price").value;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState !== 4)
            return;
        if (this.status === 200)
            addSuccess();
        else if (this.status === 409)
            displayErrors(xhttp.responseText)
    };
    xhttp.open("POST", "/month/");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send(
        "action=add&" +
        "buyer=" + encodeURI(buyer) + "&" +
        "what=" + encodeURI(what) + "&" +
        "price=" + encodeURI(price)
    )
}
