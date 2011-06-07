function montartabela(h,w) {
  
  /* -------------------------------------------- JQGRID READY -------------------------------------------- */ 

  var mydata = [ {id:"1",invdate:"2007-10-01",name:"test",note:"note",amount:"200.00",tax:"10.00",total:"210.00"} ];

  for(var i=2;i<=50;i++) {
  	mydata[i] = [ {id:i,invdate:"2007-10-01",name:"test",note:"note",amount:"200.00",tax:"10.00",total:"210.00"} ];
  }
  
  if (h == null && w == null) {

  w = $(window).width();
  h = $(window).height();
  
  jQuery("#list4").jqGrid({ 

  	datatype: "local",
  	height:h-250,
  	width: 930,
  	colNames:[
  	'Veículo',
  	'Modelo'
  	], 
  	colModel:[ 
  	{name:'id',index:'id', sorttype:"int"}, 
  	{name:'invdate',index:'invdate', sorttype:"date"}
  	], 
  	multiselect: true, 
  	caption: "Rastreamento veicular" }); 

  	for(var i=0;i<=mydata.length;i++) {
  		jQuery("#list4").jqGrid('addRowData',i+1,mydata[i]); 
  	}
  	
  }  
  
}
/* --------------------------------------------- FIM JQGRID READY --------------------------------------------- */

$('#tabs-1').ready(function(){  
  montartabela();
});

jQuery(document).ready(function(){  
  w = $(window).width();
  h = $(window).height();
  $( "#tabs" ).tabs();
  $( "#tabs" ).css("top","130px");
  
  tabw = ($("#tabs-1").width());
  tabh = ($("#tabs-1").height());
  
  document.body.style.overflow = "hidden";
  
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
        $('#tabs').css("width","100%");
        $('#tabs').css("height","100%");
        $('#tabs').css("top","0");
        $('#tabs').css("left","0");
        $("#tabs-3").css("height","100%");
        $("#tabs-3").css("width","97%");
        normal = 0;
        
        //resize do jqgrid
        $("#list4").setGridWidth(w - 50);
        $("#list4").setGridHeight(h - 150);
        
        break;
        
     case 0:
      $('#menuContainer').css("z-index","2");
      $('#tabs').css("width","960px");
      $('#tabs').css("height",height);
      $('#tabs').css("top","130px" );
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

/* --------------------------------------------- GOOGLE MAPS ------------------------------------------------------ */
// function codeLatLng() {  
	var geocoder;
	var map;
	var infowindow = new google.maps.InfoWindow();
	var marker;
	geocoder = new google.maps.Geocoder();
	var latlng = new google.maps.LatLng(-14.239424,-53.186502);
	var myOptions = {
		zoom: 4,
		center: latlng,
		mapTypeId: 'roadmap'
	}
	
	map = new google.maps.Map(document.getElementById("tabs-3"), myOptions);
  
	var input = "-22.896359,-47.060092";
	var latlngStr = input.split(",",2); 
	var lat = parseFloat(latlngStr[0]);
	var lng = parseFloat(latlngStr[1]);
	var latlng = new google.maps.LatLng(lat, lng);
	geocoder.geocode({'latLng': latlng}, function(results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			if (results[1]) {
				map.setZoom(16);
				marker = new google.maps.Marker({
					position: latlng, 
					map: map
				});
				infowindow.setContent(results[1].formatted_address);
				infowindow.open(map, marker);
			} else {
				alert("No results found");
			}
		} else {
			alert("Geocoder failed due to: " + status);
		}
	});
  
  $("#tabs-3").css("height","100%");
  
// }

});

function mapa_multi() {
	callMultispectral(-22.896359,-47.060092);
	//jQuery("#dialog").dialog({height: $(window).height()},{ width : ($(window).width() - 25)},{ closeText: 'X' }); 
	//jQuery(".ui-icon").css("background-image", "none");
	//jQuery(".ui-icon").css("text-indent", "0");
	
}
