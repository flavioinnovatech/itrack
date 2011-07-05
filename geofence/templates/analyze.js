function collectcirclepoints(){
    var zoom = map.getZoom();
    var normalProj = G_NORMAL_MAP.getProjection();
  	var centerPt = normalProj.fromLatLngToPixel(centerMarker.getPoint(),zoom);
  	var radiusPt = normalProj.fromLatLngToPixel(radiusMarker,zoom);
    with (Math){
	    var radius = floor(sqrt(pow((centerPt.x-radiusPt.x),2) + pow((centerPt.y-radiusPt.y),2)));
        for (var a = 0 ; a < 361 ; a+=10 ){
        	var aRad = a*(PI/180);
        	y = centerPt.y + radius * sin(aRad)
        	x = centerPt.x + radius * cos(aRad)
        	var p = new GPoint(x,y);
            if(holemode){
        	    holePoints.push(normalProj.fromPixelToLatLng(p, zoom));
            }else{
                polyPoints.push(normalProj.fromPixelToLatLng(p, zoom));
            }
	    }
        if(holemode){
            var helper = [];
            var k = 0;
            var j = holePoints.length;
            for (var i = j-1; i>-1; i--) {
                helper[k] = holePoints[i];
                k++;
            }
            holePoints = helper;
        }
    }
}


dist = 50;
                    m = (actual.Ja - previous.Ja)/(actual.Ia - previous.Ia);
                    m = -1/m;
                    n = previous.Ja - m*previous.Ia;
                    // y = m*x + n
                    C = - dist*dist + previous.Ja*previous.Ja + previous.Ia*previous.Ia -2*previous.Ja*n;
                    A = 1 + m*m;
                    B = 2*m*n - 2*previous.Ia - 2*m*previous.Ja;
                    
                    x1=-B/2/A+Math.pow(Math.pow(B,2)-4*A*C,0.5)/2/A;
                    x2=-B/2/A-Math.pow(Math.pow(B,2)-4*A*C,0.5)/2/A;
                    
                    y1 = m*x1 + n;
                    y2 = m*x2 + n;

                    p1 = new google.maps.LatLng(x1,y1);
                    p2 = new google.maps.LatLng(x2,y2);
                    
                    alert(p1);
                    alert(p2);
                    alert(actual);
                    
                    marker1 = new google.maps.Marker({position:p1, map: map});
                    marker2 = new google.maps.Marker({position:p2, map: map});
                    
                    
                    
                    
                     var linha = new google.maps.Polyline({
                        path: [latlng_p,actual],
                        strokeColor: "#FF0000",
                        strokeOpacity: 0.5,
                        strokeWeight: 1,
                        map:map
                      });
