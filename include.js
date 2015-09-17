
$( document ).ready(function() {
	$( ".include" ).each(function() {
	  $(this).load( "include/" + $(this).html() + ".html" );
	  
	});
});