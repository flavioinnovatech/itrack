var map;
var markersarray = [];
var infoarray = [];
jQuery(document).ready(function(){

    jQuery("#send").click(function(){
        jQuery.post(
            "/paths/load/",
            {
                vehicle: jQuery("#id_vehicle").val(),
                period_start: jQuery("#id_period_start").val(),
                period_end: jQuery("#id_period_end").val(),
                geofence: jQuery("#id_geofence").val()
            },
            function(data){
                
                //cleaning the mess
                for(i=0;i<markersarray.length;i++){
                    markersarray[i].setMap(null);
                    infoarray[i].setMap(null);
                }
                if (typeof bermudaTriangle != 'undefined') bermudaTriangle.setMap(null);
                if (typeof flightPath != 'undefined') flightPath.setMap(null);
                
                
                //drawing the markers
                jQuery.each(data[0], function(key,pnt){
                    var latlng = new google.maps.LatLng(pnt[0], pnt[1]);
                    
                    var marker = new google.maps.Marker({
                        position: latlng, 
                        map: map
                    });
                    
                    var infowindow = new google.maps.InfoWindow({
                        content: key
                    });
                    
                    google.maps.event.addListener(marker, 'click', function() {
                        infowindow.open(map,marker);
                    });
                    
                    markersarray.push(marker);
                    infoarray.push(infowindow);                    
                });
                //end drawing the markers
                
                //drawing the geofence
                if (data[1] != {}){
                    if(data[1]["type"] == 'C') {
                        
                        var polygon = [];
                        
                        jQuery.each (data[1]['coords'][0][0], function(key,point) {
                          var latlng = new google.maps.LatLng(point[1], point[0]);
                          polygon.push(latlng)
                          
                        });
                                            
                        bermudaTriangle = new google.maps.Polygon({
                          paths: polygon,
                          strokeColor: "#FF0000",
                          strokeOpacity: 0.8,
                          strokeWeight: 2,
                          fillColor: "#FF0000",
                          fillOpacity: 0.35
                        });
                        
                        bermudaTriangle.setMap(map);
                        
                      }
                      if(data[1]["type"] == "P") {
                    
                     var polygon = [];

                      jQuery.each (data[1]['coords'][0][0], function(key1,point) {
                        var latlng = new google.maps.LatLng(point[1], point[0]);
                        polygon.push(latlng)

                      });

                      bermudaTriangle = new google.maps.Polygon({
                        paths: polygon,
                        strokeColor: "#FF0000",
                        strokeOpacity: 0.8,
                        strokeWeight: 2,
                        fillColor: "#FF0000",
                        fillOpacity: 0.35
                      });

                      bermudaTriangle.setMap(map);
                  
                  }
                  if (data[1]["type"] == "R") {
                    var flightPlanCoordinates = []
                    
                    jQuery.each (data[1]['coords'], function(key1,point) {
                      var latlng = new google.maps.LatLng(point[1], point[0]);
                      flightPlanCoordinates.push(latlng);
                    });
                                        
                    var flightPath = new google.maps.Polyline({
                        path: flightPlanCoordinates,
                        strokeColor: "#FF0000",
                        strokeOpacity: 1.0,
                        strokeWeight: 2
                    });

                    flightPath.setMap(map);
                    
                    map.setCenter(flightPlanCoordinates[0]);
                    
                    geofence[id] = flightPath;
                      
                  }
                }
                
            });
    });

    jQuery('.datepicker').datetimepicker({
        showSecond: true,
        timeFormat: 'hh:mm:ss',
        dateFormat: 'yy-mm-dd'
    });
    
    jQuery(".main-form").css("height","700px");

    var geocoder;

	var infowindow = new google.maps.InfoWindow();
	var marker;
	var coords;
	geocoder = new google.maps.Geocoder();


  
  	var input = "-22.896359,-47.060092";
	var latlngStr = input.split(",",2); 
	var lat = parseFloat(latlngStr[0]);
	var lng = parseFloat(latlngStr[1]);
	var latlng = new google.maps.LatLng(lat, lng);
	var myOptions = {
		zoom: 4,
		center: latlng,
		mapTypeId: 'roadmap'
	}
	map = new google.maps.Map(document.getElementById("map"), myOptions);
    google.maps.event.addListener(map, "mousemove", function(pos){
        jQuery("#lat").val(pos.latLng.lat().toFixed(10));
        jQuery("#lng").val(pos.latLng.lng().toFixed(10));
    });
    
});