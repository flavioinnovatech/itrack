$(document).ready( function() {
    $(".alertdialog").click( function(){
        jQuery("#generaldialog").html("");
        jQuery("#generaldialog").attr("title","Dados do alerta");
        id = (jQuery(this).attr('id'));
        
        jQuery.post(
            "/alerts/load/",
            {id:id},

            function(data){
              $("#generaldialog").append("<p style='font-size:16px'><b>  "+data['name']+" </b></p><hr/>");
              $("#generaldialog").append("<p><b>Enviado por:</b>  "+data['sender']+"</p>");
              $("#generaldialog").append("<p><b>Ativo:</b>  "+data['active']+"</p>");
              $("#generaldialog").append("<p><b>Início do monitoramento:</b>  "+data['time_start']+"</p>");
              $("#generaldialog").append("<p><b>Fim do monitoramento:</b>  "+data['time_end']+"</p>");
              $("#generaldialog").append("<p><b>Notificação por Popup:</b>  "+data['receive_popup']+"</p>");
              $("#generaldialog").append("<p><b>Notificação por Email:</b>  "+data['receive_email']+"</p>");
              $("#generaldialog").append("<p><b>Notificação por SMS:</b> "+data['receive_sms']+"</p>")
              $("#generaldialog").append("<p><b>Evento:</b> "+data['event']+"</p>");
              $("#generaldialog").append("<p><b>Alertar quanto:</b> "+data['when']+"</p>");
              $("#generaldialog").append("<p><b>Veículo(s):</b> "+data['vehicles']+"</p>");
              $("#generaldialog").append("<p><b>Notificado(s):</b> "+data['destinataries']+"</p>");

            },'json'
         );
        
        jQuery("#generaldialog").dialog({show: "blind",modal:true});
        });
    });
