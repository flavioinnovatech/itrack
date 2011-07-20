jQuery(document).ready(function(){
  jQuery('.commanddialog').click(function(){
    jQuery("#generaldialog").html("");
    jQuery("#generaldialog").attr("title","Dados do comando");

    id = (jQuery(this).attr('id'));

    jQuery.post(
        "/commands/load/",
        {id:id},
        
        function(data){
          alert(data.toSource());
          $("#generaldialog").append("<p><b>Veículo:</b>  "+data['vehicle']+"</p>")
          $("#generaldialog").append("<p><b>"+data['type']+":</b>  "+data['action']+"</p>")
          $("#generaldialog").append("<p><b>Data enviada:</b>  "+data['time_sent']+"</p>")
          $("#generaldialog").append("<p><b>Data recebida:</b>  "+data['time_received']+"</p>")
          $("#generaldialog").append("<p><b>Data recebida:</b>  "+data['time_executed']+"</p>")
          $("#generaldialog").append("<p><b>Estado:</b></p>")
          
        },'json'
     );

    jQuery("#generaldialog").dialog({show: "blind",modal:true});
  });
});