function drawPolyRoute(result){
	    for (i=0;i<result.routes.length;i++){
                previous = result.routes[i].overview_path[0];
                top_points = [];
                bottom_points = [];
                lastbrng = 0;
                
                var p1 = new LatLon(result.routes[i].overview_path[1].lat(),result.routes[i].overview_path[1].lng());
                var p2 = new LatLon(result.routes[i].overview_path[0].lat(),result.routes[i].overview_path[0].lng());
                
                brng = p1.bearingTo(p2);
                p3 = p2.destinationPoint(brng-90,0.1);
                p4 = p2.destinationPoint(brng+90,0.1);
                
                p3_google = new google.maps.LatLng(p3.lat(),p3.lon());
                p4_google = new google.maps.LatLng(p4.lat(),p4.lon());
                
                top_points.push(p4_google);
                bottom_points.push(p3_google);
                
                
                for(j=1;j<result.routes[i].overview_path.length;j++){
                    actual = result.routes[i].overview_path[j];
                    
                    var p1 = new LatLon(previous.lat(),previous.lng());
                    var p2 = new LatLon(actual.lat(),actual.lng());
                    
                    brng = p1.bearingTo(p2);
                    deltabrng = lastbrng - brng;
                    marker = new google.maps.Marker({position:actual, map: map, title: deltabrng.toString()});
                    
                    p3 = p2.destinationPoint(brng-90,10);
                    p4 = p2.destinationPoint(brng+90,10);
                    
                    
                    p3_google = new google.maps.LatLng(p3.lat(),p3.lon());
                    p4_google = new google.maps.LatLng(p4.lat(),p4.lon());
                    
                    
                    if((deltabrng < 180)&&(deltabrng > -180)){
                        top_points.push(p3_google);
                        bottom_points.push(p4_google);
                    }
                    
                    //marker = new google.maps.Marker({position:p3_google, map: map});
                    //marker = new google.maps.Marker({position:p4_google, map: map});
                    var flightPath = new google.maps.Polyline({
                      path: [p3_google,p4_google],
                      strokeColor: "#0000FF",
                      strokeOpacity: 1.0,
                      strokeWeight: 2,
                      map:map
                    });
                    lastbrng = brng;
                    previous = actual;
                }
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
    }
