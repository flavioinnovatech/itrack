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
                alert(data);
            }
              );
    
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
    var map;

  
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
