jQuery(document).ready(function() {
	
	$('#content').css("width","98%");

	
	h = jQuery(window).height();
	tw =jQuery("table#list4").width();
	
	jQuery('img.fullscreen').click(function() {

		//It was not fullscreen
		//It is fullscreen now
		if ($(this).hasClass('unselected')) {
			
			$("#content").css("height",h-200);
			$("#content").addClass('fullscreen');
			$("#tabs").addClass('fullscreen');
			$("#tabs").removeClass('normal');
			$("#list4").setGridWidth(w - 50);
			$("#list4").setGridHeight(h - 250);
			$(".ui-jqgrid-htable").width("101.5%");
			$("#list4").width("100%");
									
			$(this).removeClass('unselected');
		}
		
		else {
			$("#content").css("height","100%");
			$("#content").removeClass('fullscreen');
			$("#tabs").removeClass('fullscreen');
			$("#tabs").addClass('normal');
			$("#list4").setGridWidth("931px");
			$("#list4").setGridHeight(h - 250);
			$(".ui-jqgrid-htable").width("931px");
			$("#list4").width("931px");
			$("#list4").css("margin","0");
			
			$(this).addClass('unselected');
		}

		return false;

		
	});
});
