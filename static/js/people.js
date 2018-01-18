function displayInfo(info) {
    var divTag = document.getElementById("info");
    var content =
        "<div class='panel-heading'>" +
        "   <h4><strong>{}</strong></h4>" +
        "</div>" +
        "<table class='table table-striped table-bordered table-hover'>" +
        "   <tr><td class=''>Key</td><td>{}</td></tr>" +
        "   <tr><td class=''>Total spending</td><td>{}</td></tr>" +
        "   <tr><td class=''>Number of months attended</td><td>{}</td></tr>" +
        "   <tr><td class=''>Payments made for everyone</td><td>{}</td></tr>" +
        "   <tr><td class=''>Latest month attended</td><td>{}</td></tr>" +
        "   <tr><td class=''>Money left</td><td>{}</td></tr>" +
        "   <tr><td class=''>In current month</td><td>{}</td></tr>" +
        "</table>";

    divTag.innerHTML = simpleFormat(content, info.split(";"));
}

function displayErrorPersonInfo(error) {
    var divTag = document.getElementById("info");
    var content =
        "<div class='panel-heading'>" +
        "   <h4><strong>ERROR</strong></h4>" +
        "</div>" +
        "<div style='margin: 30px'>{}</div>";

    divTag.innerHTML = simpleFormat(content, error);
}

function getPersonInfo(key) {
    var content = "action=getpersoninfo&key=" + key;
    makeHttpRequest(displayInfo, displayErrorPersonInfo, "/admin", content);
}
