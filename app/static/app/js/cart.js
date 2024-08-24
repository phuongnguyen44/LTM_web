var updateBtns = document.getElementsByClassName('update-cart')
// Alert
const alertPlaceholder = document.getElementById('liveAlertPlaceholder')
const divContainer=document.getElementById('ctn')
var cnt=0
var option
const appendAlert = (message, type) => {
  const wrapper = document.createElement('div')
  wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible" role="alert">`,
    `   <div>${message}</div>`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    '</div>'
  ].join('')
  alertPlaceholder.append(wrapper)
  console.log(alertPlaceholder)
}

if (updateBtns.length !=0) {
    for(i=0;i<updateBtns.length;i++){
        updateBtns[i].addEventListener('click',function(){
            var productId = this.dataset.product
            var action = this.dataset.action
            if (user === "AnonymousUser"){
                console.log('user not logged in')
            }
            else{
                if(alertPlaceholder){
                    option=1
                    if(cnt ==0){
                    appendAlert('Them vao gio hang thanh cong','success')
                    }
                    cnt=1
                    updateUserOrder(productId,action)
                    alertPlaceholder.style.display='block'
                    setTimeout(() =>{
                        alertPlaceholder.style.display='none'
                    },3000) 
                }
                else{
                    option=2
                    updateUserOrder(productId,action)
                    
                }
               
               
            }

        })
    }
}
const appendcart = (message) => {
  const wrapper2 = document.createElement('p')
  wrapper2.id='cart-total'
  wrapper2.innerHTML = message
  divContainer.appendChild(wrapper2)
}

function updateUserOrder(productId,action){
    console.log('user logged in')
    var url ='/update_item/'
    fetch(url,{
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken  

        },
        body: JSON.stringify({'productId':productId,'action':action})
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        var cart = document.getElementById('cart-total')
        if(divContainer){
            if(cart){
                divContainer.removeChild(cart)
                appendcart(data)
            }
        }
        if(option==2){
            location.reload()
        }
    })
   
}