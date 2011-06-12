

function saveConfigs(){
    
    $("#id_custom_fields_to").each(function(){
        alert($(this).text());
        });
        
    $("#id_vehicles_to").each(function(){
        alert($(this).text());
        });
    
}

$(document).ready( function() {
	
	$('#saveconf').click(function() {
        saveConfigs();
        /*
        $.get("/rastreamento/xhrtest", function(data) {
            $("#tabs-6").html(data);

        });
        */
        
    });
    
});
