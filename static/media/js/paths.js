var map;
var markersarray = [];
var infoarray = [];

var popupsarray = {};
var showpopup = null;

jQuery(document).ready(function(){

    map = new OpenLayers.Map('map');
    vlayer = new OpenLayers.Layer.Vector("vectors");
    
    var styleMap = new OpenLayers.StyleMap({'strokeWidth': 5, 'strokeColor': '#ff0000'});
    rlayer = new OpenLayers.Layer.Vector("routes", {styleMap: styleMap});
    // var dm_wms = new OpenLayers.Layer.WMS(
        // "Canadian Data",
        // "http://187.61.51.164/GeoportalWMS/TileServer.aspx",
        // {
            // layers: "multispectral",
            // format: "image/gif"
        // },{isBaseLayer: true,tileSize: new OpenLayers.Size(256, 256),transitionEffect:'resize',minScale: 30000000});
        
    var dm_wms = load_wms();
        
    map.addLayer(dm_wms);
    map.addLayer(vlayer);
    map.addLayer(rlayer);
    map.setCenter(new OpenLayers.LonLat(-49.47,-16.40).transform(
        new OpenLayers.Projection("EPSG:4326"),
        map.getProjectionObject()
    ),4);
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
          
          var markers = new OpenLayers.Layer.Markers( "Markers" );
          map.addLayer(markers);
          var size = new OpenLayers.Size(16,16);
          var offset = new OpenLayers.Pixel(-(size.w/2), -size.h+8);
          var icon = new OpenLayers.Icon('/media/img/marker.png',size,offset);
          
          jQuery.each(data[0], function(key,pnt){
            point = new OpenLayers.Geometry.Point(parseFloat(pnt[1]),parseFloat(pnt[0]));
            point2 = point.transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
            marker = new OpenLayers.Marker(new OpenLayers.LonLat(point2.x,point2.y),icon.clone())
            feature = new OpenLayers.Feature(vlayer, 
                                new OpenLayers.LonLat(point2.x,point2.y));
            popup = feature.createPopup(true);
            popup.setBackgroundColor("white");
            popup.setOpacity(0.9);
            popup.setContentHTML("<b>Data e hora: </b><br/>"+key);
            popup.hide();
            //popup.size = new OpenLayers.Size(400,400);
            popupsarray[point2.x.toString()+" "+point2.y.toString()]=popup;
            markers.map.addPopup(popup);
            
            marker.events.register('mousedown', marker, function(evt) { 
                        point2=evt.object.lonlat;   
                        popupsarray[point2.lon.toString()+" "+point2.lat.toString()].toggle();                   
                        popupsarray[point2.lon.toString()+" "+point2.lat.toString()].updateSize();
                        OpenLayers.Event.stop(evt);
            });
            
            markers.addMarker(marker);
            //collection.addComponents(point2);
          });

          center = new OpenLayers.LonLat(collection.getCentroid().x,collection.getCentroid().y);
          
          if (!jQuery.isEmptyObject( data[1] )){   
            var wkt_f = new OpenLayers.Format.WKT();
            var ploaded = wkt_f.read(data[1]['coords']);
            
            // var geometry = ploaded.geometry.clone();
			ploaded.geometry.transform(new OpenLayers.Projection("EPSG:4326"),map.getProjectionObject());
            
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
          
          map.zoomToExtent(markers.getDataExtent(),1);
          
          closeloading();
          
        });
    });

    
    jQuery(".main-form").css("height","700px");

  
});
