jQuery(document).ready(function(){
  jQuery('.commanddialog').click(function(){
    jQuery("#generaldialog").html("");
    jQuery("#generaldialog").attr("title","Dados do comando");

    id = (jQuery(this).attr('id'));

    jQuery.post(
        "/commands/load/",
        {id:id},
        
        function(data){
          $("#generaldialog").append("<p><b>Veículo:</b>  "+data['vehicle']+"</p>")
          $("#generaldialog").append("<p><b>"+data['type']+":</b>  "+data['action']+"</p>")
          $("#generaldialog").append("<p><b>Enviado por:</b>  "+data['sender']+"</p>")
          $("#generaldialog").append("<p><b>Data enviada:</b>  "+data['time_sent']+"</p>")
          $("#generaldialog").append("<p><b>Data recebida:</b>  "+data['time_received']+"</p>")
          $("#generaldialog").append("<p><b>Data recebida:</b>  "+data['time_executed']+"</p>")
          $("#generaldialog").append("<p><b>Estado:</b></p>")
          
          if (data['state'] == 0) {
            $("#generaldialog").append('<p align="center"><img src="/media/img/command-1-big.png"></p>');
          }
          else if (data['state'] == 1) {
            $("#generaldialog").append('<p align="center"><img src="/media/img/command-2-big.png"></p>');
          }
          else if (data['state'] == 2) {
            $("#generaldialog").append('<p align="center"><img src="/media/img/command-3-big.png"></p>');
          }
          else if (data['state'] == 3) {
            $("#generaldialog").append('<p align="center"><img src="/media/img/command-fail-big.png"></p>');
          }
          
        },'json'
     );

    jQuery("#generaldialog").dialog({show: "blind",modal:true});
  });
});