

function statusChange() {
   	bars = document.getElementsByClassName('statusBar');
   	statusText = document.getElementsByClassName('status');
	gigsText = document.getElementsByClassName('gigs');
   	PMI = document.forms["inspection"]["PMI"].value;
	gigs = $('.gig:checkbox:checked').length;
	auto = $('.auto:checkbox:checked').length;
    if ((gigs >= {{amiMaxGigs}} && PMI.includes("No")) || ((gigs >= {{pmiMaxGigs}} && PMI.includes("Yes")) || auto > 0) {
        for (var i = 0; i < bars.length; i++)  {
            bars[i].style.backgroundColor="red";
			gigsText[i].textContent=gigs;
            statusText[i].textContent="Failing";
        }
		document.getElementById("finalStatus").value = "Fail";
		document.getElementById("gigNumber").value = gigs;
    }else{
        for (var i = 0; i < bars.length; i++)  {
			gigsText[i].textContent=gigs;
			document.getElementById("gigNumber").value = gigs;
            if (PMI.includes("Yes")) {
                bars[i].style.backgroundColor="lightblue";
                statusText[i].textContent="PMI";
				document.getElementById("finalStatus").value = "PMI";
            }else{
                bars[i].style.backgroundColor="lightgreen";
                statusText[i].textContent="Passing";
				document.getElementById("finalStatus").value = "Pass";
            }          
        }
    }
}

function changePMI() {
    PMI = document.forms["inspection"]["PMI"].value;
    if (PMI.includes("Yes")) {
        document.getElementById('PMIdesc').style.color="black";
        document.getElementById('AMIdesc').style.color="#b4b4b4";
        statusChange();
    }else{
        document.getElementById('PMIdesc').style.color="#b4b4b4";
        document.getElementById('AMIdesc').style.color="black";
        statusChange();
    }    
}
function descChange() {
    option = document.forms["inspection"]["desc"];
    objects = document.getElementsByClassName('descObject');
    if (option.checked == true) {
        for (var i = 0; i < objects.length; i++)  {
            objects[i].style.display='none';
        }
    }else{
        for (var i = 0; i < objects.length; i++)  {
            objects[i].style.display='inline';
        }
    }    
}
changePMI()
