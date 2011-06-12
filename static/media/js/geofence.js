$(document).ready(function(){
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
  
  // directionsDisplay = new google.maps.DirectionsRenderer();
  
  map = new google.maps.Map(document.getElementById("map"), myOptions);

  var input = "-22.896359,-47.060092";
  var latlngStr = input.split(",",2); 
  var lat = parseFloat(latlngStr[0]);
  var lng = parseFloat(latlngStr[1]);
  var latlng = new google.maps.LatLng(lat, lng);
  geocoder.geocode({'latLng': latlng}, function(results, status) {
  	if (status == google.maps.GeocoderStatus.OK) {
  		if (results[1]) {
  			map.setZoom(16);
  			marker = new google.maps.Marker({
  				position: latlng, 
  				map: map
  			});
  			infowindow.setContent(results[1].formatted_address);
  			infowindow.open(map, marker);
  		} else {
  			alert("No results found");
  		}
  	} else {
  		alert("Geocoder failed due to: " + status);
  	}

    // directionsDisplay.setMap(map);
    
});
  
/*======================================================  END MAP LOAD ======================================================*/
// google.maps.event.addListener(map,"mousemove",function(point){
   // $("#lat").val( point.latLng.lat() );
   // $("#lng").val( point.latLng.lng() );
// });

/*======================================================  CIRCLE ======================================================*/

var markersArray = [];

$("#circletool").click(function(){

  alert('Clique para escolher origem do círculo');

  google.maps.event.addListener(map,"click",function(point){
    
      if (markersArray) {
          for (i in markersArray) {
            markersArray[i].setMap(null);
          }
        }
      
    
      radius = parseInt($("#radius").val());
    
      circle = new google.maps.Circle({
        center : point.latLng,
        map : map,
        strokeColor : "#FFAA00",
        radius : radius
      });
      
      markersArray.push(circle);
      google.maps.event.clearListeners(map, 'click');

      /*$.post({
           url: "/geofence/",
           data: {geo1 = {lat = point.latLng.lat(),lng = point.latLng.lng(), r = radius}}
           success: function(msg){
             alert( "Data Saved: " + msg );
           }
      });*/
    
  });
  
  

});
/*====================================================== END CIRCLE ======================================================*/

/*======================================================  ROUTE ======================================================*/
$("#routetool").click(function(){

    alert('Selecione uma rua para origem e outra para destino');

    google.maps.event.addListener(map,"click",function(point){
      
      var start = point.latLng

      google.maps.event.addListener(map,"click",function(point){

      // var start = "São Paulo";
      //       var end = "Campinas";
      var request = {
        origin:start, 
        destination:point.latLng,
        travelMode: google.maps.DirectionsTravelMode.DRIVING
      };
      directionsService.route(request, function(result, status) {
        if (status == google.maps.DirectionsStatus.OK) {
          directionsDisplay.setDirections(result);
        }
      
        else {
          alert('Rua inválida');
        }
      });
      google.maps.event.clearListeners(map, 'click');
      
    });
    });
    
    

});

/*====================================================== END ROUTE ======================================================*/

});




