/**
 * magaObtain.js
 */
$(document).ready(function(){
	$('#fetchFromSite').on('click',function(e) {
		$(e.target).html("取得中...");
		$(e.target).attr('disabled','disabled');
		$("a[name='article-ancher']").attr('disabled','disabled');

		location.href=$(e.target).data('url');
	})
});