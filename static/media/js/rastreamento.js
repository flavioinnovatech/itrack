//Global variables
var map;
var multispectral;
var markers,size,icon;
var multimarkers = new Array;
var collection = new OpenLayers.Geometry.Collection();
var tab;
var colNames;


/* extending array to allow the pushnew: push only if the value isn't in the array */
Array.prototype.pushNew=function(obj){
    if(this.indexOf(obj) == -1){
        this.push(obj);
        return true;
    }else{
        return false;
    }
}
/*end of extension*/


/* function to clone a object*/
function clone(obj) {
    // Handle the 3 simple types, and null or undefined
    if ((null == obj) || ("object" != typeof obj)) return obj;

    // Handle Date
    if (obj instanceof Date) {
        var copy = new Date();
        copy.setTime(obj.getTime());
        return copy;
    }

    // Handle Array
    if (obj instanceof Array) {
        var copy = [];
        var i =0;
        var len= obj.length;
        for (i = 0,len = obj.length; i < len; ++i) {
            copy[i] = clone(obj[i]);
        }
        return copy;
    }

    // Handle Object
    if (obj instanceof Object) {
        var copy = {};
        for (var attr in obj) {
            if (obj.hasOwnProperty(attr)) copy[attr] = clone(obj[attr]);
        }
        return copy;
    }

    throw new Error("Unable to copy obj! Its type isn't supported.");
}
/*end of function to clone a object*/


jQuery(document).ready(function(){ 
  
  openloading();
  
  loadData();
  loadmaps();
  

  
  jQuery("img[id=maptools]").tipTip();
  jQuery("img[class=fullscreen]").tipTip();
  
  //desabilita vehicles toolbar quando tabela é selecionada
  jQuery('a[href=#tabs-1]').click(function(){
    jQuery("img[id=maptools]").hide();
  });

  w = jQuery(window).width();
  h = jQuery(window).height();
  tab = jQuery( "#tabs" ).tabs();
  selected = tab.tabs('option', 'selected');


  $('.css3button').click(function(){
    tab.tabs('select', 1);
    jQuery("#tabs-3").css("height",h-200);
    multispectral.updateSize();
  });
  
  tabw = (jQuery("#tabs-1").width());
  tabh = (jQuery("#tabs-1").height());
  
  jQuery('.searchfield').keyup(function() {
  	loadData(jQuery('.searchfield').attr("value"));

  });
  
/* ---------------------------------------------  MAPS ------------------------------------------------------ */

function loadmaps() {
  
  multispectral = new OpenLayers.Map('tabs-3right');

  var dm_wms = load_wms();

  vlayer = new OpenLayers.Layer.Vector();
  multispectral.addLayer(dm_wms);
  multispectral.addLayer(vlayer);
  
  center = new OpenLayers.LonLat(-49.47,-16.40);
  
  
  multispectral.setCenter(new OpenLayers.LonLat(-49.47,-16.40).transform(
        new OpenLayers.Projection("EPSG:4326"),
        multispectral.getProjectionObject()
    ), 4);
  

  markers = new OpenLayers.Layer.Markers( "Markers" );


  multispectral.addLayer(markers);
  size = new OpenLayers.Size(21,25);
  offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
  icon = new OpenLayers.Icon('http://www.openlayers.org/dev/img/marker.png', size, offset);
  
}  
/* --------------------------------------------- END  MAPS ------------------------------------------------------ */

/* --------------------------------------------- BUSCAR DADOS E MONTAR TABELA ------------------------------------------------------ */
  closeloading();
});

var globaldata;
function loadData(plate) {

	jQuery.post(
    	"/rastreamento/loadData/",
        {plate:plate},
        
		function(data){

          globaldata = data;
          loadGrid();
          loadlateralgrid();
          closeloading();
        },'json'
	);
	
}

//var globaldata;
var olddata = null;



