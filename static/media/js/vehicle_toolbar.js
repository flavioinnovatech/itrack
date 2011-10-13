jQuery(document).ready(function(){ 

  jQuery("#tabs-3left").hide();
  
  var toolnow = null;
  jQuery("img[id=maptools]").click(function() {

    if (!toolnow) {
      toolnow = jQuery(this).attr('class');
    }

    if(jQuery("#tabs-3left").css("display") == "none") {
      //alert(markersToDisplay.toSource());
      size = (jQuery('#tabs-3right').width() - 190).toString();
      jQuery("#tabs-3right").css("width",size+"px");
      jQuery("#tabs-4").css("width",size+"px");
      jQuery("#tabs-3left").css("width","190px");
      jQuery("#tabs-3left").show();
      
    }
    else {

      if (jQuery(this).attr('class') == toolnow) {
        jQuery("#tabs-3left").hide();
        //Tab do Google
        jQuery("#tabs-3right").css("width","100%");
        
        //Tab da Multispectral
        jQuery("#tabs-4").css("width","100%");
        
        jQuery("#tabs-3left").css("width","0px");     
      }
      toolnow = jQuery(this).attr('class');

    }
  });

  jQuery("img.vehicle").click(function(){
    jQuery("#gbox_list").show();
    
    jQuery("#gbox_list1").hide();
  });
 
  
  
  var globalgeofences = null;
  var oldgeofences = null;
  jQuery("img.geofence").click(function(){
    
    jQuery("#gbox_list").hide();
    jQuery("#gbox_list1").show();
    
    // jQuery('#list').jqGrid('GridUnload');
    
    if ( jQuery("#tabs-3left").css("width") > "0px" ) { 

      jQuery.getJSON("/geofence/load/",function(data){
        globalgeofences = data;
        //montar cabeçalhos
        var colModel = [];
        var colNames = [];
        
        colNames.push("Nome");
        colModel.push({name:"Nome",align:"center"});
        colNames.push("id");
        colModel.push({name:"id",hidden:true});
        
        
        myData = [];
        object = new Object;
        jQuery.each(colNames, function(key, name) {
            object[name] = "";
        });
        
        jQuery.each(data, function(key, geofence) {
        	
          if (oldgeofences != null) { 
            
            jQuery.each(oldgeofences, function(key2,olditem) {
            	if (olditem.id == geofence.id) {
                	jQuery("#list1").jqGrid('delRowData', geofence.id);
              }

            });
          }
          
          object = new Object;
          jQuery.each(colNames, function(key, name) {
          	
          
            if (name == "Nome") {
              object[name] = geofence.name;
            }
            
            if (name == "id") {
              object[name] = geofence.id
            }
              
          });
          
          myData.push(object);
        });
        
        var geofence = new Array;
        
        jQuery("#list1").jqGrid({   
          datatype: "local",
          height:h-250,
          width: 180,
          colNames: colNames, 
          colModel:colModel,
          multiselect: true, 
          caption: "Cercas eletrônicas",
          
          onSelectRow: function(id,status){ 
            
            if (status == true) {

              jQuery.each(globalgeofences, function(key,data) {

                if (data.id == id) {
                  if(data.type == 'C' || data.type == 'P') {
                                        
                    var wkt_f = new OpenLayers.Format.WKT();
                  	var ploaded = wkt_f.read(data['polygon']);
                  	
                  	ploaded.geometry.transform(new OpenLayers.Projection("EPSG:4326"),multispectral.getProjectionObject());
                  	
                  	vlayer.addFeatures([ploaded]);
                  	multispectral.zoomToExtent(vlayer.getDataExtent(),1);
                    
                    geofence[id] = ploaded;
                  }
                  
                  
                  if (data.type == "R") {
                    var wkt_f = new OpenLayers.Format.WKT();
                    
                  	var ploaded = wkt_f.read(data['route']);
                  	
                 	ploaded.geometry.transform(new OpenLayers.Projection("EPSG:4326"),multispectral.getProjectionObject());
                  	
                  	vlayer.addFeatures([ploaded]);
					multispectral.zoomToExtent(vlayer.getDataExtent(),1);
                    
                    geofence[id] = ploaded;
                      
                  }

                }  

              });

            }
            
            else {
              
              try{
                vlayer.removeFeatures(geofence[id]);
                multispectral.zoomToExtent(vlayer.getDataExtent());
              }
              catch(err) {
                jQuery.each (geofence[id],function(key,value) {
                  value.setMap(null);
                });
              }
            }
            
          } 
        }); 

		oldgeofences = myData;
			
        var i = 0;
        jQuery.each(myData, function(key, item) { 
        	jQuery("#list1").jqGrid('addRowData',item.id,item);
        	i = i+1;
        });
          
        jQuery("table#list1").css("width","180px");
        jQuery("table[aria-labelledby=gbox_list1]").css("width","180px");

      });
    }
  });
    
});

