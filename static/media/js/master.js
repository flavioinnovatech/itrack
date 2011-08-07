jQuery(document).ready(function(){

  jQuery('input[type="submit"]').mousedown(function(){
    $(this).css("border-style","inset");
  }).mouseup(function(){
    $(this).css("border-style","solid");
  }).mouseleave(function(){
    $(this).css("border-style","solid");
  });
  
  jQuery("ul#nav > li").hover(
  	function(){  //hover in
        $('ul', this).slideDown('fast', function(){});
        $('ul', this).css('display','block');
  	},
  	function(){ //hover out
  	    $("ul#nav > li ul").fadeOut(0);
  	    $("ul#nav > li ul").css('display', 'none'); 	
    });
  
});

