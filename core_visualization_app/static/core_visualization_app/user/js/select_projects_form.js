
/**
 * on change of checkbox
 * Add selected project to the list of selected projects
 */
var onCheckboxChanged = function(event){
    project = $(this).attr("value");
    $.ajax({
        url : select_projects_form,
        type : "POST",
        data : {
            project,
        },
        error: function(data){
            console.log("Error select_projects_form");
        }
       });
}

// .ready() called.
$(function() {
    // bind change event to checkbox
    $(":checkbox").on("change", onCheckboxChanged);
});