var circle;
jQuery(document).ready(function(){
	
  jQuery("#circlearea").html("<i>Nenhuma cerca eletrônica selecionada.</i>")

  // loadmap();
  
  //If the user wants to edit a previous created geofence
  if (g) {
  	var wkt_f = new OpenLayers.Format.WKT();
  	var ploaded = wkt_f.read(g['polygon']);
  	vlayer.addFeatures([ploaded]);
  	multispectral.setCenter( new OpenLayers.LonLat(ploaded.geometry.getCentroid().x,ploaded.geometry.getCentroid().y),1)
  }
	
  //calculates the center of the circle
  $('#step1circle').submit(function() {
  	address =  $('.routeinput').attr("value");
  	number = $('.routenumber').attr("value");
  	city = $('.routecity').attr("value");
  	state = $(".routestate option:selected").text();
  	radius = $('#routetolerance').attr("value");
	
	if(address != '' && number != '' && city != '' && state != '') {
		
		data = {};
		routeaddresses = [];
		data['address'] = address;
		data['number'] = number;
		data['city'] = city;
		data['state'] = state;
		routeaddresses.push(data);
		
		$.post(
	          "/geofence/geocode/",
	          {addresses:routeaddresses},
	          function (data) {
	            vlayer3.destroyFeatures();

	            var pntc = new OpenLayers.Geometry.Point(data[0]['lng'],data[0]['lat']);
				var pnt2c = pntc.transform(new OpenLayers.Projection("EPSG:4326"), multispectral1.getProjectionObject());
	          
	          	center = new OpenLayers.LonLat(pnt2c.x, pnt2c.y);
	          
	            var circle = OpenLayers.Geometry.Polygon.createRegularPolygon(pnt2c,radius, 50);
	            vlayer3.addFeatures([new OpenLayers.Feature.Vector(circle)]);
	            
	            //TODO: make zoom with te get vlayer extent
	            multispectral1.setCenter(center,15);
	            
    	          
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
	
	//TODO: change these alerts to modals
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

// var vlayer;
// function create_map() {
// 
	// vlayer = new OpenLayers.Layer.Vector("Editable", {
		// eventListeners : {
			// sketchstarted : function(evt) {
				// vlayer.destroyFeatures();
			// }
		// },
		// onFeatureInsert : function(feature) {
			// circle = (feature.geometry.toString());
			// area = (feature.geometry.getGeodesicArea() / 1000000).toFixed(2);
			// jQuery("#circlearea").html(area + " km²");
		// }
	// });
// 
// 
  // var options = {
      // //units: 'm'
  // };
  // multispectral = new OpenLayers.Map('map3',options);
// 
  // var dm_wms = load_wms();
//                       
  // multispectral.addLayer(dm_wms);
  // multispectral.addLayer(vlayer);
  // //multispectral.setCenter(new OpenLayers.LonLat(-47,-22),4);
  // multispectral.setCenter(new OpenLayers.LonLat(10.2, 48.9), 5);
  // //multispectral.setCenter(new OpenLayers.LonLat(-16.40,-49.47),4);
  // //multispectral.setCenter(new OpenLayers.LonLat(-54, -18), 5);
// 
  // //Control Panel
  // panel = new OpenLayers.Control.Panel({'displayClass': 'olControlEditingToolbar'});
  // var nav = new OpenLayers.Control.Navigation();
  // polyOptions = {sides: 40};
  // draw_ctl = new OpenLayers.Control.DrawFeature(vlayer, OpenLayers.Handler.RegularPolygon, {'displayClass': 'olControlDrawFeaturePolygon',handlerOptions: polyOptions});
  // var mod = new OpenLayers.Control.ModifyFeature(vlayer, {'displayClass': 'olControlModifyFeature'});
  // controls = [nav, draw_ctl];
  // panel.addControls(controls);
  // multispectral.addControl(panel);
  // multispectral.addControl(new OpenLayers.Control.MousePosition());
// }