var map;

jQuery(document).ready(function(){ 
  
  loadData();

  //loadGrid();
  
  jQuery("img[id=maptools]").easyTooltip();
  jQuery("img[class=fullscreen]").easyTooltip();
  
  setTimeout(function(){
    doTimer();
  },1000); 
  
  //desabilita vehicles toolbar quando gmaps nao é selecionado
  jQuery('a[href=#tabs-1]').click(function(){
   
    jQuery("img[id=maptools]").hide();
  });

  w = jQuery(window).width();
  h = jQuery(window).height();
  jQuery( "#tabs" ).tabs();
  // jQuery( "#tabs" ).css("top","130px");
  
  tabw = (jQuery("#tabs-1").width());
  tabh = (jQuery("#tabs-1").height());
  
  // document.body.style.overflow-x = "hidden";
  
  normal = 1;
  jQuery('img.fullscreen').click(function() {
    switch (normal) {
      
      case 1:
      //fullscren
        width = jQuery('#tabs').css("width");
        height= jQuery('#tabs').css("height");
        top =  parseInt(jQuery('#tabs').position().top);
        left =  jQuery('#tabs').css("left");
        top = parseInt(top);
      
        jQuery('#menuContainer').css("z-index","0");
        jQuery('#tabs').css("width",w);
        jQuery('#tabs').css("height",h);
        jQuery('#tabs').css("position","absolute");
        jQuery('#tabs').css("top","0");
        jQuery('#tabs').css("left","0");
        jQuery("#tabs-3").css("height","97%");
        jQuery("#tabs-3").css("width","97%");
        normal = 0;
        
        //resize do jqgrid
        jQuery("#list4").setGridWidth(w - 50);
        jQuery("#list4").setGridHeight(h - 150);
        
        break;
        
     case 0:
     jQuery('#tabs').css("position","inherit");
      jQuery('#menuContainer').css("z-index","2");
      jQuery('#tabs').css("width","960px");
      jQuery('#tabs').css("height",height);
      // jQuery('#tabs').css("top","130px" );
      jQuery('#tabs').css("left",( left ) );

      jQuery("#tabs-3").css("width", "924px");
      normal = 1;
      
      //resize jqgrid
      jQuery("#list4").setGridWidth(tabw);
      jQuery("#list4").setGridHeight(tabh - 80);

      break;
    }
    
    
  }); //end .fullscreen click function
    
  
// }); //end document.ready



/* --------------------------------------------- GOOGLE MAPS ------------------------------------------------------ */


jQuery("#googlemap").click(function() {
  w = jQuery(window).width();
  h = jQuery(window).height();
  //habilita botao vehicle
  jQuery("img[class=vehicle]").show();
  jQuery("img[class=geofence]").show();
  
  jQuery("#tabs-3").css("height",h-200);
  
  
});
	var geocoder;
	var infowindow = new google.maps.InfoWindow();
	var marker;
	geocoder = new google.maps.Geocoder();
	
	var input = "-22.896359,-47.060092";
	var latlngStr = input.split(",",2); 
	var lat = parseFloat(latlngStr[0]);
	var lng = parseFloat(latlngStr[1]);
	var latlng = new google.maps.LatLng(lat, lng);
	var myOptions = {
		zoom: 4,
		center: latlng,
		mapTypeId: 'roadmap'
	}
	
	//Works only for the first vehicle
  // if (jQuery("input[id^=jqg_list4_1]").is(':checked')) {
  //   
  // var lat = jQuery("td[aria-describedby=list4_Latitude]").text();
  // var lng = jQuery("td[aria-describedby=list4_Longitude]").text();
  // var latlng = new google.maps.LatLng(lat, lng);
  // geocoder.geocode({'latLng': latlng}, function(results, status) {
  //   if (status == google.maps.GeocoderStatus.OK) {
  //     if (results[1]) {
  //       map.setZoom(16);
  //       marker = new google.maps.Marker({
  //         position: latlng, 
  //         map: map
  //       });
  //       infowindow.setContent(results[1].formatted_address);
  //       infowindow.open(map);
  //     } else {
  //       alert("No results found");
  //     }
  //   } else {
  //     alert("Geocoder failed due to: " + status);
  //   }
  // });
  // }
  map = new google.maps.Map(document.getElementById("tabs-3right"), myOptions);
  google.maps.event.trigger(map, 'resize');
  map.setZoom( map.getZoom() );
   
  google.maps.event.addListener(map, "mousemove", function(){
    google.maps.event.trigger(map, 'resize'); 
  });
	
  
// });
/* --------------------------------------------- END GOOGLE MAPS ------------------------------------------------------ */

/* --------------------------------------------- BUSCAR DADOS E MONTAR TABELA ------------------------------------------------------ */

});

