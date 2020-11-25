// drop down menu
var dropdownTitle = document.getElementById("dropdownMenu2");
var dropdownOptions = document.getElementsByClassName("dropdown-item-platform")


// pagesize list
var pagesizeTitle = document.getElementById("dropdownMenu3");
var pagesizeOptions = document.getElementsByClassName("dropdown-item-pagesize")

var pageNumOptions = document.getElementsByClassName("ant-pagination-item")
var previousButton = document.getElementById("PreBtn");
var NextButton = document.getElementById("NextBtn");
var pageJumper = document.getElementById("page_jumper");



function urlBtnsClick(){
	var urlBtns = document.getElementsByClassName("showLink")
	for(var i=0; i<urlBtns.length;i++){
		urlBtns[i].onclick = function(){
			var newElement = document.createElement("div")
			newElement.className = "alert alert-info"
			newElement.setAttribute("role","alert")
			newElement.innerText = this.getAttribute("url-value")
			this.parentElement.appendChild(newElement)
		}
	}
} 


dropdownTitle.onclick = function(){
    for(var i=0; i<dropdownOptions.length;i++){
        dropdownOptions[i].onclick = function(){
            dropdownTitle.value = this.value;
            dropdownTitle.textContent = this.textContent;
        }
    }
};

pagesizeTitle.onclick = function(){
	for(var i=0; i<pagesizeOptions.length; i++){
        pagesizeOptions[i].onclick = function(){
            pagesizeTitle.value = this.value;
			pagesizeTitle.textContent = this.textContent;
			var program_id = document.getElementById("dropdownMenu2").getAttribute("value");
			var product_key = document.getElementById("inputPassword2").value;
			var pageSize = document.getElementById("dropdownMenu3").value;
			
			url_path = "http://106.12.160.222:8002/baoxian/?searchType=1"+ "&program_id="+program_id+"&product_key="+product_key+"&page=1&pageSize="+pageSize;
			window.location.href = url_path;
        }
    }
};

function searchBtnClickEvent(){
    var program_id = document.getElementById("dropdownMenu2").getAttribute("value");
	var product_key = document.getElementById("inputPassword2").value;
	var pageSize = document.getElementById("dropdownMenu3").value;
	var current_page = document.getElementsByClassName("ant-pagination-item-active")[0].textContent;
    url_path = "http://106.12.160.222:8002/baoxian/?searchType=1"+ "&program_id="+program_id+"&product_key="+product_key+"&page=1"+"&pageSize="+pageSize;
    window.location.href = url_path;
};

function switchPage(){
	var previousButton = document.getElementById("PreBtn");
    var NextButton = document.getElementById("NextBtn");
	var current_page = document.getElementsByClassName("ant-pagination-item-active")[0].value;
	var totol_num = document.getElementById("total-page").value;
	var pageSize = document.getElementById("dropdownMenu3").value;
	
	if(current_page == "1"){
		previousButton.classList.add("ant-pagination-disabled");
	}else{
		previousButton.classList.remove("ant-pagination-disabled");
	}
	if((parseInt(totol_num)-parseInt(current_page)*parseInt(pageSize)) > 0){
		NextButton.classList.remove("ant-pagination-disabled");
	}else{
		NextButton.classList.add("ant-pagination-disabled");
	}
};

function initPageBtn(){
	var pageNumOptions = document.getElementsByClassName("ant-pagination-item");	
	for(var i=0;i<pageNumOptions.length;i++){		
        pageNumOptions[i].onclick = function(){
            var program_id = document.getElementById("dropdownMenu2").getAttribute("value");
			var product_key = document.getElementById("inputPassword2").value;
			var pageNo = this.value
			var pageSize = document.getElementById("dropdownMenu3").value;
			url_path = "http://106.12.160.222:8002/baoxian/?searchType=1"+ "&program_id="+program_id+"&product_key="+product_key+"&page="+pageNo+"&pageSize="+pageSize;
			window.location.href = url_path;
        }
    }
};

previousButton.onclick = function(){
	var current_page = document.getElementsByClassName("ant-pagination-item-active")[0].value;
	if(!(current_page == "1")){
		var program_id = document.getElementById("dropdownMenu2").getAttribute("value");
		var product_key = document.getElementById("inputPassword2").value;
		var pageNo = parseInt(current_page)-1;
		var pageSize = document.getElementById("dropdownMenu3").value;
		url_path = "http://106.12.160.222:8002/baoxian/?searchType=1"+ "&program_id="+program_id+"&product_key="+product_key+"&page="+pageNo+"&pageSize="+pageSize;
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
		var pageSize = document.getElementById("dropdownMenu3").value;
		url_path = "http://106.12.160.222:8002/baoxian/?searchType=1"+ "&program_id="+program_id+"&product_key="+product_key+"&page="+pageNo+"&pageSize="+pageSize;
		window.location.href = url_path;
	}
};

pageJumper.onblur = function(){
	if(pageJumper.value){
		var totol_num = document.getElementById("total-page").value // 151
		var current_page = document.getElementsByClassName("ant-pagination-item-active")[0].textContent; // 20
		var pageSize = document.getElementById("dropdownMenu3").value;
		if(parseInt(pageJumper.value) <= 0){
			pageJumper.value = 1;
		}else if(!(Math.floor(pageJumper.value) === pageJumper.value)){
			pageJumper.value = parseInt(pageJumper.value);
		}
		if(parseInt(totol_num)%parseInt(pageSize)==0){
			if(parseInt(pageJumper.value) > parseInt(totol_num)/parseInt(pageSize)){
				pageJumper.value = parseInt(parseInt(totol_num)/parseInt(pageSize));
			}
		}else{
			if(parseInt(pageJumper.value) > (parseInt(totol_num)/parseInt(pageSize))){
				console.log("pageJumper>totol_num");
				pageJumper.value = parseInt(parseInt(totol_num)/parseInt(pageSize)+1);
			}
		}
		if(!(parseInt(pageJumper.value)==parseInt(current_page))){
			var program_id = document.getElementById("dropdownMenu2").getAttribute("value");
			var product_key = document.getElementById("inputPassword2").value;
			var pageNo = pageJumper.value;
			url_path = "http://106.12.160.222:8002/baoxian/?searchType=1"+ "&program_id="+program_id+"&product_key="+product_key+"&page="+pageNo+"&pageSize="+pageSize;
			window.location.href = url_path;
		}
	}
};

window.onload = function(){
	switchPage();
	initPageBtn();
	urlBtnsClick();
};