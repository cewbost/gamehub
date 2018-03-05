/* global $ */

$(document).ready(function () {
    "use strict";

    //Game id and user_id from the hidden field to post the data
    var game_update_url = $("#game_update_url").val();
    var game_highscore_url = $("#game_highscore_url").val();
    //updates the highscore
    setInterval(function () {
        $("#gameresult").load(game_highscore_url);
    }, 10000);

    var csrftoken = getCookie("csrftoken");
    $.ajaxSetup({
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });

    $(window).on("message", function (evt) {
        //Note that messages from all origins are accepted
        //Get data from sent message
        var data = evt.originalEvent.data;

        if (data.messageType) {
            var posting;
            switch (data.messageType) {
            case "SETTING":
                $("#game_iframe").attr("width", data.options.width);
                $("#game_iframe").attr("height", data.options.height);
                break;
            default:
                posting = $.post(game_update_url, {data: JSON.stringify(data)});
                posting.done(function (data) {
                    //sends event to the iframe if error or to be load the new data
                    if (data.messageType === "LOAD" || data.messageType === "ERROR") {
                        var iframe_window = $("#game_iframe")[0].contentWindow;
                        iframe_window.postMessage(data, "*");
                    }
                });
            }
        }
    });
});
