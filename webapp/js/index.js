console.log("1111")

// drop down menu
var dropdownTitle = document.getElementById("dropdownMenu2");
var dropdownOptions = document.getElementsByClassName("dropdown-item")

// page foot
var previousBtn = document.getElementById("PreviousBtn");
var pageNo = document.getElementById("pageNo");
var NextBtn = document.getElementById("NextBtn");

dropdownTitle.onclick = function(){
    for(var i=0; i<dropdownOptions.length;i++){
        dropdownOptions[i].onclick = function(){
            console.log(this.value, this.textContent)
            dropdownTitle.value = this.value;
            dropdownTitle.textContent = this.textContent;
        }
    }
}

function searchBtnClickEvent(){
    //document.getElementById("pageNo").textContent = 1
    var program_id = document.getElementById("dropdownMenu2").getAttribute("value");
    var product_key = document.getElementById("inputPassword2").value;
    var pageNo = document.getElementById("pageNo").textContent;
    console.log(22222)
    console.log(program_id, product_key, pageNo)
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

previousBtn.onclick = function(){
    currentPage = document.getElementById("pageNo").textContent;
    if(parseInt(currentPage)>1){
        document.getElementById("pageNo").textContent = parseInt(currentPage) - 1;
        var program_id = document.getElementById("dropdownMenu2").getAttribute("value");
        var product_key = document.getElementById("inputPassword2").value;
        var pageNo = document.getElementById("pageNo").textContent;
        url_path = "http://106.12.160.222:8002/test/?searchType=1"+ "&program_id="+program_id+"&product_key="+product_key+"&page="+pageNo;
        window.location.href = url_path;
    }
    
    // }eles{
    //     previousBtn.setAttribute("disabled", true)
    // }
    
}
