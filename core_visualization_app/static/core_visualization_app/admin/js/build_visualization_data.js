
/**
* on click 'Build visualization data'
load and create data lines visualization objects
*/

var loadVisualizationData = function(event){
   document.getElementById("loading_background").style.visibility = "visible";
   $.ajax({
    url:"visualization/build-visualization-data",
    success: function(data) {
        document.getElementById("loading_background").style.visibility = "hidden";
    },
    error: function(data){
        console.log("Error");
        }
  });
 }


$(function() {
    $('#build-visualization-data').on("click", loadVisualizationData);
});