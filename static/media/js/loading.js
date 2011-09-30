function openloading() {
   $("#loadingScreen").dialog({
    		dialogClass: "loadingScreenWindow",
    		closeOnEscape: false,
    		draggable: false,
    		width: 460,
    		minHeight: 50,
    		modal: true,
    		buttons: {},
    		resizable: false,
    		open: function() {
    			// scrollbar fix for IE
    			$('body').css('overflow','hidden');
    		},
    		close: function() {
    			// reset overflow
    			$('body').css('overflow','auto');
    		}
    });
}

function closeloading(time){
  
  if (typeof time == "undefined") {
      $("#loadingScreen").dialog("close");
  }
  
  else {
    setTimeout(function(){ $("#loadingScreen").dialog("close"); }, time);
  }
}
