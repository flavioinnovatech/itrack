$(document).ready(function(){

  $('input[type="submit"]').mousedown(function(){
    $(this).css("border-style","inset");
  }).mouseup(function(){
    $(this).css("border-style","solid");
  }).mouseleave(function(){
    $(this).css("border-style","solid");
  });
  
  $("ul#nav > li").hover(
  	function() { $('ul', this).slideDown('fast', function(){}); },
  	function() { $('ul', this).css('display', 'none'); 	
  });
  
});
