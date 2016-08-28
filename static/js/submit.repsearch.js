"use strict";


function submitRepSearch(evt) {
    evt.preventDefault();

    var formInputs = {
        "city": $("#city-field").val(),
        "state": $("#state-field").val()
    };

    $.post("/repdetails", 
    	   formInputs,
    	   showOrderResults
    	   );
}

$("#order-form").on("submit", submitOrder);



