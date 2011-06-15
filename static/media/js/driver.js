$(document).ready( function() {
    $(".driver").click( function(){
        //alert($(this).attr('value'));
        $("#driverprofile-"+$(this).attr('value')).dialog(
        {
            height:250,
            width:400
        }
        );
        });
    });
