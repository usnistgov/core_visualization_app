
/**
 * on change of checkbox
 * Add selected project to the list of selected projects
 */
var onCheckboxChanged = function(event){
    project = $(this).attr("value");
    $.ajax({
        url : 'select-projects-form',
        type : "POST",
        data : {
            project,
        },
       });
}

// .ready() called.
$(function() {
    // bind change event to checkbox
    $(":checkbox").on("change", onCheckboxChanged);
});