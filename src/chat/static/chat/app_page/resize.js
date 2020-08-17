function resize_app() {
	var window_width = $(window).width();
	var sibling_width = 0;
	if ($("#show-chat-group-list").css("display") != "block") {
		sibling_width = $(".chat-group-list").outerWidth();
	}
	$(".app-container").width(window_width - sibling_width);
	$(".chat-message-input-container").width(window_width - sibling_width);
}

function resize_chat_log() {
	var sibling_height = $(".chat-message-input-container").outerHeight();
	var parent_height = $(".app-container").height();
	$("#chat-log-container").outerHeight(parent_height - sibling_height);
}

window.addEventListener(
	"resize", 
	function() {
		resize_app();
		resize_chat_log();
	}
);

resize_app();
resize_chat_log();