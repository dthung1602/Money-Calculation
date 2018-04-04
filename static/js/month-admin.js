//------------------  get month info -----------------

function displayMonthInfo(info) {
    var divTag = document.getElementById("month-info");
    var content =
        "<table id=\"month-info\" class='table table-hover'>" +
        "<thead class='panel-heading'>" +
        "<tr><th colspan='2'><h3><strong>{}</strong></h3></th></tr>" +
        "</thead>" +
        "<tbody>" +
        "<tr><td class='col-sm-3'>Key</td><td id='month-key'>{}</td></tr>" +
        "<tr><td>Start date</td><td>{}</td></tr>" +
        "<tr><td>End date</td><td>{}</td></tr>" +
        "<tr><td>Previous month</td><td>{}</td></tr>" +
        "<tr><td>Next month</td><td>{}</td></tr>" +
        "<tr><td>People in month</td><td id='people-in-month'>{}</td></tr>" +
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
    for (var i = 0; i < data.length; i++)
        data[i] = decodeURIComponent(data[i]);

    var month_key = document.getElementById("month-key").innerText;
    var rows = "";
    var row =
        "<tr id='row-item-{}' onmouseenter='showHideEditButton({}, false)' onmouseleave='showHideEditButton({}, true)'>" +
        "   <td class='col-sm-2'>{}</td>" +
        "   <td class='col-sm-2'>{}</td>" +
        "   <td>{}</td>" +
        "   <td class='col-sm-2'>{}</td>" +
        "   <td class='col-sm-3'>" +
        "       <input type='checkbox' id='item-{}' onclick='checkSelectAll()'>" +
        "       <span style='padding-left: 15px' id='edit-btn-{}' hidden><button onclick='startEdit({})' class='btn btn-default'>Edit</button></span>" +
        "   </td>" +
        "</tr>";

    for (i = 0; i < data.length; i++) {
        data[i] = data[i].split("|");
        for (var j = 0; j < data[i].length; j++)
            data[i][j] = decodeURIComponent(data[i][j]);

        var ii = i.toString();
        var arr = [ii, ii, ii];

        arr = arr.concat(data[i], [ii, ii, ii]);
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
    window.editting = -1;
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
    if (window.editting !== -1) {
        alert("You are editing an item.\nPlease save or cancel editing before deleting other items.")
        return;
    }

    var content = "action=deleteitems&key=" + key + "&items=";
    var items = document.querySelectorAll('[id^="item-"]');
    var delItemsCount = 0;
    var first = true;
    for (var i = 0; i < items.length; i++) {
        if (items[i].checked) {
            delItemsCount++;
            if (first) {
                content += items[i].id.slice(5);
                first = false;
            } else
                content += "%2C" + items[i].id.slice(5);
        }
    }
    if (delItemsCount > 0 && confirm("Are you sure to delete " + delItemsCount + " item(s)?"))
        makeHttpRequest(reloadMonth, displayMonthInfoError, "/admin", content);
}

// ----------------------- edit ----------------------------
editting = -1;
oldData = null;

function showHideEditButton(num, hidden) {
    if (editting === -1)
        document.getElementById("edit-btn-" + num).hidden = hidden;
}

function startEdit(num) {
    showHideEditButton(num, true);
    var row = document.getElementById("row-item-" + num);

    window.editting = num;
    window.oldData = row.innerHTML;
    var tds = row.getElementsByTagName("td");

    // date
    var oldDate = "20" + tds[0].innerText.split("/").reverse().join("-");

    // buyer
    var oldBuyerName = tds[1].innerText;
    var selectContent = "";
    var validNames = document.getElementById("people-in-month").innerText.split(", ");
    for (var i = 0; i < validNames.length; i++) {
        if (oldBuyerName !== validNames[i]) {
            selectContent += simpleFormat("<option value='{}'>{}</option>",
                personNameToKey[validNames[i]],
                validNames[i]
            )
        } else {
            selectContent += simpleFormat("<option value='{}' selected>{}</option>",
                personNameToKey[validNames[i]],
                validNames[i]
            )
        }
    }

    // what & price
    var oldWhat = tds[2].innerText;
    var oldPrice = tds[3].innerText;

    // create content
    var row_content =
        "<td class='col-sm-2'>" +
        "    <input type='date' name='date' id='edit-date' value='{}'>" +
        "</td>" +
        "<td class='col-sm-2'>" +
        "    <select name='buyer' id='edit-buyer'>{}</select>" +
        "</td>" +
        "<td>" +
        "    <input type='text' name='what' id='edit-what' value='{}'>" +
        "</td>" +
        "<td class='col-sm-2'>" +
        "    <input type='text' name='price' id='edit-price' value='{}' pattern='^[0-9 \\+\\-\\*\\/\\(\\)]+$'>" +
        "</td>" +
        "<td class='col-sm-3'>" +
        "    <button onclick='saveItem()' class='btn btn-default'>Save</button>" +
        "    <button onclick='cancelSaveItem()' class='btn btn-default'>Cancel</button>" +
        "</td>";

    row.innerHTML = simpleFormat(row_content, oldDate, selectContent, oldWhat, oldPrice);
}

function saveItem() {
    var month_key = document.getElementById("month-key").innerText;

    var date = encodeURIComponent(document.getElementById("edit-date").value);
    var buyer = encodeURIComponent(document.getElementById("edit-buyer").value);
    var what = encodeURIComponent(document.getElementById("edit-what").value);
    var price = encodeURIComponent(document.getElementById("edit-price").value);

    var content = "action=edititem" +
        "&key=" + month_key +
        "&item=" + window.editting +
        "&date=" + date +
        "&buyer=" + buyer +
        "&what=" + what +
        "&price=" + price;
    makeHttpRequest(reloadMonth, alert, "/admin", content)
}

function cancelSaveItem() {
    document.getElementById("row-item-" + window.editting).innerHTML = window.oldData;
    window.oldData = null;
    window.editting = -1;
}