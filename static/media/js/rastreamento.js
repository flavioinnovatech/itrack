function montartabela(h,w) {
  
  /* -------------------------------------------- JQGRID READY -------------------------------------------- */ 

  
  
  if (h == null && w == null) {

  w = $(window).width();
  h = $(window).height();
  
  	
  }  
  
}

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
$("#googlemap").click(function() {  
	var geocoder;
	var map;
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
	
  
  if ($("#jqg_list4_1").is(':checked')) {
    
  var lat = $("td[aria-describedby=list4_Latitude]").text();
  var lng = $("td[aria-describedby=list4_Longitude]").text();
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
				infowindow.open(map);
			} else {
				alert("No results found");
			}
		} else {
			alert("Geocoder failed due to: " + status);
		}
	});
  }
  map = new google.maps.Map(document.getElementById("tabs-3"), myOptions);
	
  $("#tabs-3").css("height","100%");
  
});

  $.getJSON("/rastreamento/loadCustomFields",
    function(customFields){
      
      $.getJSON("/rastreamento/loadData",
        function(data){
           // $.each(data, function(key1, val1) {alert(val1.type);    });
          var colModel = [];
          var colNames = [];
          myData = data;
          
          $.each(data, function(key1, val1) {
              
                colNames.push(val1.type);
                
                colModel.push({name:val1.type});
               
          });
            
            jQuery("#list4").jqGrid({   
             	datatype: "local",
             	height:h-250,
             	width: 930,
             	colNames: colNames, 
             	colModel:colModel,
             	multiselect: true, 
             	caption: "Rastreamento veicular" }); 

              var i = 0
              var myData = [];
              var arraytype = [];
              var arrayvalue = [];
              $.each(data, function(key1, val1) {
                arraytype.push(val1.type);
                arrayvalue.push(val1.value);
              });
              
              myData = [ { "Entrada Negativa 2":arrayvalue[0],"Botão de Pânico":arrayvalue[1],"Ignição (PPC)":arrayvalue[2],"Velocidade Tacógrafo":arrayvalue[3],"RPM":arrayvalue[4],"Longitude":arrayvalue[5],"Latitude":arrayvalue[6],"Velocidade GPS":arrayvalue[7] } ];

              jQuery("#list4").jqGrid('addRowData',1,myData[0]);
              
              //HACK
              $("table#list4").css("width","930px")
              
    });
  });

  

});



function mapa_multi() {
	callMultispectral(-22.896359,-47.060092);
	//jQuery("#dialog").dialog({height: $(window).height()},{ width : ($(window).width() - 25)},{ closeText: 'X' }); 
	//jQuery(".ui-icon").css("background-image", "none");
	//jQuery(".ui-icon").css("text-indent", "0");
	
}
