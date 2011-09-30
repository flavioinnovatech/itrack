//Global variables
var polygon;
var markers,size,offset;

jQuery(document).ready(function(){
  
  //create_map_polygon();
  
  //Polygon
  $("#addpoint").click(function(){
    var i = $("input[id^=polygoninput]").size() + 1;
    
    var content =  ($("#polygoninputs ol li").html());
    
    $("<li>"+content+"</li>").appendTo('#polygoninputs ol');
    i++;
  });
  
  jQuery("#polygonarea").html("<i>Nenhuma cerca eletrônica selecionada.</i>")
  
    
  if (g) {
  	var wkt_f = new OpenLayers.Format.WKT();
  	var ploaded = wkt_f.read(g['polygon']);
  	vlayer2.addFeatures([ploaded]);
  	multispectral2.setCenter( new OpenLayers.LonLat(ploaded.geometry.getCentroid().x,ploaded.geometry.getCentroid().y),1)
  }
  

  $("#step1polygon").submit(function(){
  	routeaddresses = [];
	var prox = 1;

    $("#routeinputs ol li").each(function(){
    	
    	address =  $(".routeinput", this).val();
	    number =  $(".routenumber", this).val();
	    city =  $(".routecity", this).val();
	    state =  $(".routestate", this).val();	  
	   	
    	if(address != '' && number != '' && city != '' && state != '') {

	 			data = {};
	 			data['address'] = address;
	 			data['number'] = number;
	 			data['city'] = city;
	 			data['state'] = state;
	 			
	 			routeaddresses.push(data);
	 	}
    	
    	else {
	  		jQuery("#generaldialog").html("");
        	jQuery("#generaldialog").attr("title","Endereço(s) incorreto(s)");
        	$("#generaldialog").append("Por favor preencha todos os campos para cada endereço.");
        	jQuery("#generaldialog").dialog({show: "blind",modal:true});
        	prox = 0;
	  	}
    });
        
    if (prox) {
    	$.post("/geofence/geocode/", {
				addresses : routeaddresses
			}, function(data) {
				
				var points = data;
				
				ppol = []
				
				for (var i in points){
					p = new OpenLayers.Geometry.Point(points[i]['lng'],points[i]['lat']);
					p2 = p.transform(new OpenLayers.Projection("EPSG:4326"), multispectral1.getProjectionObject());
					ppol.push(p2);
				}
				
				var linear_ring = new OpenLayers.Geometry.LinearRing(ppol);
				
				polygonFeature = new OpenLayers.Feature.Vector(new OpenLayers.Geometry.Polygon([linear_ring]));
    			vlayer3.addFeatures([polygonFeature]);
    			
    			center = new OpenLayers.LonLat(p2.x, p2.y);
    			multispectral1.setCenter(center,15);
				
			}, 'json');
    }
    
    // var p1 = new OpenLayers.Geometry.Point(-46.62,-23.57);
    // var p2 = new OpenLayers.Geometry.Point(-47,-22);
    // var p3 = new OpenLayers.Geometry.Point(-48,-21);
//     
    // ll1 = new OpenLayers.LonLat(-46.62,-23.57);
    // ll2 = new OpenLayers.LonLat(-47,-22);
    // ll3 = new OpenLayers.LonLat(-48,-21);
//     
    // var points = [ll1,ll2,ll3];
//     
    // for (var i in points){
    	// j = parseInt(i) + parseInt(1);
    	// icon = new OpenLayers.Icon('/media/img/marker-blue-'+j+'.png', size, offset);
    	// markers.addMarker(new OpenLayers.Marker(points[i],icon));
	// }
//     
    // var linear_ring = new OpenLayers.Geometry.LinearRing([p1,p2,p3]);
//     
    // polygonFeature = new OpenLayers.Feature.Vector(new OpenLayers.Geometry.Polygon([linear_ring]));
    // vlayer2.addFeatures([polygonFeature]);
//     
    return false;
  });
  
  jQuery("#polygonsave").click(function(){
  	
    var id="";
  	
  	if(g) {
  		id = g['id'];
  	}  
    
   geofencename = $("#circlename").val();
    if(!geofencename) { 
      alert("Por favor digite um nome para a cerca eletrônica.");
    }
    else if(!polygon) { 
      alert("Por favor digite um escolha uma cerca eletrônica.");
      }
    else {
      //Save geofence
      $.post(
        "/geofence/save/",
        {name:geofencename,type:'polygon', coords: polygon.geometry.toString(),id:id},
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

function create_map_polygon() {
  
    var options = {
        units: 'm'
    };
   multispectral2 = new OpenLayers.Map('map2',options);

   var dm_wms2 = new OpenLayers.Layer.WMS(
       "Canadian Data",
       "http://187.61.51.164/GeoportalWMS/TileServer.aspx",
       {
           layers: "multispectral",
           format: "image/gif"
       },{isBaseLayer: true,tileSize: new OpenLayers.Size(256, 256),transitionEffect:'resize',minScale: 300});


	vlayer2 = new OpenLayers.Layer.Vector("Editable", {
		eventListeners : {
			sketchstarted : function(evt) {
			}
		},
		onFeatureInsert : function(feature) {
			if (polygon)
				vlayer2.destroyFeatures(polygon);
			polygon = (feature);
			area = (feature.geometry.getGeodesicArea() / 1000000).toFixed(2);
			jQuery("#circlearea").html(area + " km²");
		}
	});

   vlayer2.events.on({"afterfeaturemodified": function(feature){
         polygon = (feature.feature);
         area = (feature.feature.geometry.getGeodesicArea()/1000000).toFixed(2);
         jQuery("#circlearea").html(area + " km²");
  }});

   multispectral2.addLayer(dm_wms2);
   multispectral2.addLayer(vlayer2);
   multispectral2.setCenter(new OpenLayers.LonLat(-49.47,-16.40),0); 
   
   markers = new OpenLayers.Layer.Markers( "Markers" );
   multispectral2.addLayer(markers);
   size = new OpenLayers.Size(21,25);
   offset = new OpenLayers.Pixel(-(size.w/2), -size.h);

   //Control Panel
   panel = new OpenLayers.Control.Panel({'displayClass': 'olControlEditingToolbar'});
   var nav = new OpenLayers.Control.Navigation();
   draw_ctl = new OpenLayers.Control.DrawFeature(vlayer2, OpenLayers.Handler.Polygon, {'displayClass': 'olControlDrawFeaturePolygon'});
   var mod = new OpenLayers.Control.ModifyFeature(vlayer2, {'displayClass': 'olControlModifyFeature'});
   controls = [nav, draw_ctl,mod];
   panel.addControls(controls);
   multispectral2.addControl(panel);
   multispectral2.addControl(new OpenLayers.Control.MousePosition());
}