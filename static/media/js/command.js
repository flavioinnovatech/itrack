jQuery(document).ready(function(){

  //command dialog	
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
  
  jQuery("#id_action_0").attr('checked',false);
  jQuery("#id_action_1").attr('checked',false);
  check();
  jQuery("#id_type").change(function(){check();});
  jQuery("#id_equipment").change(function(){check();});
  
});

function check() {
	if (jQuery("#id_equipment option:selected").html()!="(Selecione a placa)" && jQuery("#id_type option:selected").html()!="(selecione o Comando)"){
  		
  		vehicle = jQuery("#id_equipment option:selected").html();
  		command = jQuery("#id_type option:selected").html();
  		
  		
  		jQuery.post(
        "/commands/check/",
        {vehicle:vehicle,command:command},
        
        function(data){
          
          if (data['action'] == "OFF") {
          	jQuery("#id_action_1").attr('disabled',false);
          	jQuery("#id_action_1").attr('checked',true);
          	
          	jQuery("#id_action_0").attr('disabled',true);
          	jQuery("#id_action_0").attr('checked',false);
          } 
          
          else if (data['action'] == "ON"){
          	jQuery("#id_action_0").attr('disabled',false);
          	jQuery("#id_action_0").attr('checked',true);
          	
          	jQuery("#id_action_1").attr('disabled',true);
          	jQuery("#id_action_1").attr('checked',false);
          }
          
          else {
          	jQuery("#id_action_0").attr('disabled',false);
          	jQuery("#id_action_1").attr('disabled',false);
          }
          
        },'json'
     	);
  	}	
}
