if (document.readyState == 'loading') {
    document.addEventListener("DOMContentLoaded", ready)
} else {
    ready()
}

function ready() {
    cart = sessionStorage.getItem("cart")
    cart = JSON.parse(cart)
    var total = 0
    for (let i = 0; i < cart.length; i++) {
        var cart_item = cart[i];
        total += parseInt(cart_item.qty) * parseInt(cart_item.price)
        addItemToCart(cart_item.title, cart_item.price, cart_item.qty)

    }
    document.getElementsByClassName("order-total")[0].innerText = total + " ብር"
}

function addItemToCart(title, price, qty) {
    var Row = document.createElement('div')
    Row.classList.add("order-col")
    var Item = document.getElementsByClassName('order-products')[0]
    var RowContents = `
    <div>
    <h4> ${title}</h4></div>
    <div>${parseInt(qty) * parseInt(price)} </div>

    `
    Row.innerHTML = RowContents
    Item.append(Row)
}