jQuery(document).ready(function(){
  
  var toolnow = null;
  jQuery("img[id=maptools]").click(function() {

    if (!toolnow) {
      toolnow = jQuery(this).attr('class');
    }

    if(jQuery("#tabs-3left").css("width") == "0px") {
      jQuery("#tabs-3right").css("width","79%");
      jQuery("#tabs-3left").css("width","20%");
      
    }
    else {

      if (jQuery(this).attr('class') == toolnow) {
        jQuery("#tabs-3right").css("width","100%");
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
                	jQuery("#list4").jqGrid('delRowData', equip.id);
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
          caption: "Cercas eletrõnicas",
          
          onSelectRow: function(id,status){ 
            
            if (status == true) {

              jQuery.each(globalgeofences, function(key,data) {

                if (data.id == id) {

                  if(data.type == 'C') {
                    
                    var polygon = [];
                    
                    jQuery.each (data.polygon[0][0], function(key1,point) {
                      var latlng = new google.maps.LatLng(point[1], point[0]);
                      polygon.push(latlng)
                      
                    });
                                        
                    bermudaTriangle = new google.maps.Polygon({
                      paths: polygon,
                      strokeColor: "#FF0000",
                      strokeOpacity: 0.8,
                      strokeWeight: 2,
                      fillColor: "#FF0000",
                      fillOpacity: 0.35
                    });
                    
                    bermudaTriangle.setMap(map);
                    
                    geofence[id] = bermudaTriangle;
                  }
                  
                  if(data.type == "P") {
                    
                     var polygon = [];

                      jQuery.each (data.polygon[0][0], function(key1,point) {
                        var latlng = new google.maps.LatLng(point[1], point[0]);
                        polygon.push(latlng)

                      });

                      bermudaTriangle = new google.maps.Polygon({
                        paths: polygon,
                        strokeColor: "#FF0000",
                        strokeOpacity: 0.8,
                        strokeWeight: 2,
                        fillColor: "#FF0000",
                        fillOpacity: 0.35
                      });

                      bermudaTriangle.setMap(map);

                      geofence[id] = bermudaTriangle;
                  
                  }
                  
                  if (data.type == "R") {
                      var bermudaTriangle = []
                      jQuery.each (data.polygon[0], function(key1,polygons) {
                        
                        var polygon = [];
                        
                        jQuery.each (polygons, function(key2,point) {
                          var latlng = new google.maps.LatLng(point[1], point[0]);
                          polygon.push(latlng)
                        });
                                                
                        bermudaTriangle[key1] = new google.maps.Polygon({
                          paths: polygon,
                          strokeColor: "#FF0000",
                          strokeOpacity: 0.8,
                          strokeWeight: 2,
                          fillColor: "#FF0000",
                          fillOpacity: 0.35,
                          map:map
                        });
                        
                        // bermudaTriangle[key1].setMap(map);
                        
                        return false;

                      });
                      
                      geofence[id] = bermudaTriangle;
                  }

                }  

              });

            }
            
            else {
              
              try{
                geofence[id].setMap(null);
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
        jQuery("table.ui-jqgrid-htable").css("width","180px");

      });
    }
  });
    
});


function loadlateralgrid () { 

	if (globaldata == null)
		return;
    // if ( jQuery("#tabs-3left").css("width") > "0px" ) {
      
      // jQuery.getJSON("/rastreamento/loadData",function(data){
        // if (olddata != null) {
        //   alert (olddata.toSource());
        // }
        // else{
        //   alert ('null');
        // }

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
                
        var markers = new Array;
        
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
              var latlng = new google.maps.LatLng(lat, lng);
              
              marker = new google.maps.Marker({
                position: latlng, 
                map: map
              });
              
              map.setCenter(latlng);
              
              markers[rowid] = marker;
            
            }
            
            else {
              markers[rowid].setMap(null);
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
          jQuery("table.ui-jqgrid-htable").css("width","180px");
          
      
      olddata = data;
  //}
  
}

  

  
