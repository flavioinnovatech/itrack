$(document).ready(function(){
  
  var toolnow = null;
  $("img[id=maptools]").click(function() {

    if (!toolnow) {
      toolnow = $(this).attr('class');
    }

    if($("#tabs-3left").css("width") == "0px") {
      $("#tabs-3right").css("width","79%");
      $("#tabs-3left").css("width","20%");
      
    }
    else {

      if ($(this).attr('class') == toolnow) {
        $("#tabs-3right").css("width","100%");
        $("#tabs-3left").css("width","0px");     
      }
      toolnow = $(this).attr('class');

    }
  });

  $("img.vehicle").click(function(){
    $("#gbox_list").show();
    $("#gbox_list1").hide();
  });
  
  var globaldata = null;
  $("img.geofence").click(function(){
    
    $("#gbox_list").hide();
    $("#gbox_list1").show();
    
    // $('#list').jqGrid('GridUnload');
    
    if ( $("#tabs-3left").css("width") > "0px" ) { 

      $.getJSON("/geofence/load/",function(data){
        globaldata = data;
        //montar cabeçalhos
        var colModel = [];
        var colNames = [];
        
        colNames.push("Nome");
        colModel.push({name:"Nome",align:"center"});
        colNames.push("id");
        colModel.push({name:"id",hidden:true});
        
        
        myData = [];
        object = new Object;
        $.each(colNames, function(key, name) {
            object[name] = "";
        });
        
        $.each(data, function(key, geofence) {
          
          object = new Object;
          $.each(colNames, function(key, name) {
          
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

              $.each(globaldata, function(key,data) {

                if (data.id == id) {

                  if(data.type == 'C') {
                    var latlng = new google.maps.LatLng(data.coords.lat, data.coords.lng);

                    circle = new google.maps.Circle({
                      center : latlng,
                      map : map,
                      strokeColor : "#FFAA00",
                      radius : data.coords.radius
                    });
                    
                    map.setCenter(latlng);
                    
                    geofence[id] = circle;
                  }
                  
                  if(data.type == "P") {
                    
                    var polygon = [];
                    
                    $.each (data.coords, function(key1,point) {
                      var latlng = new google.maps.LatLng(point.lat, point.lng);
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

                }  

              });

            }
            
            else {
              geofence[id].setMap(null);
            }
            
          } 
        }); 

          var i = 0;
          $.each(myData, function(key, item) { 
            jQuery("#list1").jqGrid('addRowData',item.id,item);
            i = i+1;
          });
          
          $("table#list1").css("width","180px");
          $("table.ui-jqgrid-htable").css("width","180px");

      });
    }
  });
    
});


function loadlateralgrid () { 
    // if ( $("#tabs-3left").css("width") > "0px" ) {
      
      // $.getJSON("/rastreamento/loadData",function(data){
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
        $.each(colNames, function(key, name) {
            object[name] = "";
        });
        $.each(data, function(key, equip) {              
          
          object["id"] = equip.id;
          
            $.each(colNames, function(key, name) {
          
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
              lat = $('#list4').jqGrid('getCell',rowid,'Latitude');
              lng = $('#list4').jqGrid('getCell',rowid,'Longitude');
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
          $.each(myData, function(key, item) { 
            
            if (olddata != null) {
            
              $.each(olddata, function(key2,olditem) {
                if (olditem.id == item.id) {
                  jQuery("#list").jqGrid('delRowData', item.id);
                }
              });
            }
            
            jQuery("#list").jqGrid('addRowData',item.id,item);
            i = i+1;
          });
          
          //$("#list_cb").css("width","180px");
          $("table#list").css("width","180px");
          $("table.ui-jqgrid-htable").css("width","180px");
          
      
      olddata = data;
  //}
  
}

  

  