function loadGrid() {

          var data = globaldata;
          var colModel = [];
          colNames = [];
          var size = new OpenLayers.Size(16,16);
          var offset = new OpenLayers.Pixel(-(size.w/2), -size.h+8);
          var icon = new OpenLayers.Icon('/media/img/marker.png',size,offset);
          
          //Campos fixos
          if(colNames.pushNew("Latitude"))  
            colModel.pushNew({name:"Latitude",hidden:true});
          if(colNames.pushNew("Longitude"))
            colModel.pushNew({name:"Longitude",hidden:true});
          if(colNames.pushNew("Placa"))
            colModel.pushNew({name:"Placa",align:"center",formatter:currencyFmatter,width:75,sortable:true,key:true});
          if(colNames.pushNew("Tipo veículo"))
            colModel.pushNew({name:"Tipo veículo",align:"center",width:75,sortable:true});
          if(colNames.pushNew("Hora"))
            colModel.pushNew({name:"Hora",align:"center",sortable:true});
          if(colNames.pushNew("Cliente"))
            colModel.pushNew({name:"Cliente",align:"center",width:75,sortable:true});
          
          //para cada veículo
          var nequips = 0;
          
          jQuery.each(data, function(key, equip) {

            nequips++;
           //hack para colocar endereço em primeiro
           addr = equip.geocode["Endereço"];
           delete equip.geocode["Endereço"];

            if(colNames.pushNew("Endereço"))
                colModel.pushNew({name:"Endereço",align:"center",width:200});
    
            //para cada info de geocode
            jQuery.each(equip.geocode, function(key3,info){
                if (info != ""){
                    if(colNames.pushNew(key3))
                        colModel.pushNew({name:key3,align:"center",width:100});
                }
            });
            
            //fim do hack para botar endereço em primeiro
            equip.geocode["Endereço"] = addr;
    
            //para cada info do rastreador
            jQuery.each(equip.info, function(key2,info){
              if (!(key2 == "Latitude" || key2 == "Longitude")) {
                if(colNames.pushNew(key2))
                    colModel.pushNew({name:key2.replace(" ","_"),align:"center",width:75});
              }
            });
          });
                    
          h = jQuery(window).height();
          if (olddata == null) {
            jQuery("#list4").jqGrid({
              //uncomment the line below for the pager
              //pager: "#gridpager",
              sortable:false,
              datatype: "local",
              height:h-250,
              //width: 960,
              colNames: colNames, 
              colModel:colModel,
              multiselect: true, 
              loadui:"block",
              caption: "Selecione os veículos na tabela e clique no botão acima para visualizá-los no mapa:",
              autoheight:true,
              autowidth: true,
              shrinkToFit: false,
              loadComplete: function(data) {
              	
              	//inserir dados
          		insertDataJqgrid();
          		          		          		
				jQuery('#gridlink').click(function() {

					if(selected == 1) {

						jQuery("#list4").resetSelection();

						jQuery.each(jQuery("#list4").jqGrid('getRowData'), function(rowid, celldata) {
							plate = celldata["Placa"].replace(/(<([^>]+)>)/ig, "").replace(" ", "");
							if(markersToDisplay.hasOwnProperty(plate)) {
								// alert('plate:"'+plate+'",'+rowid);
								//alert(jQuery('#list4').getRowData(rowid));
								jQuery("#list4").setSelection(rowid);
							}
						});
					}
					selected = tab.tabs('option', 'selected');
				});


   		 	  },
              onSelectRow: function(rowid,status){ 
                //get the plate (dict key)                  
                plate = jQuery('#list4').jqGrid('getCell',rowid,'Placa').replace(/(<([^>]+)>)/ig,"").replace(" ","");                
                if (status == true) {
                 
                  lat = jQuery('#list4').jqGrid('getCell',rowid,'Latitude');
                  lng = jQuery('#list4').jqGrid('getCell',rowid,'Longitude');
                  pnt = new OpenLayers.LonLat(lng,lat).transform(new OpenLayers.Projection("EPSG:4326"),multispectral.getProjectionObject());
                  marker = new OpenLayers.Marker(pnt,icon.clone());
                  
                  if(!markersToDisplay.hasOwnProperty(plate)){
                    //alert('added: "'+plate+'"');
                    markersToDisplay[plate] = marker;
                  }
                  
				  showMarkersInMap();
                  
                  //Selects the row on the lateral grid
                  // if (jQuery("#list").getGridParam('selarrrow') != 1)
                  	// jQuery("#list").setSelection(rowid,'true');
                  
                  
                  
                  
                  //multimarkers[rowid] = marker;
                                    
                  //markers.addMarker(marker);
                  //multispectral.zoomToExtent(markers.getDataExtent(),1);
                }
                else if(markersToDisplay.hasOwnProperty(plate)){
                	
                    delete markersToDisplay[plate];
                    
                    showMarkersInMap();
                    //Unselects the row on the lateral grid
                  // if (jQuery("#list").getGridParam('selarrrow') != 0)
                  	// jQuery("#list").setSelection(rowid,'false');
                
                  //markers.removeMarker(multimarkers[rowid]);
                  //multispectral.zoomToExtent(markers.getDataExtent(),1);
                
              }
              
            }});
            
            // jQuery("#list4").jqGrid('navGrid','#gridpager',{edit:false,add:false,del:false});
            //jQuery("#list4").filterToolbar();
            // jQuery("input[id^=gs]").css("height","85%");
            // jQuery("input[id^=gs]").css("width","100%");
          
          }
          
          // jQuery("#load_list4").show();
          // jQuery("#lui_list4").show();
          
          
          
          //cria o objeto para cada linha
          
              

}

