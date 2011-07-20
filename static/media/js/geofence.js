
$(document).ready(function(){
  $(".main-form").css("height","600px");
  
  $("#accordion").accordion({ 
      autoHeight: true,
      collapsible: true
  });
  
  var geocoder;
	var map;
	var infowindow = new google.maps.InfoWindow();
	var marker;
	var coords;
	geocoder = new google.maps.Geocoder();
	
function drawPolyRoute(result){
	    for (i=0;i<result.routes.length;i++){
                previous = result.routes[i].overview_path[0];
                top_points = [];
                bottom_points = [];
                circle_points = [];
                lastbrng = 0;
                for(j=0;j<result.routes[i].legs.length;j++){
                    for(k=0;k<result.routes[i].legs[j].steps.length;k++){
                        for(l=0; l<result.routes[i].legs[j].steps[k].path.length; l++){
                            
                            actual = result.routes[i].legs[j].steps[k].path[l];
                            circle_points.push(actual);
                            
                            var p1 = new LatLon(previous.lat(),previous.lng());
                            var p2 = new LatLon(actual.lat(),actual.lng());
                    
                            brng = p1.bearingTo(p2);
                            deltabrng = lastbrng - brng;
                            
                            p3 = p1.destinationPoint(brng-90,0.1);
                            p4 = p1.destinationPoint(brng+90,0.1);

                            p3_google = new google.maps.LatLng(p3.lat(),p3.lon());
                            p4_google = new google.maps.LatLng(p4.lat(),p4.lon());
                    
                            top_points.push(p3_google);
                            bottom_points.push(p4_google);

                            circle = new google.maps.Circle({
                                center:actual,
                                map:map,
                                radius:100,
                                strokeColor: "#FF0000",
                                strokeOpacity: 0.8,
                                strokeWeight: 2,
                                fillColor: "#FF0000",
                                fillOpacity: 0.35,
                            });

                            lastbrng = brng;
                            previous = actual;
                        }
                    }
                        
            
                }
               
                
             /*
                var p1 = new LatLon(result.routes[i].overview_path[j-2].lat(),result.routes[i].overview_path[j-2].lng());
                var p2 = new LatLon(result.routes[i].overview_path[j-1].lat(),result.routes[i].overview_path[j-1].lng());
                
                brng = p1.bearingTo(p2);
                p3 = p2.destinationPoint(brng-90,0.1);
                p4 = p2.destinationPoint(brng+90,0.1);
                
                p3_google = new google.maps.LatLng(p3.lat(),p3.lon());
                p4_google = new google.maps.LatLng(p4.lat(),p4.lon());
                
                top_points.push(p3_google);
                bottom_points.push(p4_google);
            */
                
                
                points_list = top_points.concat(bottom_points.reverse());
                poligono = new google.maps.Polygon({
                    paths: points_list,
                    strokeColor: "#FF0000",
                    strokeOpacity: 0.8,
                    strokeWeight: 2,
                    fillColor: "#FF0000",
                    fillOpacity: 0.35,
                    map:map
                  });
                                 
         }
         
         return {polygon:points_list, points: circle_points};
    }
                    
	
	
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
     $("#lat").val(pos.latLng.lat().toFixed(10));
     $("#lng").val(pos.latLng.lng().toFixed(10));
   });
  
  creator = new PolygonCreator(map);
  
  var geofences = [];
  var circle = null;
  var geofencename = null;

  
  ///////////// Circle tools
  $("#circletool").click(function() {
    creator.destroy();
          
    if (isNaN(parseInt($("#radius").val()))) {
      alert('Digite um número válido para o raio');
    }

    else {
      
      //Only one geofence/time
      if (geofences.length > 0) {
        geofences[0].setMap(null);
        geofences.pop();
      }
      
      google.maps.event.addDomListenerOnce(map,"click",function(point){
      
        radius = parseInt($("#radius").val());

        circle = new google.maps.Circle({
          center : point.latLng,
          map : map,
          strokeColor : "#FFAA00",
          radius : radius
        });

        circlearea = Math.PI * radius * radius / 1000;
        circlearea = circlearea.toFixed(2);
        geofences.push(circle);

        $("#savecircle").removeAttr('disabled');
         
      });
      

      
    }
  
  });
  
  //Circle is marked with address input
  $("#circlesubmit").submit(function(){
    creator.destroy();
      
    if (isNaN(parseInt($("#radius").val()))) {
      alert('Digite um número válido para o raio');
    }
    
    else {
      
      //Only one geofence/time
      if (geofences.length > 0) {
        geofences[0].setMap(null);
        geofences.pop();
      }
      
      address = $("#circlecenter").attr("value");
      radius = parseInt($("#radius").val());
      
      geocoder.geocode( { 'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
          map.setCenter(results[0].geometry.location);
          position = results[0].geometry.location;
          
          circle = new google.maps.Circle({
            center : position,
            map : map,
            strokeColor : "#FFAA00",
            radius : radius
          });
          
          circlearea = Math.PI * radius * radius / 1000;
          circlearea = circlearea.toFixed(2);
          $("#circlearea").attr("value",circlearea)
          geofences.push(circle);
          
        } else {
          alert("Geocode was not successful for the following reason: " + status);
        }
      });
    }
    
  });
  
  //The save POST
  $("#savecircle").click(function(){
    
    if (circle) {
      coords = {lat: circle.center.lat(), lng: circle.center.lng(), radius: circle.radius};
      // alert(coords.toSource());
      $('#id_geoentities').remove();
      
      $("#generaldialog").html("");
      $("#generaldialog").attr("title","Salvar cerca eletrônica");
      $("#generaldialog").append("<p><b>Digite um nome para a cerca:</b></p>")
      $("#generaldialog").append("<p><input id='geofencename' type='text'></input></p>");
      
      
      $("#generaldialog").dialog({
        modal:true,
        show:'clip',
        buttons: {
          "Salvar": function() {
            geofencename = $("#geofencename").val();
            
            if(geofencename){ 
              $.post(
                "/geofence/save/",
                {name:geofencename,type:'circle', coords: coords, system : window.location.pathname.split("/")[3]},
                function(data){
                  $('form').append("<input type='hidden' name='geoentities' id='id_geoentities' value='"+data+"' />");
                  $("#dialog").dialog("close");
                }
              );
              
              $( this ).dialog( "close" );
            }
            
            else {
              alert('Digite um nome para a cerca eletrônica.')
            }
          },
          Cancel: function() {
            $( this ).dialog( "close" );
          }
        }
      });
      
             
    }
    
    else {
      alert("Selecione um círculo primeiro.");
    }
    
  });
  
  
  ///////////// Polygon tool  
  $("#polygontool").click(function(){
    creator.destroy();
    creator = new PolygonCreator(map);
    
      if (geofences.length > 0) {
        geofences[0].setMap(null);
        geofences.pop();
      }
      // computeArea(loop:
      //     Array.<LatLng>|
      //     MVCArray.<LatLng>, radius?:number)
    
     
  });
  
  // The save POST
  $("#savepolygon").click(function(){
    
    // var match = /\\(.+?\\)/.exec(creator.showData());
        
    // (-12.746114226507563, -52.9927091875)(-15.981071606666031, -43.9399748125)(-22.36906704273474, -56.4204435625)
    
    coords = {points: creator.showData()};
    
    $('#id_geoentities').remove();
      
    $("#generaldialog").html("");
    $("#generaldialog").attr("title","Salvar cerca eletrônica");
    $("#generaldialog").append("<p><b>Digite um nome para a cerca:</b></p>")
    $("#generaldialog").append("<p><input id='geofencename' type='text'></input></p>");
    
    $("#generaldialog").dialog({
      modal:true,
      show:'clip',
      buttons: {
        "Salvar": function() {
          geofencename = $("#geofencename").val();
          
          if(geofencename){ 
            $.post(
                "/geofence/save/",
                {name:geofencename,type:'polygon', coords: coords, system : window.location.pathname.split("/")[3]},
                function(data){
                    $('form').append("<input type='hidden' name='geoentities' id='id_geoentities' value='"+data+"' />");
                    $("#dialog").dialog("close");
                }
             );
            
            $( this ).dialog( "close" );
          }
          
          else {
            alert('Digite um nome para a cerca eletrônica.')
          }
        },
        Cancel: function() {
          $( this ).dialog( "close" );
        }
      }
    });
    
     
  });
  
  // Add inputs when desirable
  $("#addpoint").click(function(){
    var i = $("input[id^=polygoninput]").size() + 1;
     $('<input type="text" id="polygoninput'+i+'" />').appendTo('#polygoninputs');
     i++;
  });
  
  $("#polygonsubmit").submit(function(){
    
    creator.destroy();
    var directionDisplay;
    var directionsService = new google.maps.DirectionsService();
    directionsDisplay = new google.maps.DirectionsRenderer();
    directionsDisplay.setMap(map);

    if (geofences.length > 0) {
      geofences[0].setMap(null);
      geofences.pop();
    }
    
    var points = [];
    waypoints = [];
    var distance;

    var i = 0;
    $("input[id^=polygoninput]").each(function(){
      
      if ($(this).attr("value") == "")
        return false;
      
      i++;
      var address =  $(this).attr("value");

      geocoder.geocode( { 'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
          // map.setCenter(results[0].geometry.location);
          position = results[0].geometry.location;
          points.push(position);
          var waypoint = {location:position};
          waypoints.push(waypoint);

        } else {
          alert("Geocode was not successful for the following reason: " + status);
        }
      });
    });
    
    var time = $("input[id^=polygoninput]").size();
    time = time*40;
    setTimeout(function(){
     
      bermudaTriangle = new google.maps.Polygon({
          paths: points,
          strokeColor: "#FF0000",
          strokeOpacity: 0.8,
          strokeWeight: 2,
          fillColor: "#FF0000",
          fillOpacity: 0.35
        });
        
        area = google.maps.geometry.spherical.computeArea(bermudaTriangle.getPath());
        area = area/1000;
        area = area.toFixed(2);

    		$("#polygonarea").attr("value",area);
        
        map.setCenter(points[0]);
        
        geofences.push(bermudaTriangle);

        bermudaTriangle.setMap(map);
      
    },time); 
    
  });
  
  ///////////// Route
  // Add inputs when desirable
  $("#adddestiny").click(function(){
    var i = $("input[id^=routeinput]").size() + 1;
     $('<input type="text" id="routeinput'+i+'" />').appendTo('#routeinputs');
     i++;
  });
  
  //Route is marked with address input
  $("#routesubmit").submit(function(){
    if (typeof poligono != 'undefined') poligono.setMap(null);
    if (typeof directionsDisplay != 'undefined') directionsDisplay.setMap(null);
    creator.destroy();
    var directionDisplay;
    var directionsService = new google.maps.DirectionsService();
    directionsDisplay = new google.maps.DirectionsRenderer({
       draggable: true
     });
     directionsDisplay.setMap(map);
     google.maps.event.addListener(directionsDisplay, 'directions_changed', function() {
       distance = computeTotalDistance(directionsDisplay.directions);
       $("#routedistance").attr("value",distance);
     });
   
    if (geofences.length > 0) {
      geofences[0].setMap(null);
      geofences.pop();
    }
    
    var points = [];
    waypoints = [];
    var distance;

    var i = 0;
    $("input[id^=routeinput]").each(function(){
      
      if ($(this).attr("value") == "")
        return false;
      
      i++;
      var address =  $(this).attr("value");
      points.push(address);
      var waypoint = {location:address};
      waypoints.push(waypoint);
      realwaypoints = waypoints.slice();
      realwaypoints.pop();       
    });

    var request = {
      origin:points[0], 
      destination:points[(points.length)-1],
      optimizeWaypoints:true,
      waypoints:realwaypoints,
      travelMode: google.maps.DirectionsTravelMode.DRIVING
    };
    directionsService.route(request, function(result, status) {
      if (status == google.maps.DirectionsStatus.OK) {
        directionsDisplay.setDirections(result);
        
        for (i=0;i<result.routes.length;i++){ 
          for(j=0;j<result.routes[i].legs.length;j++){
            for(k=0;k<result.routes[i].legs[j].steps.length;k++){
              for(l=0; l<result.routes[i].legs[j].steps[k].path.length; l++){
                  var string =""
                  string += result.routes[i].legs[j].steps[k].path[l]
                  path.push(string);
              }
            }
          }
        }
        

        
        
        geofences.push(directionsDisplay);
        $("#saveroute").removeAttr('disabled');
      }

      else {
        alert('Rota inválida');
      }
    });





  });
  
  function computeTotalDistance(result) {
    var total = 0;
    var myroute = result.routes[0];
    for (i = 0; i < myroute.legs.length; i++) {
      total += myroute.legs[i].distance.value;
    }
    total = total / 1000.
    return total;
  }
  
  //Route tool
  var path=[];
  $("#routetool").click(function(){

     creator.destroy();
     if (typeof directionsDisplay != 'undefined') directionsDisplay.setMap(null);
     var directionDisplay;
     var directionsService = new google.maps.DirectionsService();
     directionsDisplay = new google.maps.DirectionsRenderer({
       draggable: true
     });
     directionsDisplay.setMap(map);
     google.maps.event.addListener(directionsDisplay, 'directions_changed', function() {
       distance = computeTotalDistance(directionsDisplay.directions);
       $("#routedistance").attr("value",distance);
     });
     
     if (geofences.length > 0) {
       geofences[0].setMap(null);
       geofences.pop();
     }
     if (typeof poligono != 'undefined') poligono.setMap(null);
     var points = [];
     waypoints = [];
     var realwaypoints = [];
     var route;
     
     google.maps.event.clearInstanceListeners(map);
     google.maps.event.addListener(map,"click",function(point){

       points.push(point);
           
       if (points.length >= 2) {
         
         var waypoint = {location:point.latLng};
         waypoints.push(waypoint);
         realwaypoints = waypoints.slice();
         realwaypoints.pop();
         
         var request = {
           origin:points[0].latLng, 
           destination:points[(points.length)-1].latLng,
           optimizeWaypoints:true,
           waypoints:realwaypoints,
           travelMode: google.maps.DirectionsTravelMode.DRIVING
         };
         if (typeof result != 'undefined') result.setMap(null);
         if (typeof poligono != 'undefined') poligono.setMap(null);
         directionsService.route(request, function(result, status) {
           if (status == google.maps.DirectionsStatus.OK) {
             directionsDisplay.setDirections(result);
             
            for (i=0;i<result.routes.length;i++){ 
              for(j=0;j<result.routes[i].legs.length;j++){
                for(k=0;k<result.routes[i].legs[j].steps.length;k++){
                  for(l=0; l<result.routes[i].legs[j].steps[k].path.length; l++){
                      var string =""
                      string += result.routes[i].legs[j].steps[k].path[l]
                      path.push(string);
                  }
                }
              }
            }          
                           
           }
           else {
             alert('Rota inválida');
           }
         });
       }
       });
       
       
    });

    $('#saveroute').click(function(){
                  
    // alert(path.toSource());
    $('#id_geoentities').remove();
      
    $("#generaldialog").html("");
    $("#generaldialog").attr("title","Salvar cerca eletrônica");
    $("#generaldialog").append("<p><b>Digite um nome para a cerca:</b></p>")
    $("#generaldialog").append("<p><input id='geofencename' type='text'></input></p>");
    
    $("#generaldialog").dialog({
      modal:true,
      show:'clip',
      buttons: {
        "Salvar": function() {
          geofencename = $("#geofencename").val();
          
          if(geofencename){ 
            $.post(
                "/geofence/save/",
                {name:geofencename,type:'route', system : window.location.pathname.split("/")[3],coords:path},
                
                // {name:geofencename,type:'route', coords: dict_to_send, system : window.location.pathname.split("/")[3]},
                function(data){
                    $('form').append("<input type='hidden' name='geoentities' id='id_geoentities' value='"+data+"' />");
                    $("#dialog").dialog("close");
                }
             );
            
            $( this ).dialog( "close" );
          }
          
          else {
            alert('Digite um nome para a cerca eletrônica.')
          }
        },
        Cancel: function() {
          $( this ).dialog( "close" );
        }
      }
    });
    
    
    
    });

});
  
