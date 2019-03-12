
/**
 * on change of radio
 * Update selected test subcategory
 */
var onSubRadioChanged = function(event){
    subcategory = $(this).attr("value");
    $.ajax({
        url : 'select-subcategory-form',
        type : "POST",
        data : {
            subcategory,
        },
        success: function(data){
            document.getElementById("load-test-data").style.visibility = "visible";
            //document.getElementById("load-test-data").addAttribute(selectedTest=data);
        },
        error: function(data){
            console.log("Error");
        }
    });
}

// .ready() called.
$(function() {
    // bind change event to subcategory radio button
    $("[name='subcategories']").on("change", onSubRadioChanged);
});