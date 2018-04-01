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
        "<div align='center' id='items'><button id='list-items-btn' class='btn btn-default' onclick='listItems(\"{}\")'>List items</button></div>";

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
    data = data.split(";");
    var month_key = data[0];
    var rows = "";
    var row =
        "<tr id='item-row-{}' onmouseenter='showHideEditButton({}, false)' onmouseleave='showHideEditButton({}, true)'>" +
        "   <td class='col-sm-2'>{}</td>" +
        "   <td class='col-sm-2'>{}</td>" +
        "   <td>{}</td>" +
        "   <td class='col-sm-2'>{}</td>" +
        "   <td class='col-sm-3'>" +
        "       <input type='checkbox' id='item-{}' onclick='checkSelectAll()'>" +
        "       <span style='padding-left: 15px' id='edit-btn-{}' hidden><button onclick='startEdit({})' class='btn btn-default'>Edit</button></span>" +
        "   </td>" +
        "</tr>";

    for (var i = 1; i < data.length; i++) {
        var ii = (i - 1).toString();
        var arr = [ii, ii, ii];
        arr = arr.concat(data[i].split("|"), [ii, ii, ii]);
        rows += simpleFormat(row, arr);
    }

    var table =
        "<table class='table table-hover' style='margin-top: 50px; margin-bottom: 50px;'>" +
        "   <thead class='panel-heading'>" +
        "       <tr><th colspan='5'><h3><strong>Items</strong></h3></th></tr>" +
        "       <tr>" +
        "           <th>Date</th>" +
        "           <th>Buyer</th>" +
        "           <th>What</th>" +
        "           <th>Price (K)</th>" +
        "           <th><input id='all-items' type='checkbox' onclick='selectAllItems()'></th>" +
        "       </tr>" +
        "   </thead>" +
        "   <tbody>{}</tbody>" +
        "</table>" +
        "<div align='center' style='margin-top: 30px; margin-bottom: 60px'>" +
        "   <button class='btn btn-default' onclick='reloadMonth(\"{}\")'>Reload</button>" +
        "   <button class='btn btn-primary' onclick='deleteItems(\"{}\")'>Delete</button>" +
        "</div>";

    document.getElementById("items").innerHTML = simpleFormat(table, rows, month_key, month_key);
}

function displayItemsError(error) {
    var divTag = document.getElementById("items");
    var content = "<div style='color: red; margin: 10px'>{}</div>";
    divTag.innerHTML += simpleFormat(content, error);
    document.getElementById("list-items-btn").innerText = "Try again";
}

function listItems(key) {
    var content = "action=listitems&key=" + key;
    makeHttpRequest(displayItems, displayItemsError, "/admin", content);
}

//----------------- reload -------------------

function reloadMonth(key) {
    getMonthInfo(key);
    setTimeout(listItems, 200, key);
}

//----------------- select -------------------

function selectAllItems() {
    var bool = document.getElementById("all-items").checked;
    var items = document.querySelectorAll('[id^="item-"]');
    for (var i = 0; i < items.length; i++)
        items[i].checked = bool;
}

function checkSelectAll() {
    var items = document.querySelectorAll('[id^="item-"]');
    for (var i = 0; i < items.length; i++)
        if (!items[i].checked) {
            document.getElementById("all-items").checked = false;
            return;
        }
    document.getElementById("all-items").checked = true;
}

//----------------- delete -------------------

function deleteItems(key) {
    var content = "action=deleteitems&key=" + key + "&items=";
    var items = document.querySelectorAll('[id^="item-"]');
    var first = true;
    for (var i = 0; i < items.length; i++) {
        if (items[i].checked) {
            if (first) {
                content += items[i].id.slice(5);
                first = false;
            } else
                content += "%2C" + items[i].id.slice(5);
        }
    }
    if (confirm("Are you sure to delete " + items.length + " item(s)?"))
        makeHttpRequest(reloadMonth, displayMonthInfoError, "/admin", content);
}

// ----------------------- edit ----------------------------
editting = false;
oldData = null;

function showHideEditButton(num, hidden) {
    if (!editting)
        document.getElementById("edit-btn-" + num).hidden = hidden;
}

function startEdit(num) {
    var row = document.getElementById("item-row-" + num);

    window.editting = true;
    window.oldData = row.innerHTML;

    var row_content =
        "<tr onmouseenter='showHideEditButton({}, false)' onmouseleave='showHideEditButton({}, true)'>" +
        "<form method='post' action='/admin'>" +
        "   <input type='hidden' name='action' value='edititem'>" +
        "   <input type='hidden' name='item' value='{}'>" +
        "   <td class='col-sm-2'>" +
        "       <input type='date' name='date' value='{}'>" +
        "       <input type='time' name='time' value='{}'>" +
        "   </td>" +
        "   <td class='col-sm-2'>" +
        "       <select name='buyer'>{}</select>" +
        "   </td>" +
        "   <td>" +
        "       <input type='text' name='what' value='{}'>" +
        "   </td>" +
        "   <td class='col-sm-2'>" +
        "       <input type='text' name='price' value='{}' pattern='^[0-9 \\+\\-\\*\\/\\(\\)]+$'>" +
        "   </td>" +
        "   <td class='col-sm-3'>" +
        "       <button onclick='saveItem({})' class='btn btn-default'>Save</button>" +
        "       <button onclick='cancelSaveItem({})' class='btn btn-default'>Cancel</button>" +
        "   </td>" +
        "</form>" +
        "</tr>";

    row.innerHTML = row_content;
}

function saveItem(num) {
    alert("save " + num);
}

function cancelSaveItem(num) {
    // document.getElementById("edit-row-" + num).innerHTML = window.oldData
    window.oldData = null;
    window.editting = false;
}