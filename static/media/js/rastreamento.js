var map;

jQuery(document).ready(function(){ 
  loadGrid();
  $("img[id=maptools]").easyTooltip();
  $("img[class=fullscreen]").easyTooltip();
  
  setTimeout(function(){
    doTimer();
  },1000); 
  
  //desabilita vehicles toolbar quando gmaps nao é selecionado
  $('a[href=#tabs-1]').click(function(){
   
    $("img[id=maptools]").hide();
  });

  w = $(window).width();
  h = $(window).height();
  $( "#tabs" ).tabs();
  // $( "#tabs" ).css("top","130px");
  
  tabw = ($("#tabs-1").width());
  tabh = ($("#tabs-1").height());
  
  // document.body.style.overflow-x = "hidden";
  
  normal = 1;
  $('img.fullscreen').click(function() {
    switch (normal) {
      
      case 1:
      //fullscren
        width = $('#tabs').css("width");
        height= $('#tabs').css("height");
        top =  parseInt($('#tabs').position().top);
        left =  $('#tabs').css("left");
        top = parseInt(top);
      
        $('#menuContainer').css("z-index","0");
        $('#tabs').css("width",w);
        $('#tabs').css("height",h);
        $('#tabs').css("position","absolute");
        $('#tabs').css("top","0");
        $('#tabs').css("left","0");
        $("#tabs-3").css("height","97%");
        $("#tabs-3").css("width","97%");
        normal = 0;
        
        //resize do jqgrid
        $("#list4").setGridWidth(w - 50);
        $("#list4").setGridHeight(h - 150);
        
        break;
        
     case 0:
     $('#tabs').css("position","inherit");
      $('#menuContainer').css("z-index","2");
      $('#tabs').css("width","960px");
      $('#tabs').css("height",height);
      // $('#tabs').css("top","130px" );
      $('#tabs').css("left",( left ) );

      $("#tabs-3").css("width", "924px");
      normal = 1;
      
      //resize jqgrid
      $("#list4").setGridWidth(tabw);
      $("#list4").setGridHeight(tabh - 80);

      break;
    }
    
    
  }); //end .fullscreen click function
    
  
// }); //end document.ready

/* --------------------------------------------- toolbar starts  ------------------------------------------------------ */

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

/* --------------------------------------------- toolbar end  ------------------------------------------------------ */

/* --------------------------------------------- GOOGLE MAPS ------------------------------------------------------ */


$("#googlemap").click(function() {
  w = $(window).width();
  h = $(window).height();
  //habilita botao vehicle
  $("img[class=vehicle]").show();
  $("img[class=geofence]").show();
  
  $("#tabs-3").css("height",h-200);
  
  
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
  // if ($("input[id^=jqg_list4_1]").is(':checked')) {
  //   
  // var lat = $("td[aria-describedby=list4_Latitude]").text();
  // var lng = $("td[aria-describedby=list4_Longitude]").text();
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
function loadGrid() {
  $('#list4').jqGrid('GridUnload');     
  
      $.getJSON("/rastreamento/loadData",
        function(data){
          globaldata = data;
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
          $.each(data, function(key, equip) {
            nequips++;
            //para cada info
            $.each(equip.info, function(key2,info){

              if (key2 == "Latitude" || key2 == "Longitude") {

              }
              
              else {
                colNames.push(key2);
                colModel.push({name:key2,align:"center"});
              }
            });
             
          });
          
          var markers = new Array;
          
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
          
          // $("#load_list4").show();
          // $("#lui_list4").show();
          
          //inserir dados
          
          //cria o objeto para cada linha
          myData = [];
          object = new Object;
          $.each(colNames, function(key, name) {
              object[name] = "";
          });
          
          
          $.each(data, function(key, equip) {              
            
              $.each(colNames, function(key, name) {
            
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
                  
                  // object[name] = $("#end").val();
                  
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
              $.each(myData, function(key, item) { 
                jQuery("#list4").jqGrid('addRowData',i+1,item);
                i = i+1;
              });
              
              // $("#load_list4").hide();
              // $("#lui_list4").hide();
              
              //HACK
              $("table#list4").css("width","931px");
              $("table.ui-jqgrid-htable").css("width","931px");
            
          },time);
          
          

    });
  

}

function doTimer() {
  setTimeout(function(){
    loadGrid();
    doTimer();
  },30000);
}

function currencyFmatter (cellvalue, options, rowObject)
{
   link = "<a href='javascript:showVehicle(\""+cellvalue+"\")'>"+cellvalue+"</a> ";
   return link;
}

function showVehicle(vehicle) {
  
  $("#vehicledialog").html("");
  $("#vehicledialog").attr("title","Dados do veículo "+vehicle);
  
  $.each(globaldata, function(key, equip) {
    $.each(equip, function(key1, equipdata) {
      
      if (key1 == "veiculo" && equipdata.license_plate == vehicle) {
                
        $.each(equipdata,function(key2,vehicledata) {
          $("#vehicledialog").append("<p><b>"+key2+":</b>  "+vehicledata+"</p>");
          $("#vehicledialog").dialog({show: "blind",modal:true});
        });  
      }     
    });
  });
  
}



function mapa_multi() {
	callMultispectral(-22.896359,-47.060092);
	//jQuery("#dialog").dialog({height: $(window).height()},{ width : ($(window).width() - 25)},{ closeText: 'X' }); 
	//jQuery(".ui-icon").css("background-image", "none");
	//jQuery(".ui-icon").css("text-indent", "0");
	
}
