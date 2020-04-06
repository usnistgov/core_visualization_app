
/**
 * on change of radio
 * Update selected test category
 */
var onRadioChanged = function(event){
    category = $(this).attr("value");
     document.getElementById("select-subcategory-form").style.visibility = "visible";
     document.getElementById("load-test-data").style.visibility = "hidden";
    $.ajax({
        url : select_category_form,
        type : "POST",
        data : {
            category,
        },
        success: function(data){
            var subcategories = JSON.parse(data);
            $("#select-subcategory-form").find("li").hide();
            for (var subcategory in subcategories){
                $("[value='"+subcategories[subcategory]+"']").closest("li").show();
            };
        },
        error: function(data){
            console.log("Error select_category_form");
        }
    });
}

// .ready() called.
$(function() {
    // bind change event to category radio button
    $("[name='categories']").on("change", onRadioChanged);
});