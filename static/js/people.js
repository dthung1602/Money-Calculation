//--------------------- Get info ----------------------

function displayPersonInfo(info) {
    var divTag = document.getElementById("info");
    var content =
        "<div class='panel-heading'>" +
        "   <h4><strong>{}</strong></h4>" +
        "</div>" +
        "<table class='table table-striped table-bordered table-hover'>" +
        "   <tr><td class=''>ID</td><td>{}</td></tr>" +
        "   <tr><td class=''>Total spending</td><td>{}</td></tr>" +
        "   <tr><td class=''>Number of months attended</td><td>{}</td></tr>" +
        "   <tr><td class=''>Payments made for everyone</td><td>{}</td></tr>" +
        "   <tr><td class=''>Latest month attended</td><td>{}</td></tr>" +
        "   <tr><td class=''>Money left</td><td>{}</td></tr>" +
        "   <tr><td class=''>In current month</td><td>{}</td></tr>" +
        "</table>";

    divTag.innerHTML = simpleFormat(content, info.split(";"));
}

function displayPersonInfoError(error) {
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
    makeHttpRequest(displayPersonInfo, displayPersonInfoError, "/admin", content);
}

//--------------------- New person ----------------------

function addNewPerson(data) {
    data = data.split(";");

    var content =
        "<div class='list-group-item striped' style='padding-left: 35px'" +
        "             onclick=\"getPersonInfo('{}')\">{}</div>";
    document.getElementById("people").innerHTML += simpleFormat(content, data[0], data[1]);

    content = "<div style=\"margin: 20px; color: forestgreen\">Successfully add '{}' to data store</div>";
    document.getElementById("info").innerHTML = simpleFormat(content, data[1]);

    document.getElementById("name").value = "";
}

function displayNewPersonError(error) {
    var content = "<div style=\"margin: 20px; color: red\">{}</div>";
    document.getElementById("info").innerHTML = simpleFormat(content, error);
}

function createNewPerson() {
    var name = document.getElementById("name").value;
    var content = "action=newperson&name=" + name;
    makeHttpRequest(addNewPerson, displayNewPersonError, "/admin", content)
}