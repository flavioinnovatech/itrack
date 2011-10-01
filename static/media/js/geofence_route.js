var route;

$(document).ready(function(){

	loadmap();

	$("#addpointroute").click(function(){
    var i = $("input[id^=routeinput]").size() + 1;
    
    var content =  ($("#routeinputs ol li").html());
    
    $("<li>"+content+"</li>").appendTo('#routeinputs ol');
    i++;
  });
  
  $("#step1route").submit(function(){
  	
  	//TODO: put loading in this submit
  	
  	vlayer3.destroyFeatures();
  	routeaddresses = [];
  	routepoints = [];
  	var wait = 1;
  	
  	tolerance = $("#routetolerance").val();
  	
	if(tolerance == '') {
		jQuery("#generaldialog").html("");
		jQuery("#generaldialog").attr("title", "Faltando campo Tolerância");
		$("#generaldialog").append("Por favor preencha o campo tolerância");
		jQuery("#generaldialog").dialog({
			show : "blind",
			modal : true
		});
	}

	else {
	  	//For each address do the Geocode, get the coordinates and mount an array
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
	 		} else {
		  		jQuery("#generaldialog").html("");
	        	jQuery("#generaldialog").attr("title","Endereço(s) incorreto(s)");
	        	$("#generaldialog").append("Por favor preencha todos os campos para cada endereço.");
	        	jQuery("#generaldialog").dialog({show: "blind",modal:true});
		  	}
	    	
	  	});
	  	
	  	if (routeaddresses[0]) {
	  		//Post only one time an array of addresses
			$.post("/geofence/geocode/", {
				addresses : routeaddresses
			}, function(data) {
				
				var points = data;
				
				// alert(points.toSource());
				
				$.post("/geofence/route/", {
					points : points,
					tolerance:tolerance
				}, function(data) {
					
					multiline = [];
					test = [];
					
					for (var i in data){
						var pnt = new OpenLayers.Geometry.Point(data[i]['lng'],data[i]['lat']);
						test.push(pnt);
						pnt2 = pnt.transform(new OpenLayers.Projection("EPSG:4326"), multispectral1.getProjectionObject());
						multiline.push(pnt2);

					}
					
					testline = new OpenLayers.Geometry.LineString(test);
					test = new OpenLayers.Feature.Vector(testline,null);
					
					wkt = new OpenLayers.Format.WKT();
					
					// alert(wkt.write(test));
										
					multiline2 = new OpenLayers.Geometry.LineString(multiline);
	
					var style_green =
			        {
			            strokeColor: "#00FF00",
			            strokeOpacity: 0.7,
			            strokeWidth: 6,
			            pointRadius: 6,
			            pointerEvents: "visiblePainted"
			        };
	
					polygonFeature = new OpenLayers.Feature.Vector(multiline2,null,style_green);
					
					center = new OpenLayers.LonLat(pnt2.x, pnt2.y);
	                                  	
	                vlayer3.addFeatures([polygonFeature]);
	                multispectral1.setCenter(center,15);
	
				},'json');
			}, 'json');
		
		}

	}
  	
  	return false;
  });

	
  jQuery("#routesave").click(function(){
  	var id="";
  	
  	if(g) {
  		id = g['id'];
  	}  
    
   geofencename = $("#circlename").val();
    if(!geofencename) { 
      alert("Por favor digite um nome para a cerca eletrônica.");
    }
    else if(!route) { 
      alert("Por favor digite um escolha uma cerca eletrônica.");
      }
    else {
      // Save geofence
      
      $.post(
        "/geofence/save/",
        {name:geofencename,type:'route', coords: route,id:id},
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

var vlayer3;
function loadmap(){
	
  var options = {
  	units: 'm'
  };
	
  multispectral1 = new OpenLayers.Map('map1',options);
  
  var dm_wms1 = load_wms();

  //FIXME: add support to editables routes

	vlayer3 = new OpenLayers.Layer.Vector("Editable", {
		onFeatureInsert : function(feature) {
			if (offset == 1) {
				if (circle)
					vlayer3.destroyFeatures(circle);
				var geometry = feature.geometry.clone();
				geometry.transform(multispectral1.getProjectionObject(), new OpenLayers.Projection("EPSG:4326"));
				circle = (geometry.toString());
				area = (feature.geometry.getArea() / 1000).toFixed(3);
				jQuery("#circlearea").html(area + " km²");
			}
			
			if (offset == 2) {
				if (polygon)
					vlayer3.destroyFeatures(polygon);
				var geometry = feature.geometry.clone();
				geometry.transform(multispectral1.getProjectionObject(), new OpenLayers.Projection("EPSG:4326"));
				polygon = (geometry.toString());
				area = (feature.geometry.getArea() / 1000).toFixed(3);
				jQuery("#circlearea").html(area + " km²");
			}
			
			if (offset == 3) {
				if (route)
					vlayer3.destroyFeatures(route);
					
				var geometry = feature.geometry.clone();
				geometry.transform(multispectral1.getProjectionObject(), new OpenLayers.Projection("EPSG:4326"));
				route = (geometry.toString());
				area = (feature.geometry.getLength() / 1000).toFixed(3);
				jQuery("#circlearea").html(area + " km");
			}
		}
	});

  /*
  vlayer3.events.on({"afterfeaturemodified": function(feature){
        polygon = (feature.feature);
        area = (feature.feature.geometry.getGeodesicArea()/1000000).toFixed(2);
        jQuery("#polygonarea").html(area + " km²");
 }});
 */

  multispectral1.addLayer(dm_wms1);
  
  //FIXME: same as above
  multispectral1.addLayer(vlayer3);
  
  multispectral1.setCenter(new OpenLayers.LonLat(-49.47,-16.40).transform(
        new OpenLayers.Projection("EPSG:4326"),
        multispectral1.getProjectionObject()
    ), 5);
  
  // multispectral1.setCenter(new OpenLayers.LonLat(-49.47,-16.40),0); 
  
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
