const selecter= document.getElementById('sort')
function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
    }
    return "";
}
if (selecter){
    if (getCookie('sort')=="asc"){
        selecter.selectedIndex = 0;
    }
    else{
        selecter.selectedIndex = 1;
    }
    selecter.addEventListener('change', function() {
    var selectedValue = this.value
    document.cookie = `sort=${selectedValue}`;
    location.reload()


})
}