/* global $ */

// using jQuery - source Django
function getCookie(name) {
    "use strict";
    if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        return decodeURIComponent(cookies.filter(
            (cookie) => cookie.substring(0, name.length + 1) === (name + "=")
        )[0].substring(name.length + 1));
    } else {
        return null;
    }
}