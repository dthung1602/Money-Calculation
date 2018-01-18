function openTab(tabName) {
    var tabs = document.getElementsByClassName("tab");
    for (var i = 0; i < tabs.length; i++)
        tabs[i].hidden = true;
    document.getElementById("tab-" + tabName).hidden = false;
}

function successChangePassword(login_cookie) {
    // set login cookie
    document.cookie = "login=" + login_cookie;

    // reset other elements
    document.getElementById("password-last-mod").innerHTML = "<span style='color: forestgreen'> Updated: "
        + getDateTimeFormatted() + "</span>";
    var clearList = ["password", "re-password"];
    for (i = 0; i < clearList.length; i++)
        document.getElementById(clearList[i]).value = "";
    clearList = ["password-error", "re-password-error", "password-strength"];
    for (var i = 0; i < clearList.length; i++)
        document.getElementById(clearList[i]).innerText = "";
}

function changePassword() {
    // validate
    var password = document.getElementById("password").value;
    if (!validateRePassword(password) || !validateRePassword())
        return;

    // content
    var content = "action=changepassword&password=" + encodeURIComponent(password);

    // send request
    makeHttpRequest(successChangePassword, null, "/admin", content);
}

function isASCII(str) {
    for (var i = 0, n = str.length; i < n; i++) {
        if (str.charCodeAt(i) > 255)
            return false;
    }
    return true;
}

function validatePassword() {
    var password = document.getElementById("password").value;
    var tag = document.getElementById("password-error");

    if (!isASCII(password))
        tag.innerHTML = "<span style='color: red'>Password must contain only ASCII characters</span>";
    else if (password.length === 0)
        tag.innerHTML = "<span style='color: red'>Password must not be empty</span>";
    else {
        tag.innerHTML = "";
        var pwStrength = passwordStrength(password);

        document.getElementById("password-strength").innerHTML =
            "<div class='form-group'>" +
            "<label class='control-label col-sm-3' for='password-strength'>Password strength</label>" +
            "<div class='col-sm-5'>" +
            "<span id='password-strength' style='color: " + pwStrength.color + "'><strong>" + pwStrength.strength + "</strong></span>" +
            "</div></div>";

        return pwStrength.valid;
    }
    return false;
}

function passwordStrength(password) {
    // calculate password strength
    var score = password.length; // 1p for each character
    var regex = [/[a-z]/, /[0-9]/, /[A-Z]/, /[~`!@#$%^&*()_\-+={[}\]|\\:;"'<,>.?/]/];
    for (var i = 0, n = regex.length; i < n; i++)
        if (regex[i].test(password))
            score += i + 2;

    // classify
    var strength, color;
    var securityLevels = [
        {
            score: 5,
            strength: "Very weak",
            color: "red",
            valid: false
        },
        {
            score: 8,
            strength: "Weak",
            color: "orange",
            valid: false
        },
        {
            score: 14,
            strength: "Medium",
            color: "yellow",
            valid: true
        },
        {
            score: 22,
            strength: "Strong",
            color: "yellowgreen",
            valid: true
        },
        {
            score: Number.POSITIVE_INFINITY,
            strength: "Very Strong",
            color: "green",
            valid: true
        }
    ];

    for (i = 0; i < securityLevels.length; i++) {
        if (score <= securityLevels[i].score) {
            strength = securityLevels[i].strength;
            color = securityLevels[i].color;
            return securityLevels[i]
        }
    }
}

function validateRePassword() {
    var str = document.getElementById("re-password").value;
    var match = document.getElementById("password").value === str;
    if (match) {
        if (str.length > 0) {
            document.getElementById("re-password-error").innerHTML = "<span style='color: forestgreen'>Matched</span>";
            return true;
        } else
            document.getElementById("re-password-error").innerHTML = "<span style='color: red'>Please confirm password</span>";
    } else {
        document.getElementById("re-password-error").innerHTML = "<span style='color: red'>Password does not match</span>";
    }
    return false;
}