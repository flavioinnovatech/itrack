var circle;
jQuery(document).ready(function(){
	
  jQuery("#circlearea").html("<i>Nenhuma cerca eletrônica selecionada.</i>")

  create_map();
  
  //If the user wants to edit a previous created geofence
  if (g) {
  	var wkt_f = new OpenLayers.Format.WKT();
  	var ploaded = wkt_f.read(g['polygon']);
  	vlayer.addFeatures([ploaded]);
  	multispectral.setCenter( new OpenLayers.LonLat(ploaded.geometry.getCentroid().x,ploaded.geometry.getCentroid().y),1)
  }
	
  //calculates the center of the circle
  $('#step2circle').submit(function() {
  	address =  $('#circleaddress').attr("value");
  	number = $('#circlenumber').attr("value");
  	city = $('#circlecity').attr("value");
  	state = $("#circleselect option:selected").text();
  	radius = $('#radius').attr("value") / 100;
	
	if(address != '' && number != '' && city != '' && state != '') {
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
	}
	else {
		jQuery("#generaldialog").html("");
        jQuery("#generaldialog").attr("title","Endereço(s) incorreto(s)");
        $("#generaldialog").append("Por favor preencha todos os campos para o endereço.");
        jQuery("#generaldialog").dialog({show: "blind",modal:true});
	}
	
	return false;
	
  });

  jQuery("#circlesave").click(function(){
  	var id="";
  	
  	if(g) {
  		id = g['id'];
  	}
  	
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
        {name:geofencename,type:'circle', coords: circle.toString(),id:id},
        function (data) {
          if (data == 'create_finish') {
            location.href = "/geofence/create/finish";
          }
          else if (data == 'edit_finish') {
            location.href = "/geofence/edit/finish";
          }
          else {
            alert ('Erro na criação de cerca eletrônica.')
          }
          
        }
       
      );
    }
  });

});

var vlayer;
function create_map() {
  vlayer = new OpenLayers.Layer.Vector("Editable",{eventListeners: {sketchstarted: function(evt) {vlayer.destroyFeatures();}},onFeatureInsert: function(	feature	) { circle = (feature.geometry.toString()); area = (feature.geometry.getGeodesicArea()/1000000).toFixed(2); jQuery("#circlearea").html(area + " km²");} });

  var options = {
      units: 'm'
  };
  multispectral = new OpenLayers.Map('map3',options);

  var dm_wms = new OpenLayers.Layer.WMS(
      "Canadian Data",
      "http://187.61.51.164/GeoportalWMS/TileServer.aspx",
      {
          layers: "multispectral",
          format: "image/gif"
      },{isBaseLayer: true,tileSize: new OpenLayers.Size(256, 256),transitionEffect:'resize',minScale: 300});

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
}