function doTimer() {
  setTimeout(function(){
    loadData();
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
        	
          if (key2 == 'license_plate') {
          	jQuery("#vehicledialog").append("<p><b>Placa:</b>  "+vehicledata+"</p>");
          }
          else if (key2 == 'type') {
          	jQuery("#vehicledialog").append("<p><b>Tipo:</b>  "+vehicledata+"</p>");
          }
          else if (key2 == 'sistema') {
          	jQuery("#vehicledialog").append("<p><b>Cliente:</b>  "+vehicledata+"</p>");
          }
          else {
          	jQuery("#vehicledialog").append("<p><b>"+key2+":</b>  "+vehicledata+"</p>");
          }
          jQuery("#vehicledialog").dialog({show: "blind",modal:true});
        });  
      }     
    });
  });
  
}

function showMarkersInMap(){
	
	//Remove all the current markers in the map
	markers.clearMarkers();
	
	$.each(markersToDisplay,function(key,data){
		markers.addMarker(data);
	})
	
	multispectral.updateSize();
	multispectral.zoomToExtent(markers.getDataExtent(),1);
	multispectral.updateSize();
	multispectral.zoomOut();
	multispectral.updateSize();
}

function insertDataJqgrid(){

	myData = [];
	object = new Object;

	if(olddata != null) {
		jQuery.each(olddata, function(key2, olditem) {
			jQuery("#list4").jqGrid('delRowData', olditem.id);

		});
	}
	nequips = 0;
	jQuery.each(globaldata, function(key, equip) {
		if(olddata != null) {

			//Deleta info antiga e repoe info nova
			/*
			 jQuery.each(olddata, function(key2,olditem) {
			 if (olditem.id == equip.id) {
			 jQuery("#list4").jqGrid('delRowData', olditem.id);
			 }
			 });
			 */
		}
		object = {};

		jQuery.each(colNames, function(keyx, name) {

			//Campos fixos
			if(name == "Hora")
				object[name] = equip.hora.eventdate;
			else if(name == "Tipo veículo")
				object[name] = equip.veiculo.type;
			else if(name == "Placa")
				object[name] = equip.veiculo.license_plate;
			else if(name == "Cliente")
				object[name] = equip.veiculo.sistema;
			//Geocode fields
			else if(name == "Endereço") {
				if(equip.geocode["Endereço"].constructor == String)
					object[name] = equip.geocode["Endereço"];
				else
					object[name] = Math.floor(equip.lat * 100000) / 100000 + "," + Math.floor(equip.lng * 100000) / 100000;
			} else if(name == "Cidade")
				object[name] = equip.geocode["Cidade"];
			else if(name == "CEP")
				object[name] = equip.geocode["CEP"];
			else if(name == "Estado")
				object[name] = equip.geocode["Estado"];
			else if(name == "Latitude")
				object[name] = equip["lat"];
			else if(name == "Longitude")
				object[name] = equip["lng"];

			//Custom fields
			else {
				object[name.replace(" ", "_")] = equip.info[name];
			}

		});
		nequips++;
		object['id'] = nequips;
		myData.push(clone(object));
	});

	var i = 0;
	jQuery.each(myData, function(key, item) {
		// Please don't mess this again
		jQuery("#list4").jqGrid('addRowData', i, myData[i]);
		i = i + 1;
	});

	olddata = globaldata;
}

