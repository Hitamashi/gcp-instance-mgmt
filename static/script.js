(function() {
	var oReq;

	function getCurrentTime(){
		var today = new Date();
		var dd = today.getDate();
		var mm = today.getMonth()+1; //January is 0!

		var yyyy = today.getFullYear();
		if(dd<10){
		    dd='0'+dd;
		}
		if(mm<10){
		    mm='0'+mm;
		}

		var now = {
			'date': dd,
			'month': mm,
			'year': yyyy,
			'time': today.toLocaleTimeString(),
			'full': dd + "-" + mm + "-" + yyyy + " " + today.toLocaleTimeString()
		};
		return now;
	}

	function startServer(event){
		var ele = event.currentTarget;
		console.log(ele)
		zone = this.getAttribute("data-zone")
		vm = this.getAttribute("data-vm")
		oReq = new XMLHttpRequest();
		oReq.open('GET', "/startTS?zone="+ zone +"&vm=" + vm, true);
		oReq.onload = function(){
			var end = new Date().getTime() + 30*1000;

			if (oReq.status === 200) {
				myInterval = setInterval(function(){
					var countDown = end - new Date().getTime();

					if (countDown <= 0){
						clearInterval(myInterval);
						location.reload();
					}

					ele.innerHTML = "Server starting in " + Math.floor(countDown/1000);
				}, 1000);
			} else {
				ele.addEventListener("click", startServer, {once: true});
				alert('There was a problem with the server');
			}
		}
		oReq.send();
	    ele.innerHTML = "Loading..."
	    ele.classList.add("loading");
	}

	document.addEventListener("DOMContentLoaded", function() {
		//Set time
		var now = getCurrentTime();

		document.getElementById("date-now").innerHTML = now.date;
		document.getElementById("month-now").innerHTML = now.month;
		document.getElementById("year-now").innerHTML = now.year;
		document.getElementById("time-now").innerHTML = "Last updated on " + now.full;

		//Set button start server action
		var buttons = document.getElementsByClassName('start-server');

		Array.from(buttons).forEach(function(element) {
			element.addEventListener('click', startServer, {once: true});
		});
	});
})();