// drop down menu
var dropdownTitle = document.getElementById("dropdownMenu2");
var dropdownOptions = document.getElementsByClassName("dropdown-item")


// page foot
var previousBtn = document.getElementById("PreviousBtn");
var pageNo = document.getElementById("pageNo");
var NextBtn = document.getElementById("NextBtn");

var pageNumOptions = document.getElementsByClassName("ant-pagination-item")

dropdownTitle.onclick = function(){
    for(var i=0; i<dropdownOptions.length;i++){
        dropdownOptions[i].onclick = function(){
            dropdownTitle.value = this.value;
            dropdownTitle.textContent = this.textContent;
        }
    }
}

function searchBtnClickEvent(){
    //document.getElementById("pageNo").textContent = 1
    var program_id = document.getElementById("dropdownMenu2").getAttribute("value");
    var product_key = document.getElementById("inputPassword2").value;
    url_path = "http://106.12.160.222:8002/test/?searchType=1"+ "&program_id="+program_id+"&product_key="+product_key+"&page=1";
    window.location.href = url_path;
}

NextBtn.onclick = function(){
    currentPage = document.getElementById("pageNo").textContent;
    document.getElementById("pageNo").textContent = parseInt(currentPage) + 1;
    var program_id = document.getElementById("dropdownMenu2").getAttribute("value");
    var product_key = document.getElementById("inputPassword2").value;
    var pageNo = document.getElementById("pageNo").textContent;
    url_path = "http://106.12.160.222:8002/test/?searchType=1"+ "&program_id="+program_id+"&product_key="+product_key+"&page="+pageNo;
    window.location.href = url_path;
}


var pageNumOptions = document.getElementsByClassName("ant-pagination-item");
var previousButton = document.getElementById("PreBtn");
var NextButton = document.getElementById("NextBtn");
var pageJumper = document.getElementById("page_jumper");

function switchPage(){
	var current_page = document.getElementsByClassName("ant-pagination-item-active")[0].textContent;
	var totol_num = document.getElementById("total-page").value;
	if(current_page == "1"){
		previousButton.classList.add("ant-pagination-disabled");
	}else{
		previousButton.classList.remove("ant-pagination-disabled");
	}
	if(parseInt(totol_num)-parseInt(current_page)*5 > 0){
		NextButton.classList.remove("ant-pagination-disabled");
	}else{
		NextButton.classList.add("ant-pagination-disabled");
	}
    for(var i=0;i<pageNumOptions.length;i++){		
        pageNumOptions[i].onclick = function(){		
      		//var program_id = document.getElementById("dropdownMenu2").getAttribute("value");
    		// var product_key = document.getElementById("inputPassword2").value;
            var program_id = document.getElementById("dropdownMenu2").getAttribute("value");
			var product_key = document.getElementById("inputPassword2").value;
			var pageNo = this.value
			url_path = "http://106.12.160.222:8002/test/?searchType=1"+ "&program_id="+program_id+"&product_key="+product_key+"&page="+pageNo;
			window.location.href = url_path;
        }
    };
};

previousButton.onclick = function(){
	var current_page = document.getElementsByClassName("ant-pagination-item-active")[0].textContent;
	if(!(current_page == "1")){
		var program_id = document.getElementById("dropdownMenu2").getAttribute("value");
		var product_key = document.getElementById("inputPassword2").value;
		var pageNo = parseInt(current_page)-1;
		url_path = "http://106.12.160.222:8002/test/?searchType=1"+ "&program_id="+program_id+"&product_key="+product_key+"&page="+pageNo;
		window.location.href = url_path;
	}
	
};

NextButton.onclick = function(){
	var totol_num = document.getElementById("total-page").value
	var current_page = document.getElementsByClassName("ant-pagination-item-active")[0].textContent;
	if(parseInt(totol_num)-parseInt(current_page)*5 > 0){
		var program_id = document.getElementById("dropdownMenu2").getAttribute("value");
		var product_key = document.getElementById("inputPassword2").value;
		var pageNo = parseInt(current_page)+1;
		url_path = "http://106.12.160.222:8002/test/?searchType=1"+ "&program_id="+program_id+"&product_key="+product_key+"&page="+pageNo;
		window.location.href = url_path;
	}
};

pageJumper.onblur = function(){
	console.log("pageJumper lose focus");
	var totol_num = document.getElementById("total-page").value // 151
	var current_page = document.getElementsByClassName("ant-pagination-item-active")[0].textContent; // 20
	if(parseInt(pageJumper.value) <= 0){
		pageJumper.value = 1;
	}else if(!(Math.floor(pageJumper.value) === pageJumper.value)){
		pageJumper.value = parseInt(pageJumper.value);
	}
	if(parseInt(totol_num)%5==0){
		if(parseInt(pageJumper.value) > parseInt(totol_num)/5){
			pageJumper.value = parseInt(parseInt(totol_num)/5);
		}
	}else{
		// 1
		//           21                         151/5 = 30.2
		if(parseInt(pageJumper.value) > (parseInt(totol_num)/5)){
			console.log("pageJumper>totol_num");
			pageJumper.value = parseInt(parseInt(totol_num)/5+1);
		}
	}
	if(!(parseInt(pageJumper.value)==parseInt(current_page))){
		var program_id = document.getElementById("dropdownMenu2").getAttribute("value");
		var product_key = document.getElementById("inputPassword2").value;
		var pageNo = pageJumper.value;
		url_path = "http://106.12.160.222:8002/test/?searchType=1"+ "&program_id="+program_id+"&product_key="+product_key+"&page="+pageNo;
		window.location.href = url_path;
	}
}

window.onload = function(){
    switchPage();
};