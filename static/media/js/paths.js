var map;
var markersarray = [];
var infoarray = [];
jQuery(document).ready(function(){

    // jQuery("#send").click(function(){
    //        jQuery.post(
               // "/paths/load/",
               //         {
               //             vehicle: jQuery("#id_vehicle").val(),
               //             period_start: jQuery("#id_period_start").val(),
               //             period_end: jQuery("#id_period_end").val(),
               //             geofence: jQuery("#id_geofence").val()
               //         },
               //         function(data){
    //                
    //                //cleaning the mess
    //                for(i=0;i<markersarray.length;i++){
    //                    markersarray[i].setMap(null);
    //                    infoarray[i].setMap(null);
    //                }
    //                if (typeof bermudaTriangle != 'undefined') bermudaTriangle.setMap(null);
    //                if (typeof flightPath != 'undefined') flightPath.setMap(null);
    //                
    //                
    //                //drawing the markers
    //                jQuery.each(data[0], function(key,pnt){
    //                    var latlng = new google.maps.LatLng(pnt[0], pnt[1]);
    //                    
    //                    var marker = new google.maps.Marker({
    //                        position: latlng, 
    //                        map: map
    //                    });
    //                    
    //                    var infowindow = new google.maps.InfoWindow({
    //                        content: key
    //                    });
    //                    
    //                    google.maps.event.addListener(marker, 'click', function() {
    //                        infowindow.open(map,marker);
    //                    });
    //                    
    //                    markersarray.push(marker);
    //                    infoarray.push(infowindow);                    
    //                });
    //                //end drawing the markers
    //                
    //                //drawing the geofence
    //                if (data[1] != {}){
    //                    if(data[1]["type"] == 'C') {
    //                        
    //                        var polygon = [];
    //                        
    //                        jQuery.each (data[1]['coords'][0][0], function(key,point) {
    //                          var latlng = new google.maps.LatLng(point[1], point[0]);
    //                          polygon.push(latlng)
    //                          
    //                        });
    //                                            
    //                        bermudaTriangle = new google.maps.Polygon({
    //                          paths: polygon,
    //                          strokeColor: "#FF0000",
    //                          strokeOpacity: 0.8,
    //                          strokeWeight: 2,
    //                          fillColor: "#FF0000",
    //                          fillOpacity: 0.35
    //                        });
    //                        
    //                        bermudaTriangle.setMap(map);
    //                        
    //                      }
    //                      if(data[1]["type"] == "P") {
    //                    
    //                     var polygon = [];
    // 
    //                      jQuery.each (data[1]['coords'][0][0], function(key1,point) {
    //                        var latlng = new google.maps.LatLng(point[1], point[0]);
    //                        polygon.push(latlng)
    // 
    //                      });
    // 
    //                      bermudaTriangle = new google.maps.Polygon({
    //                        paths: polygon,
    //                        strokeColor: "#FF0000",
    //                        strokeOpacity: 0.8,
    //                        strokeWeight: 2,
    //                        fillColor: "#FF0000",
    //                        fillOpacity: 0.35
    //                      });
    // 
    //                      bermudaTriangle.setMap(map);
    //                  
    //                  }
    //                  if (data[1]["type"] == "R") {
    //                    var flightPlanCoordinates = []
    //                    
    //                    jQuery.each (data[1]['coords'], function(key1,point) {
    //                      var latlng = new google.maps.LatLng(point[1], point[0]);
    //                      flightPlanCoordinates.push(latlng);
    //                    });
    //                                        
    //                    var flightPath = new google.maps.Polyline({
    //                        path: flightPlanCoordinates,
    //                        strokeColor: "#FF0000",
    //                        strokeOpacity: 1.0,
    //                        strokeWeight: 2
    //                    });
    // 
    //                    flightPath.setMap(map);
    //                    
    //                    map.setCenter(flightPlanCoordinates[0]);
    //                    
    //                    geofence[id] = flightPath;
    //                      
    //                  }
    //                }
    //                
    //            });
    //    });
    
    map = new OpenLayers.Map('map');
    vlayer = new OpenLayers.Layer.Vector("vectors");
    
    var styleMap = new OpenLayers.StyleMap({'strokeWidth': 5, 'strokeColor': '#ff0000'});
    rlayer = new OpenLayers.Layer.Vector("routes", {styleMap: styleMap});
    var dm_wms = new OpenLayers.Layer.WMS(
        "Canadian Data",
        "http://187.61.51.164/GeoportalWMS/TileServer.aspx",
        {
            layers: "multispectral",
            format: "image/gif"
        },{isBaseLayer: true,tileSize: new OpenLayers.Size(256, 256),transitionEffect:'resize',minScale: 30000000});
        
    map.addLayer(dm_wms);
    map.addLayer(vlayer);
    map.addLayer(rlayer);
    map.setCenter(new OpenLayers.LonLat(-49.47,-16.40),0);
    map.addControl(new OpenLayers.Control.MousePosition());
    
    jQuery("#send").click(function(){
      
     openloading();
      
      vlayer.destroyFeatures();
      
      jQuery.post(
      "/paths/load/",
        {
            vehicle: jQuery("#id_vehicle").val(),
            period_start: jQuery("#id_period_start").val(),
            period_end: jQuery("#id_period_end").val(),
            geofence: jQuery("#id_geofence").val(),
            vehicle_other:jQuery("#id_vehicle_other").val()
        },
        function(data){
          
          collection = new OpenLayers.Geometry.Collection();
          
          jQuery.each(data[0], function(key,pnt){
            point = new OpenLayers.Geometry.Point(parseFloat(pnt[1]),parseFloat(pnt[0]));
            collection.addComponents(point);
          });
          
          center = new OpenLayers.LonLat(collection.getCentroid().x,collection.getCentroid().y);
          
          if (!jQuery.isEmptyObject( data[1] )){   
            var wkt_f = new OpenLayers.Format.WKT();
            var ploaded = wkt_f.read(data[1]['coords']);
            
            if (ploaded.geometry.CLASS_NAME == 'OpenLayers.Geometry.LineString') {
                            
              ploaded.style = {
                              strokeColor: "blue",
                              strokeWidth: 10,
                              cursor: "pointer"
              };

            }
            
            rlayer.addFeatures(ploaded);
            
            collection.addComponents(ploaded.geometry);
            center = new OpenLayers.LonLat(collection.getCentroid().x,collection.getCentroid().y);
            collection.removeComponents(ploaded.geometry);
          }
          
          thevector = new OpenLayers.Feature.Vector(collection);
          vlayer.addFeatures(thevector);
          
          map.setCenter(center,2);
          
          closeloading();
          
        });
    });

    
    jQuery(".main-form").css("height","700px");

  
});
