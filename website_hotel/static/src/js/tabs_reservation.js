$(document).ready(function () {
    //Initialize tooltips
    $('.nav-tabs > li a[title]').tooltip();
    
    //Wizard
    $('a[data-toggle="tab"]').on('show.bs.tab', function (e) {

        var $target = $(e.target);
    
        if ($target.parent().hasClass('disabled')) {
            return false;
        }
    });

    $(".next-step").click(function (e) {

        var $active = $('.wizard .nav-tabs li.active');
        $active.next().removeClass('disabled');
        nextTab($active);

    });
    $(".prev-step").click(function (e) {

        var $active = $('.wizard .nav-tabs li.active');
        prevTab($active);

    });
});

function nextTab(elem) {
    $(elem).next().find('a[data-toggle="tab"]').click();
}
function prevTab(elem) {
    $(elem).prev().find('a[data-toggle="tab"]').click();
}

//
function validateFormh() {
    var x = document.forms["reservationformh"]["name"].value;
    var x = document.forms["reservationformh"]["checkin"].value;
    var x = document.forms["reservationformh"]["checkout"].value;
    if (x == null || x == "") {
        alert("Todos os campos são obrigatórios");
        return false;
    }
}
//
function validateForm() {
    var x = document.forms["reservationform"]["name"].value;
    var x = document.forms["reservationform"]["checkin"].value;
    var x = document.forms["reservationform"]["checkout"].value;
    var x = document.forms["reservationform"]["contact_name"].value;
    var x = document.forms["reservationform"]["email_from"].value;
    var x = document.forms["reservationform"]["phone"].value;
    var x = document.forms["reservationform"]["street"].value;
    var x = document.forms["reservationform"]["zip"].value;
    var x = document.forms["reservationform"]["city"].value;
    var x = document.forms["reservationform"]["country_id"].value;
    var x = document.forms["reservationform"]["vat"].value;
    var x = document.forms["reservationform"]["cardname"].value;
    var x = document.forms["reservationform"]["card-number"].value;
    var x = document.forms["reservationform"]["cvv"].value;
    if (x == null || x == "") {
        alert("Volte atrás e verifique os campos");
        return false;
    }
}
//
//    $(function() {
//        $('#card-number').validateCreditCard(function(result) {
//            $('.log').html('Card type: ' + (result.card_type == null ? '-' : result.card_type.name)
//                     + '<br>Valid: ' + result.valid
//                     + '<br>Length valid: ' + result.length_valid
//                     + '<br>Luhn valid: ' + result.luhn_valid);
//        });
//    });
//

//
$('#terms').click(function () {
    //check if checkbox is checked
    if ($(this).is(':checked')) {
        
        $('#enabledbutton').removeAttr('disabled'); //enable input
        
    } else {
        $('#enabledbutton').attr('disabled', true); //disable input
    }
});
