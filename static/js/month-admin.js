function displayMonthInfo(info) {
    var divTag = document.getElementById("month-info");
    var content =
        "<div class='panel-heading'>" +
        "   <h4><strong>{}</strong></h4>" +
        "</div>" +
        "<table class='table table-striped table-bordered table-hover'>" +
        "   <tr><td class=''>Start date</td><td>{}</td></tr>" +
        "   <tr><td class=''>End date</td><td>{}</td></tr>" +
        "   <tr><td class=''>Previous month</td><td>{}</td></tr>" +
        "   <tr><td class=''>Next month</td><td>{}</td></tr>" +
        "   <tr><td class=''>People in month</td><td>{}</td></tr>" +
        "   <tr><td class=''>Total</td><td>{}</td></tr>" +
        "   <tr><td class=''>Average</td><td>{}</td></tr>" +
        "</table>";

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