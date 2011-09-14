$(document).ready(function(){

	loadmap();

	$("#addpointroute").click(function(){
    var i = $("input[id^=routeinput]").size() + 1;
    
    var content =  ($("#routeinputs ol li").html());
    
    $("<li>"+content+"</li>").appendTo('#routeinputs ol');
    i++;
  });
  
  $.post(
        "/geofence/geocode/",
        {address:address,number:number,city:city,state:state},
        function (data) { alert('ae');
          vlayer.destroyFeatures();
        
          lat = "-46.62";
          lng = "-23.57";
        
          var center = new OpenLayers.Geometry.Point(lat,lng);
          var circle = OpenLayers.Geometry.Polygon.createRegularPolygon(center,radius, 50);
          vlayer.addFeatures(new OpenLayers.Feature.Vector(circle));
        
        
        },'json'
     
  );
  
  
});

function loadmap(){
	
  multispectral1 = new OpenLayers.Map('map1');
  
  var dm_wms1 = new OpenLayers.Layer.WMS(
      "Canadian Data",
      "http://187.61.51.164/GeoportalWMS/TileServer.aspx",
      {
          layers: "multispectral",
          format: "image/gif"
      },{isBaseLayer: true,tileSize: new OpenLayers.Size(256, 256),transitionEffect:'resize',minScale: 30000000});

  //FIXME: add support to editables routes
  //vlayer3 = new OpenLayers.Layer.Vector( "Editable",{eventListeners: {sketchstarted: function(evt) {vlayer3.destroyFeatures();}},onFeatureInsert: function(	feature	) {polygon = (feature);area = (feature.geometry.getGeodesicArea()/1000000).toFixed(2); jQuery("#polygonarea").html(area + " km²");}});
  /*
  vlayer3.events.on({"afterfeaturemodified": function(feature){
        polygon = (feature.feature);
        area = (feature.feature.geometry.getGeodesicArea()/1000000).toFixed(2);
        jQuery("#polygonarea").html(area + " km²");
 }});
 */

  multispectral1.addLayer(dm_wms1);
  
  //FIXME: same as above
  //multispectral2.addLayer(vlayer2);
  
  
  multispectral1.setCenter(new OpenLayers.LonLat(-49.47,-16.40),0); 
  
  //Control Panel
  panel = new OpenLayers.Control.Panel({'displayClass': 'olControlEditingToolbar'});
  var nav = new OpenLayers.Control.Navigation();
  
  //FIXME: same as above
  //draw_ctl = new OpenLayers.Control.DrawFeature(vlayer2, OpenLayers.Handler.Polygon, {'displayClass': 'olControlDrawFeaturePolygon'});
  //var mod = new OpenLayers.Control.ModifyFeature(vlayer2, {'displayClass': 'olControlModifyFeature'});
  //controls = [nav, draw_ctl,mod];
  
  controls = [nav]
  
  panel.addControls(controls);
  multispectral1.addControl(panel);
  multispectral1.addControl(new OpenLayers.Control.MousePosition());
	
}