$(document).ready(function(){
	
	loadmap();
  
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
