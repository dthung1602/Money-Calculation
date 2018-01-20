function forgetPassword() {
    var content =
        "<div class='panel panel-default col-md-9' style='margin-top: 40px; padding: 25px'>" +
        "    <label style='margin-right: 30px'>Admin email</label>" +
        "    <input id='email' style='width: 350px'>" +
        "    <div id='info' style='margin-top: 30px'></div>" +
        "    <div style='margin-top: 30px' align='center'>" +
        "        <button id='send' class='btn btn-primary' onclick='sendMail()'>Send email</button>" +
        "    </div>" +
        "</div>";

    document.getElementById("forget").innerHTML = content;
}

function displayInfo(info) {
    var content =
        "<p style='color: forestgreen'>{}</p>" +
        "<p>Haven't received your email? Try again in <span id='count'>90</span> seconds</p>";
    document.getElementById("info").innerHTML = simpleFormat(content, info);

    var button = document.getElementById("send");
    button.innerHTML = "Try again";
    button.disabled = true;
    countDown(document.getElementById("count"))
}

function displayError(error) {
    var content = "<p style='color: red'>{}</p>";
    document.getElementById("info").innerHTML = simpleFormat(content, error);

    var button = document.getElementById("send");
    button.innerHTML = "Try again";
}

function sendMail() {
    var email = document.getElementById("email").value;
    var content = "email=" + encodeURIComponent(email);
    makeHttpRequest(displayInfo, displayError, "/admin/recover-password", content);
}

function countDown(element) {
    var timeLeft = parseInt(element.innerText) - 1;
    element.innerText = timeLeft.toString();
    if (timeLeft === 0)
        document.getElementById("send").disabled = false;
    else
        setTimeout(countDown, 1000, element);
}