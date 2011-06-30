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