var globaldata;
function loadData() {
    jQuery.getJSON("/rastreamento/loadData",
        function(data){
            globaldata = data;
            
            loadGrid();
            loadlateralgrid();
        
    });
}

  
//var globaldata;
var olddata = null;
function loadGrid() {
  //jQuery('#list4').jqGrid('GridUnload');     

      //jQuery.getJSON("/rastreamento/loadData",
      //  function(data){
          var data = globaldata;

          //loadlateralgrid(data);
          
          //globaldata = data;
          //montar cabeçalhos
          var colModel = [];
          var colNames = [];
          
          //Campos fixos
          colNames.push("Latitude");
          colModel.push({name:"Latitude",hidden:true});
          colNames.push("Longitude");
          colModel.push({name:"Longitude",hidden:true});
          colNames.push("Placa");
          colModel.push({name:"Placa",align:"center",formatter:currencyFmatter});
          colNames.push("Tipo veículo");
          colModel.push({name:"Tipo veículo",align:"center"});
          colNames.push("Hora");
          colModel.push({name:"Hora",align:"center"});
          colNames.push("Endereço");
          colModel.push({name:"Endereço",align:"center"});
          
          //para cada veículo
          var nequips = 0;
          jQuery.each(data, function(key, equip) {
            nequips++;
            //para cada info
            jQuery.each(equip.info, function(key2,info){

              if (key2 == "Latitude" || key2 == "Longitude") {

              }
              
              else {
                colNames.push(key2);
                colModel.push({name:key2,align:"center"});
              }
            });
             
          });
          
          var markers = new Array;
          
          if (olddata == null) {
            jQuery("#list4").jqGrid({   
              datatype: "local",
              height:h-250,
              width: 930,
              colNames: colNames, 
              colModel:colModel,
              multiselect: true, 
              loadui:"block",
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
          
          }
          
          // jQuery("#load_list4").show();
          // jQuery("#lui_list4").show();
          
          //inserir dados
          
          //cria o objeto para cada linha
          myData = [];
          object = new Object;
          jQuery.each(colNames, function(key, name) {
              object[name] = "";
          });
          
          
          jQuery.each(data, function(key, equip) {
          
            if (olddata != null) { 
            
                jQuery.each(olddata, function(key2,olditem) {
                    if (olditem.id == equip.id) {
                        jQuery("#list4").jqGrid('delRowData', equip.id);
                    }
                });
            }
            
              jQuery.each(colNames, function(key, name) {
            
                //Campos fixos
                if (name == "Hora") {
                  object[name] = equip.hora.eventdate;
                }
                
                else if (name == "Tipo veículo") {
                  object[name] = equip.veiculo.type;
                }
                
                else if (name == "Placa") {
                  object[name] = equip.veiculo.license_plate;
                }
                
                //Geocode reverse RULES
                else if (name == "Endereço") {
                  var lat = object["Latitude"];
                  var lng = object["Longitude"];
                  var latlng = new google.maps.LatLng(lat,lng);
                  geocoder = new google.maps.Geocoder();
                  geocoder.geocode({'latLng': latlng}, function(results, status) {
                    if (status == google.maps.GeocoderStatus.OK) {
                      object[name] = results[0].formatted_address;
                    }
                    
                  });
                  
                  // object[name] = jQuery("#end").val();
                  
                }
                
                //Custom fields
                else {
                  
                  object[name] = equip.info[name];
                  
                }
                
            });
                
            

            setTimeout(function(){
              myData.push(object);
            },400);
            

            
          });

          
          var time = nequips*400 + 500;  
          
          setTimeout(function(){
              var i = 0;
              jQuery.each(myData, function(key, item) {
              
                jQuery("#list4").jqGrid('addRowData',i+1,item);
                i = i+1;
              });
              
              // jQuery("#load_list4").hide();
              // jQuery("#lui_list4").hide();
              
              //HACK
              jQuery("table#list4").css("width","931px");
              jQuery("table.ui-jqgrid-htable").css("width","931px");
            
          },time);
          
          olddata = data;

    //});
  

}

function doTimer() {
  setTimeout(function(){
    loadData();
    //loadlateralgrid();
    //loadGrid();
    doTimer();
  },30000);
}

function currencyFmatter (cellvalue, options, rowObject)
{
   link = "<a href='javascript:showVehicle(\""+cellvalue+"\")'>"+cellvalue+"</a> ";
   return link;
}

function showVehicle(vehicle) {
  
  jQuery("#vehicledialog").html("");
  jQuery("#vehicledialog").attr("title","Dados do veículo "+vehicle);
  
  jQuery.each(globaldata, function(key, equip) {
    jQuery.each(equip, function(key1, equipdata) {
      
      if (key1 == "veiculo" && equipdata.license_plate == vehicle) {
                
        jQuery.each(equipdata,function(key2,vehicledata) {
          jQuery("#vehicledialog").append("<p><b>"+key2+":</b>  "+vehicledata+"</p>");
          jQuery("#vehicledialog").dialog({show: "blind",modal:true});
        });  
      }     
    });
  });
  
}



function mapa_multi() {
	callMultispectral(-22.896359,-47.060092);
	//jQuery("#dialog").dialog({height: jQuery(window).height()},{ width : (jQuery(window).width() - 25)},{ closeText: 'X' }); 
	//jQuery(".ui-icon").css("background-image", "none");
	//jQuery(".ui-icon").css("text-indent", "0");
	
}
