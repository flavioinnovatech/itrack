jQuery(document).ready(function(){ 
  
  jQuery("#tabs-3left").hide();
  
  var toolnow = null;
  jQuery("img[id=maptools]").click(function() {

    if (!toolnow) {
      toolnow = jQuery(this).attr('class');
    }

    if(jQuery("#tabs-3left").css("display") == "none") {
      jQuery("#tabs-3right").css("width","79%");
       jQuery("#tabs-4").css("width","79%");
      jQuery("#tabs-3left").css("width","20%");
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
                  	
                  	vlayer.addFeatures([ploaded]);
                  	multispectral.zoomToExtent(vlayer.getDataExtent());
                    
                    geofence[id] = ploaded;
                  }
                  
                  
                  if (data.type == "R") {
                    var wkt_f = new OpenLayers.Format.WKT();
                  	var ploaded = wkt_f.read(data['polygon']);
                  	
                  	vlayer.addFeatures([ploaded]);
					multispectral.zoomToExtent(vlayer.getDataExtent());
                    
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


function loadlateralgrid () { 

	if (globaldata == null)
		return;
		
        //montar cabeçalhos
        var data = globaldata;
        var colModel = [];
        var colNames = [];
        
        //Campos fixos
        colNames.push("Latitude");
        colModel.push({name:"Latitude",hidden:true});
        colNames.push("Longitude");
        colModel.push({name:"Longitude",hidden:true});
        colNames.push("Placa");
        colModel.push({name:"Placa",align:"center"});
        
        //cria o objeto para cada linha
        var myData = [];
        var object = new Object;
        jQuery.each(colNames, function(key, name) {
            object[name] = "";
        });
        jQuery.each(data, function(key, equip) {              
          
          object["id"] = equip.id;
          
            jQuery.each(colNames, function(key, name) {
          
              //Campos fixos
              if (name == "Placa") {
                object[name] = equip.veiculo.license_plate;
              }
              
              
              //Custom fields
              else {
                
                object[name] = equip.info[name];
                
              }
              
          });
          
          myData.push(object);
        });
                
                        
        jQuery("#list").jqGrid({   
         	datatype: "local",
         	height:h-250,
         	width: 180,
         	colNames: colNames, 
         	colModel:colModel,
         	multiselect: true, 
         	caption: "Rastreamento veicular",
         	onSelectRow: function(rowid,status){ 
            if (status == true) {
              lat = jQuery('#list4').jqGrid('getCell',rowid,'Latitude');
              lng = jQuery('#list4').jqGrid('getCell',rowid,'Longitude');
              
              //Selects the row on the main grid
              if (jQuery("#list4").getGridParam('selarrrow') != 1)
              	jQuery("#list4").setSelection(rowid,'true');
              
              multimarkers[rowid] = new OpenLayers.Marker(new OpenLayers.LonLat(lng,lat),icon);
              markers.addMarker(multimarkers[rowid]);
              multispectral.setCenter(new OpenLayers.LonLat(lng,lat),2);
            
            }
            
            else {
              //Selects the row on the main grid
              if (jQuery("#list4").getGridParam('selarrrow') != 0)
                jQuery("#list4").setSelection(rowid,'false');
              	
              markers.removeMarker(multimarkers[rowid]);
            }
          }
        
        }); 

          var i = 0;
          jQuery.each(myData, function(key, item) { 
            
            if (olddata != null) {
            
              jQuery.each(olddata, function(key2,olditem) {
                if (olditem.id == item.id) {
                  jQuery("#list").jqGrid('delRowData', item.id);
                }
              });
            }
            
            jQuery("#list").jqGrid('addRowData',item.id,item);
            i = i+1;
          });
          
          //jQuery("#list_cb").css("width","180px");
          jQuery("table#list").css("width","180px");
          jQuery("table[aria-labelledby=gbox_list]").css("width","180px");
          
      
      olddata = data;
  //}
  
}

  

  

