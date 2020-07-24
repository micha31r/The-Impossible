var process_id;
var timer = 60;

function start_timer() {
	process_id = setInterval(
		function() {
			timer -= 1;
			document.getElementById("resend-link-text").innerHTML = `Resend in ${timer}s`;
			if (timer <= 0) { 
				window.location.href = resend_link;
				timer = 60;
				clearTimeout(process_id);
			}
		}, 
		1000
	);
}