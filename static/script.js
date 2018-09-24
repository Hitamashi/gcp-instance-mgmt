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

	function startServer(){
		var ele = document.getElementById("start-server");
		oReq = new XMLHttpRequest();
	    oReq.onload = startServerHandle;
		oReq.open('GET', "/startTS", true);
	    oReq.send();
	    ele.removeEventListener("click", startServer);
	    ele.innerHTML = "Loading..."
	    ele.classList.add("loading");
	}

	function startServerHandle(){
		var ele = document.getElementById("start-server");
		var end = new Date().getTime() + 30*1000;

		if (oReq.status === 200) {
			setInterval(function(){ 
				var countDown = end - new Date().getTime();
				ele.innerHTML = "Server starting in " + Math.floor(countDown/1000);

				if (countDown < 0){
					location.reload();
				}
			}, 1000);
		} else {
			ele.addEventListener("click", startServer);
			alert('There was a problem with the server');
		}
	}

	document.addEventListener("DOMContentLoaded", function() {
		//Set time
		var now = getCurrentTime();

		document.getElementById("date-now").innerHTML = now.date;
		document.getElementById("month-now").innerHTML = now.month;
		document.getElementById("year-now").innerHTML = now.year;
		document.getElementById("time-now").innerHTML = "Last updated on " + now.full;

		//Set button start server action
		var button = document.getElementById('start-server');
		if(button !== null)
			button.addEventListener("click", startServer);
	});
})();