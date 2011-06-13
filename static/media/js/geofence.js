////////////////// Função para habiliar o POST
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

$(document).ready(function(){
  
  
  $("#savecircle").attr('disabled','disabled');
  $("#saveroute").attr('disabled','disabled');
  // $("#savepolygon").attr('disabled','disabled');
/*======================================================  MAP LOAD ======================================================*/
  var geocoder;
  var map;
  var infowindow = new google.maps.InfoWindow();
  var marker;
  var directionDisplay;
  var directionsService = new google.maps.DirectionsService();
  
  geocoder = new google.maps.Geocoder();
  var latlng = new google.maps.LatLng(-14.239424,-53.186502);
  var myOptions = {
  	zoom: 4,
  	center: latlng,
  	mapTypeId: 'roadmap'
  }
  
  directionsDisplay = new google.maps.DirectionsRenderer();
  map = new google.maps.Map(document.getElementById("map"), myOptions);
  directionsDisplay.setMap(map);
  creator = new PolygonCreator(map);
  creator.destroy();
  
  google.maps.event.trigger(map, 'resize');
  map.setZoom( map.getZoom() );
  
  google.maps.event.addListener(map, "mousemove", function(){
     google.maps.event.trigger(map, 'resize'); 
   }); 

  map.setZoom( map.getZoom() - 1);
  map.setZoom( map.getZoom() + 1);

  

  var input = "-22.896359,-47.060092";
  var latlngStr = input.split(",",2); 
  var lat = parseFloat(latlngStr[0]);
  var lng = parseFloat(latlngStr[1]);
  var latlng = new google.maps.LatLng(lat, lng);
  // geocoder.geocode({'latLng': latlng}, function(results, status) {
    // if (status == google.maps.GeocoderStatus.OK) {
      // if (results[1]) {
        // map.setZoom(16);
        // marker = new google.maps.Marker({
          // position: latlng, 
          // map: map
        // });
        // infowindow.setContent(results[1].formatted_address);
        // infowindow.open(map, marker);
      // } else {
        // alert("No results found");
      // }
    // } else {
      // alert("Geocoder failed due to: " + status);
    // }

    // directionsDisplay.setMap(map);
    
// });
  
/*======================================================  END MAP LOAD ======================================================*/
// google.maps.event.addListener(map,"mousemove",function(point){
   // $("#lat").val( point.latLng.lat() );
   // $("#lng").val( point.latLng.lng() );
// });

/*======================================================  CIRCLE ======================================================*/
// $(document).ready(function(){

  $("#circletool").click(function() {
    creator.destroy();
      
    if (isNaN(parseInt($("#radius").val()))) {
      alert('Digite um número válido para o raio');
    }

    else {
  
      // alert('Clique para escolher centro do círculo');

      google.maps.event.addDomListenerOnce(map,"click",function(point){
      
          radius = parseInt($("#radius").val());
    
          circle = new google.maps.Circle({
            center : point.latLng,
            map : map,
            strokeColor : "#FFAA00",
            radius : radius
          });
          
           $("#savecircle").removeAttr('disabled');
           
          /*$.post({
               url: "/geofence/",
               data: {geo1 = {lat = point.latLng.lat(),lng = point.latLng.lng(), r = radius}}
               success: function(msg){
                 alert( "Data Saved: " + msg );
               }
          });*/
      
      });
    }
  
  });

   $("#savecircle").click(function(){
    
     coords = {lat: circle.center.lat(), lng: circle.center.lng(), radius: circle.radius};
     //alert(coords.toSource());
     $('#id_geoentities').remove();
     $.post(
        "/geofence/save/",
        {type:'circle', coords: coords, system : window.location.pathname.split("/")[3]},
        function(data){
            $('form').append("<input type='hidden' name='geoentities' id='id_geoentities' value='"+data+"' />");
            $("#dialog").dialog("close");
        }
     );
   });
  


/*====================================================== END CIRCLE ======================================================*/
/*======================================================  ROUTE ======================================================*/
  $("#routetool").click(function(){
    creator.destroy();

      // alert('Selecione uma rua para origem e outra para destino');

      google.maps.event.addListenerOnce(map,"click",function(point){
      
        var start = point.latLng

        google.maps.event.addListenerOnce(map,"click",function(point){ 

        var request = {
          origin:start, 
          destination:point.latLng,
          travelMode: google.maps.DirectionsTravelMode.DRIVING
        };
        directionsService.route(request, function(result, status) {
          if (status == google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(result);
          
            $("#saveroute").removeAttr('disabled');
          }
      
          else {
            alert('Rota inválida');
          }
        });
      
      });
    });
  });
  
  $("#saveroute").click(function(){
    alert('ae');
  });

/*====================================================== END ROUTE ======================================================*/

/*====================================================== POLYGON START ======================================================*/

  $("#polygontool").click(function(){
    
    creator = new PolygonCreator(map);
        
  });
  
  $("#savepolygon").click(function(){
    creator.destroy();
    alert(creator.showData());
  });

/*====================================================== POLYGON END ======================================================*/

});





