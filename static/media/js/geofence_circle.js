var circle;
jQuery(document).ready(function(){
  jQuery("#circlearea").html("<i>Nenhuma cerca eletrônica selecionada.</i>")

  vlayer = new OpenLayers.Layer.Vector( "Editable");
  vlayer = new OpenLayers.Layer.Vector("Editable",{eventListeners: {sketchstarted: function(evt) {vlayer.destroyFeatures();}},onFeatureInsert: function(	feature	) { circle = (feature.geometry.toString()); area = (feature.geometry.getGeodesicArea()/1000000).toFixed(2); jQuery("#circlearea").html(area + " km²");} });

  multispectral = new OpenLayers.Map('map1');

  var dm_wms = new OpenLayers.Layer.WMS(
      "Canadian Data",
      "http://187.61.51.164/GeoportalWMS/TileServer.aspx",
      {
          layers: "multispectral",
          format: "image/gif"
      },{isBaseLayer: true,tileSize: new OpenLayers.Size(256, 256),transitionEffect:'resize',minScale: 30000000});

  multispectral.addLayer(dm_wms);
  multispectral.addLayer(vlayer);
  multispectral.setCenter(new OpenLayers.LonLat(-49.47,-16.40),0); 

  //Control Panel
  panel = new OpenLayers.Control.Panel({'displayClass': 'olControlEditingToolbar'});
  var nav = new OpenLayers.Control.Navigation();
  polyOptions = {sides: 40};
  draw_ctl = new OpenLayers.Control.DrawFeature(vlayer, OpenLayers.Handler.RegularPolygon, {'displayClass': 'olControlDrawFeaturePolygon',handlerOptions: polyOptions});
  var mod = new OpenLayers.Control.ModifyFeature(vlayer, {'displayClass': 'olControlModifyFeature'});
  controls = [nav, draw_ctl];
  panel.addControls(controls);
  multispectral.addControl(panel);
  multispectral.addControl(new OpenLayers.Control.MousePosition());

  jQuery("#circlesave").click(function(){
    geofencename = $("#circlename").val();
    if(!geofencename) { 
      alert("Por favor digite um nome para a cerca eletrônica.");
    }
    
    else if(!circle){
      alert("Por favor selecione uma cerca eletrônica antes.");
    }
  
    else {
      //Save geofence
      $.post(
        "/geofence/save/",
        {name:geofencename,type:'circle', coords: circle.toString()},
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