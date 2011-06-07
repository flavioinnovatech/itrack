$("#map").ready(function(){
  
/*======================================================  MAP LOAD ======================================================*/
  var geocoder;
  var map;
  var infowindow = new google.maps.InfoWindow();
  var marker;
  geocoder = new google.maps.Geocoder();
  var latlng = new google.maps.LatLng(-14.239424,-53.186502);
  var myOptions = {
  	zoom: 4,
  	center: latlng,
  	mapTypeId: 'roadmap'
  }

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
  });
  
/*======================================================  END MAP LOAD ======================================================*/
google.maps.event.addListener(map,"mousemove",function(point){
   $("#lat").val( point.latLng.lat() );
   $("#lng").val( point.latLng.lng() );
});

/*======================================================  CIRCLE ======================================================*/

$("#circletool").click(function(){

  alert('Clique para escolher origem do círculo');

  google.maps.event.addListener(map,"click",function(point){
    
      radius = parseInt($("#radius").val());
    
      circle = new google.maps.Circle({
        center : point.latLng,
        map : map,
        strokeColor : "#FFAA00",
        radius : radius
      });
    
  });

});
/*====================================================== END CIRCLE ======================================================*/

/*======================================================  ROUTE ======================================================*/
$("#routetool").click(function(){

  alert('Clique para escolher origem e destino da rota');

  google.maps.event.addListener(map,"click",function(point){
      origin = point.latLng;
  });
  
  google.maps.event.addListener(map,"click",function(point){
      destiny = point.latLng;
  });
  
  alert(origin);
  alert(destiny);

});

/*====================================================== END ROUTE ======================================================*/

});




