//------------------  get month info -----------------

function displayMonthInfo(info) {
    var divTag = document.getElementById("month-info");
    var content =
        "<table id=\"month-info\" class='table table-hover'>" +
        "<thead class='panel-heading'>" +
        "<tr><th colspan='2'><h3><strong>{}</strong></h3></th></tr>" +
        "</thead>" +
        "<tbody>" +
        "<tr><td class='col-sm-3'>Start date</td><td>{}</td></tr>" +
        "<tr><td>End date</td><td>{}</td></tr>" +
        "<tr><td>Previous month</td><td>{}</td></tr>" +
        "<tr><td>Next month</td><td>{}</td></tr>" +
        "<tr><td>People in month</td><td>{}</td></tr>" +
        "<tr><td>Total</td><td>{}</td></tr>" +
        "<tr><td>Average</td><td>{}</td></tr>" +
        "</tbody>" +
        "</table>" +
        "<div align='center' id='items'><button class='btn btn-default' onclick='listItems(\"{}\")'>List items</button></div>";

    divTag.innerHTML = simpleFormat(content, info.split(";"));
}

function displayMonthInfoError(error) {
    var divTag = document.getElementById("month-info");
    var content =
        "<div class='panel-heading'>" +
        "   <h4><strong>ERROR</strong></h4>" +
        "</div>" +
        "<div style='margin: 30px'>{}</div>";

    divTag.innerHTML = simpleFormat(content, error);
}

function getMonthInfo(key) {
    var content = "action=getmonthinfo&key=" + key;
    makeHttpRequest(displayMonthInfo, displayMonthInfoError, "/admin", content);
}

//------------------  list items -----------------

function displayItems(data) {

}

function displayItemsError(error) {

}

function listItems(key) {
    var content = "action=listitems&key=" + key;
    makeHttpRequest(displayItems, displayItemsError, "/admin", content);
}