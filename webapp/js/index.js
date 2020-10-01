function clickPreviousBtn(){
    console.log("1111")
    let pageNo = document.getElementById("pageNo").textContent
    let currentPage = pageNo + 1
    document.getElementById("pageNo").innerText(currentPage)
    console.log("2222")
}

document.getElementById("PreviousBtn").onclick = clickPreviousBtn