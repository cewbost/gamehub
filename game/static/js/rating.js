/* global $ */

$(document).ready(function () {
    "use strict";

    var rate_url = $("#game_rate_url").val();

    var csrftoken = getCookie("csrftoken");
    $.ajaxSetup({
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });

    $(".rating-star").click(function () {

        var r = (parseInt(this.id[5]) + 1) / 2;
        var posting = $.post(rate_url, {rating: r});
        posting.done(function (data) {
            var q = parseInt(data);
            $(".rating-star")
                .filter(":lt(" + q + ")")
                .children("span")
                .addClass("star-full");
            $(".rating-star")
                .filter(":gt(" + (q - 1) + ")")
                .children("span")
                .removeClass("star-full");
        });
    });
});