var olddata2 = null;
function loadlateralgrid () { 

	if (globaldata == null)
		return;
		
        //montar cabeçalhos
        var data = globaldata;
        var colModel = [];
        var colNames = [];
        nequips =0;
        //Campos fixos
        colNames.push("Latitude");
        colModel.push({name:"Latitude",hidden:true});
        colNames.push("Longitude");
        colModel.push({name:"Longitude",hidden:true});
        colNames.push("Hora");
        colModel.push({name:"Hora",hidden:true});
        colNames.push("Placa");
        colModel.push({name:"Placa",align:"center",key:true});
       
        
        h = jQuery(window).height();             
        var size = new OpenLayers.Size(16,16);
        var offset = new OpenLayers.Pixel(-(size.w/2), -size.h+8);
        var icon = new OpenLayers.Icon('/media/img/marker.png',size,offset);
        
        jQuery("#list").jqGrid({   
         	datatype: "local",
         	height:h-260,
         	//width: 180,
         	colNames: colNames, 
         	colModel:colModel,
         	multiselect: true,
         	//autoheight:true,
            autowidth: true, 
         	caption: "Rastreamento veicular:",
         	loadComplete: function(data) {
         		insertDataJqgrid2();
         
				jQuery("#googlemap").click(function() {
	
					if(selected == 0) {
	
						//clear the list to be filled
						jQuery("#list").resetSelection();
	
						jQuery.each(jQuery("#list").jqGrid('getRowData'), function(rowid, celldata) {
							plate = celldata["Placa"].replace(/(<([^>]+)>)/ig, "").replace(" ", "");
							if(markersToDisplay.hasOwnProperty(plate)) {
								//alert('plate:"' + plate + '",' + rowid);
	
								//alert(jQuery('#list').getRowData(rowid));
								jQuery("#list").setSelection(rowid);
							}
						});
						w = jQuery(window).width();
						h = jQuery(window).height();
						//habilita botao vehicle
						jQuery("img[class=vehicle]").show();
						jQuery("img[class=geofence]").show();
						jQuery("#tabs-3").css("height", h - 200);
						multispectral.updateSize();
					}
					selected = tab.tabs('option', 'selected');
				});

         	},
         	onSelectRow: function(rowid,status){ 
                //get the plate (dict key)                  
                plate = jQuery('#list').jqGrid('getCell',rowid,'Placa').replace(/(<([^>]+)>)/ig,"").replace(" ","");                
                if (status == true) {
                 
                  lat = jQuery('#list').jqGrid('getCell',rowid,'Latitude');
                  lng = jQuery('#list').jqGrid('getCell',rowid,'Longitude');
                  pnt = new OpenLayers.LonLat(lng,lat)
                  
                  pnt.transform(new OpenLayers.Projection("EPSG:4326"),multispectral.getProjectionObject());
                  //alert(pnt);
                  marker = new OpenLayers.Marker(pnt,icon.clone());
                  
                  if(!markersToDisplay.hasOwnProperty(plate)){
                    feature = new OpenLayers.Feature(vlayer, pnt);
                    popup = feature.createPopup(true);
                    popup.setBackgroundColor("white");
                    popup.setOpacity(0.9);
                   
                    popup.setContentHTML("<h1>"+plate+"</h1><b>Data e hora: </b><br/>"+jQuery('#list').jqGrid('getCell',rowid,'Hora'));
                    popup.hide();
            
                    popupsarray[pnt.lon.toString()+" "+pnt.lat.toString()]=popup;
                    
                    marker.events.register('mousedown', marker, function(evt) { 
                        pnt2=evt.object.lonlat;
                        
                        popupsarray[pnt2.lon.toString()+" "+pnt2.lat.toString()].toggle();                   
                        popupsarray[pnt2.lon.toString()+" "+pnt2.lat.toString()].updateSize();
                        OpenLayers.Event.stop(evt);
                    });
                    markersToDisplay[plate] = marker;
                    
                    showMarkersInMap();
                  }
                  //multispectral.zoomToExtent(markers.getDataExtent(),1);
                }
                else if(markersToDisplay.hasOwnProperty(plate)){
                	pnt = markersToDisplay[plate].lonlat;
                    delete markersToDisplay[plate];
                    delete popupsarray[pnt.lon.toString()+" "+pnt.lat.toString()];

                    showMarkersInMap();
              }

            }
        
        }); 
          
          //jQuery("#list_cb").css("width","180px");
          //jQuery("table#list").css("width","180px");
          //jQuery("table[aria-labelledby=gbox_list]").css("width","180px");
      
      olddata2 = data;
  //}
  
}

function insertDataJqgrid2(){


	//cria o objeto para cada linha
	var myData = [];
	var object = new Object;
	jQuery.each(colNames, function(key, name) {
		object[name] = "";
	});

	jQuery.each(globaldata, function(key, equip) {
		var object = new Object;
		object["id"] = equip.id;

		jQuery.each(colNames, function(key, name) {

			//Campos fixos
			if(name == "Placa") {
				object[name] = equip.veiculo.license_plate;
			} else if(name == "Latitude") {
				object[name] = equip.lat;
			} else if(name == "Longitude") {
				object[name] = equip.lng;
			}else if(name == "Hora") {
				object[name] = equip.hora.eventdate;
			}

		});
		nequips++;
		myData.push(clone(object));
	});
	
	var i = 0;
	jQuery.each(myData, function(key, item) {

		if(olddata2 != null) {
			jQuery.each(olddata2, function(key2, olditem) {
				if(olditem.id == item.id) {
					jQuery("#list").jqGrid('delRowData', item.id);
				}
			});
		}
		
		// Please don't mess this again
		jQuery("#list").jqGrid('addRowData',i,myData[i]);
		i = i + 1;
	});
	}


  

