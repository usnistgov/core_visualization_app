
/**
 * on change of radio
 * Update selected test subcategory
 */
var onSubRadioChanged = function(event){
    subcategory = $(this).attr("value");
    console.log("RADIO CHANGED BUTTON")
    $.ajax({
        url : select_subcategory_form,
        type : "POST",
        data : {
            subcategory,
        },
        success: function(data){
            document.getElementById("load-test-data").style.visibility = "visible";
            //document.getElementById("load-test-data").addAttribute(selectedTest=data);
        },
        error: function(data){
            console.log("Error subcategory");
        }
    });
}

// .ready() called.
$(function() {
    // bind change event to subcategory radio button
    $("[name='subcategories']").on("change", onSubRadioChanged);
});