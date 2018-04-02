function makeHttpRequest(successFunction, displayErrorsFunction, path, content) {
    var request = new XMLHttpRequest();

    request.onreadystatechange = function () {
        if (this.readyState !== 4)
            return;
        switch (this.status) {
            case 200:
                if (successFunction != null)
                    successFunction(request.responseText);
                break;
            case 500:
                if (displayErrorsFunction != null)
                    displayErrorsFunction("Internal server error. Please try again later.");
                break;
            case 0:
                if (displayErrorsFunction != null)
                    displayErrorsFunction("Cannot connect to server.");
                break;
            default:
                if (displayErrorsFunction != null)
                    displayErrorsFunction(request.responseText);
        }
    };
    request.open("POST", path);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.send(content);
}

function getDateFormatted() {
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1;
    var yy = today.getFullYear();
    if (dd < 10) dd = "0" + dd;
    if (mm < 10) mm = "0" + mm;
    return dd + "/" + mm + "/" + (yy % 1000);
}

function getDateTimeFormatted() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    var dd = today.getDate();
    var mm = today.getMonth() + 1;
    var yy = today.getFullYear();

    if (dd < 10) dd = "0" + dd;
    if (mm < 10) mm = "0" + mm;
    if (h < 10) h = "0" + h;
    if (m < 10) m = "0" + m;
    if (s < 10) s = "0" + s;

    return dd + "/" + mm + "/" + (yy % 1000) + ", " + h + ":" + m + ":" + s;
}

function simpleFormat() {
    var args = [];
    for (var i = 0; i < arguments.length; i++)
        args.push(arguments[i]);
    var string = args[0];
    var subStrings;
    if (args.length === 2 && Array.isArray(args[1]))
        subStrings = args[1];
    else
        subStrings = args.slice(1, args.length);

    var pos = string.lastIndexOf("{}");
    while (pos > -1) {
        string = string.slice(0, pos)
            + subStrings.pop()
            + string.slice(pos + 2, string.length);
        pos = string.lastIndexOf("{}");
    }
    return string;
}

function deleteElementById(id) {
    var element = document.getElementById(id);
    element.parentNode.removeChild(element);
}