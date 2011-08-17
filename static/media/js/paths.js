var map;
var markersarray = [];
var infoarray = [];
jQuery(document).ready(function(){

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
