
/**
* on click 'confirm'
load and display data table
*/
var onClick = function(event){
   document.getElementById("loading_background").style.visibility = "visible";
   $.ajax({
    url: load_test_data,
    success: function(data) {
        document.getElementById("loading_background").style.visibility = "hidden";
        document.getElementById("data-table-section").style.visibility = "visible";
        document.getElementById("plot-section").style.visibility = "visible";
        removeElement("select-projects-form");
        removeElement("select-category-form");
        removeElement("select-subcategory-form");
        removeElement("load-test-data");
        removeElement("selection-header");
        removeElement("plot-example");
        var dataT = data.data_table_csv;
        var script = data.script;
        var div = data.div;
        if (data.script==null && data.div==null){$('#demo_plot').html("No data available for this selection criteria"); return;}

        var data_table = dataT.split(/\r?\n|\r/);
        var table = '<div id="table-scroll" style="overflow:auto; margin-top:20px;"><table class="table table-bordered table-striped" width="100%" style="display: block;overflow-x: auto;white-space: nowrap;"><thead>';
        for(var count = 0; count<data_table.length; count++){
            var cell_data = data_table[count].split(",");
            table += '<tr>';
            for(var cell_count=0; cell_count<cell_data.length; cell_count++){
                if(count === 0){
                    table += '<th>'+cell_data[cell_count]+'</th>';
                }
                else{
                    table += '<td>'+cell_data[cell_count]+'</td>';
                }
            }
        }
        table = table.substring(0, table.length - 13); // one cell to remove at the end
        table += '</thead></table></div>';
        $('#data_table').html(table);
        var plot = '';
        plot += div ;
        plot += '';
        plot += script ;
        $('#demo_plot').html(plot);

        $.ajax({
     url: update_selection_forms,
     type: "GET",
     dataType: "json",
     success: function(data) {
        if(data !== null) {
            $('#select_config_forms').html(data.template);
            if (data.x_parameters !== null){
                document.getElementById('select-x-parameter-form').style.visibility = "visible";
                $('#select-x-parameter-form').on("change", onChangeConfigurationsX);
                }
            if (data.y_parameters !== null){
                document.getElementById('select-y-parameter-form').style.visibility = "visible";
                $('#select-y-parameter-form').on("change", onChangeConfigurationsY);
                }
            if (data.customized_parameters !== null){
                document.getElementById('select-custom-parameter-form').style.visibility = "visible";
                $('#select-custom-parameter-form').on("change", onChangeConfigurationsCustom);
                }

        };

    },
    error: function(data){
        console.log("Error");
        }
  });
     }});
 }

/**
* on change 'plot options'
* update plot configurations
*  Might also change the custom form
**/


var onChangeConfigurationsX = function(event){
	document.getElementById("loading_background").style.visibility = "visible";
	new_parameter = $("#select-x-parameter-form :selected").attr('value');
	parameter_type = 'x_parameter';
    $.ajax({
        url : update_configuration,
        type : "POST",
        data : {
            new_parameter,
            parameter_type,
        },
        success: function(data) {
        document.getElementById("loading_background").style.visibility = "hidden";

        var plot = '';
        plot += data.div ;
        plot += '';
        plot += data.script ;
        $('#demo_plot').html(plot);

           $.ajax({
        url: update_custom_form,
        type: "GET",
        dataType: "json",
        success: function(data) {
            if(data.form) {
                document.getElementById('select_config_forms').innerHTML=data.form;
                document.getElementById('select-x-parameter-form').style.visibility = "visible";
                document.getElementById('select-custom-parameter-form').style.visibility = "visible";
                $('#select-x-parameter-form').on("change", onChangeConfigurationsX);
                $('#select-custom-parameter-form').on("change", onChangeConfigurationsCustom);
            };

        },
        error: function(data){
            console.log("Error");
            }
        });

        },
    error: function(data){
        console.log("Error");
        }
      });
}

var onChangeConfigurationsY = function(event){
	document.getElementById("loading_background").style.visibility = "visible";
	new_parameter = $("#select-y-parameter-form :selected").attr('value');
	parameter_type = 'y_parameter';
    $.ajax({
        url : update_configuration,
        type : "POST",
        data : {
            new_parameter,
            parameter_type,
        },
        success: function(data) {
        document.getElementById("loading_background").style.visibility = "hidden";

        var plot = '';
        plot += data.div ;
        plot += '';
        plot += data.script ;
        $('#demo_plot').html(plot);

        },
    error: function(data){
        console.log("Error");
        }
      });
}


var onChangeConfigurationsCustom = function(event){
	document.getElementById("loading_background").style.visibility = "visible";
	new_parameter = $("#select-custom-parameter-form :selected").attr('value');
	parameter_type = 'custom_parameter';
    $.ajax({
        url : update_configuration,
        type : "POST",
        data : {
            new_parameter,
            parameter_type,
        },
        success: function(data) {
        document.getElementById("loading_background").style.visibility = "hidden";


        var plot = '';
        plot += data.div ;
        plot += '';
        plot += data.script ;
        $('#demo_plot').html(plot);
        $('#select-x-parameter-form').on("change", onChangeConfigurationsX);
        $('#select-custom-parameter-form').on("change", onChangeConfigurationsCustom);

        },
    error: function(data){
        console.log("Error");
        }
      });
}

function removeElement(elementId) {
    // Removes an element from the document
    var element = document.getElementById(elementId);
    element.parentNode.removeChild(element);
}

// .ready() called.
$(function() {
   $('#load-test-data').on("click", onClick);
});