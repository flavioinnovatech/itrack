$(document).ready( function() {
	/*
	$('#configs').click(function() {
        $.get("/rastreamento/xhrtest", function(data) {
            $("#tabs-6").html(data);

        });
    });
    */
});

function saveConfigs(){
    
    $("#id_custom_fields option:selected").each(function(){
        alert($(this).text());
        });
        
    $("#id_vehicles option:selected").each(function(){
        alert($(this).text());
        });
    
}


