function resize() {
	// Idea setting
	if ($(window).width() < 830) {
		$("#idea-setting").appendTo("#append-target1");
	} else {
		$("#idea-setting").appendTo("#append-origin1");
	}

	// Exsisting tag
	if ($(window).width() < 460) {
		$("#exsisting-tag").appendTo("#append-target2");
	} else {
		$("#exsisting-tag").appendTo("#append-origin2");
	}
}

window.onload = function() {
	resize();
	window.addEventListener(
		"resize", 
		resize
	);
}