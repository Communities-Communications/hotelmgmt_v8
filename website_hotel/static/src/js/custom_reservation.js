// StarHotel Javascripts
jQuery(document).ready(function () {
    "use strict";

    // Reservation Form	
    //jQueryUI - Datepicker
    if (jQuery().datepicker) {
        jQuery('#checkin').datepicker({
            showAnim: "drop",
            dateFormat: "dd/mm/yy",
            minDate: "-0D",
        });

        jQuery('#checkout').datepicker({
            showAnim: "drop",
            dateFormat: "dd/mm/yy",
            minDate: "+1D",
            language: "pt",
            beforeShow: function () {
                var a = jQuery("#checkin").datepicker('getDate');
                if (a) return {
                    minDate: a
                }
            }
        });
        jQuery('#checkin, #checkout').on('focus', function () {
            jQuery(this).blur();
        }); // Remove virtual keyboard on touch devices
    }


    //Popover
    jQuery('[data-toggle="popover"]').popover();


    // Guests
    // Show guestsblock onClick
    var guestsblock = jQuery(".guests");
    var guestsselect = jQuery(".guests-select");
    var save = jQuery(".button-save");
    guestsblock.hide();

    guestsselect.click(function () {
        guestsblock.show();
    });

    save.click(function () {
        guestsblock.fadeOut(120);
    });


    // Count guests script
    var opt1;
    var opt2;
    var total;
    jQuery('.adults select, .children select').change(

        function () {
            opt1 = jQuery('.adults').find('option:selected');
            opt2 = jQuery('.children').find('option:selected');

            total = +opt1.val() + +opt2.val();
            jQuery(".guests-select .total").html(total);
        });


});
