//Global variables
var polygon;

jQuery(document).ready(function(){
  
  //Polygon
  $("#addpoint").click(function(){
    var i = $("input[id^=polygoninput]").size() + 1;
     $('<p align="center"><span>'+i+'.</span><input placeholder="Ex.:Rua Anchieta,Campinas" type="text" id="polygoninput'+i+'" /></p>').appendTo('#polygoninputs');
     i++;
  });
  
  jQuery("#polygonarea").html("<i>Nenhuma cerca eletrônica selecionada.</i>")
  
  multispectral2 = new OpenLayers.Map('map2');
  
  var dm_wms2 = new OpenLayers.Layer.WMS(
      "Canadian Data",
      "http://187.61.51.164/GeoportalWMS/TileServer.aspx",
      {
          layers: "multispectral",
          format: "image/gif"
      },{isBaseLayer: true,tileSize: new OpenLayers.Size(256, 256),transitionEffect:'resize',minScale: 30000000});

  vlayer2 = new OpenLayers.Layer.Vector( "Editable",{eventListeners: {sketchstarted: function(evt) {vlayer2.destroyFeatures();}},onFeatureInsert: function(	feature	) {polygon = (feature);area = (feature.geometry.getGeodesicArea()/1000000).toFixed(2); jQuery("#polygonarea").html(area + " km²");}});
  vlayer2.events.on({"afterfeaturemodified": function(feature){
        polygon = (feature.feature);
        area = (feature.feature.geometry.getGeodesicArea()/1000000).toFixed(2);
        jQuery("#polygonarea").html(area + " km²");
 }});

  multispectral2.addLayer(dm_wms2);
  multispectral2.addLayer(vlayer2);
  multispectral2.setCenter(new OpenLayers.LonLat(-49.47,-16.40),0); 
  
  //Control Panel
  panel = new OpenLayers.Control.Panel({'displayClass': 'olControlEditingToolbar'});
  var nav = new OpenLayers.Control.Navigation();
  draw_ctl = new OpenLayers.Control.DrawFeature(vlayer2, OpenLayers.Handler.Polygon, {'displayClass': 'olControlDrawFeaturePolygon'});
  var mod = new OpenLayers.Control.ModifyFeature(vlayer2, {'displayClass': 'olControlModifyFeature'});
  controls = [nav, draw_ctl,mod];
  panel.addControls(controls);
  multispectral2.addControl(panel);
  multispectral2.addControl(new OpenLayers.Control.MousePosition());
  
  if (g) {
  	var wkt_f = new OpenLayers.Format.WKT();
	var ploaded = wkt_f.read(g['polygon']);
	vlayer2.addFeatures([ploaded]);
  }
  
  jQuery("#polygonsave").click(function(){
   geofencename = $("#polygoname").val();
    if(!geofencename) { 
      alert("Por favor digite um nome para a cerca eletrônica.");
    }
    if(!polygon) { 
      alert("Por favor digite um nome para a cerca eletrônica.");
      }
    else {
      //Save geofence
      $.post(
        "/geofence/save/",
        {name:geofencename,type:'polygon', coords: polygon.geometry.toString()},
        function(data){
          if (data == 'success') {
            alert('Cerca eletrônica salva com sucesso.');
          }
          else {
            alert('Erro na criação da cerca eletrônica.');
          }

        }
      );
    }
   });
  });