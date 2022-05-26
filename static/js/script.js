if (document.readyState == 'loading') {
    document.addEventListener("DOMContentLoaded", ready)
} else {
    ready()
}

function ready() {
    cart = sessionStorage.getItem("cart")
    cart = JSON.parse(cart)
        // purcahse = document.getElementsByClassName()
    for (let i = 0; i < cart.length; i++) {
        var cart_item = cart[i];
        addItemToCart(cart_item.title, cart_item.price, cart_item.image, cart_item.qty, cart_item.package, cart_item.count);
        updateTotal()
    }

}

function addItemToCart(title, price, img, qty, package, count) {
    var cartRow = document.createElement('tr')
    cartRow.classList.add('cart-row')
    var cartItems = document.getElementsByClassName('orders')[0]
    if (package == "true") {
        var cartRowContents = `
        <td>
        <div class="product-widget">
            <div class="product-img"><img src="${img}" alt="metsahft" height="70">
            </div>
            <div class="product-body">
                <h3 class="product-name"><a href="#">${title}</a></h3>
            </div>
        </div>
    </td>
    <td>
        <div>
            <h5 class="price">${price} ብር</h5>
        </div>
    </td>
    
    <td>
        <div>
            <input type="number" class="qty"  value="1" style=" width: 40px" disabled>
        </div>
    </td>
    <td>
        <h5 class="total-price" style="float:right; ">55</h5>
    </td>
    <td>
        <a href="">
            <h4><span class="remove"><i class="fa fa-trash " aria-hidden="true "></i></span></h4>
        </a>
    </td>`

    } else {
        var cartRowContents = `
    <td>
    <div class="product-widget">
        <div class="product-img"><img src="${img}" alt="metsahft" height="70">
        </div>
        <div class="product-body">
            <h3 class="product-name"><a href="#">${title}</a></h3>
        </div>
    </div>
</td>
<td>
    <div>
        <h5 class="price">${price} ብር</h5>
    </div>
</td>

<td>
    <div>
        <input type="number" class="qty"  step="1" value="${qty}" style=" width: 40px " max="${count}">
    </div>
</td>
<td>
    <h5 class="total-price" style="float:right; ">55</h5>
</td>
<td>
    <a href="">
        <h4><span class="remove"><i class="fa fa-trash " aria-hidden="true "></i></span></h4>
    </a>
</td>`
    }
    cartRow.innerHTML = cartRowContents;
    cartItems.append(cartRow);
    qty = cartRow.getElementsByClassName("qty")[0].value;
    cartRow.getElementsByClassName('remove')[0].addEventListener('click', removeCartItem);
    cartRow.getElementsByClassName('qty')[0].addEventListener('change', quantityChanged);
}

function removeCartItem(event) {
    var buttonClicked = event.target.parentElement
    console.log(buttonClicked.parentElement)
    elt = buttonClicked.parentElement.parentElement.parentElement.parentElement.getElementsByClassName("product-name")[0].innerText
    console.log(elt)
    for (let i = 0; i < cart.length; i++) {
        if (cart[i].title.toLowerCase() == elt.toLowerCase()) {
            cart.splice(i, 1)
            sessionStorage.setItem("cart", JSON.stringify(cart))
        }
    }
}

function quantityChanged(event) {
    var input = event.target
    if (isNaN(input.value) || input.value <= 0) {
        input.value = 1
    }
    updateTotal()

}

function updateTotal() {
    var orders = document.getElementsByClassName("orders")[0]
    var single_orders = orders.getElementsByClassName("cart-row")
    console.log(single_orders)

    total = 0
    amount = 0
    for (var i = 0; i < single_orders.length; i++) {
        var single_order = single_orders[i]
        var price_element = single_order.getElementsByClassName("price")[0]
        var quantity_element = single_order.getElementsByClassName("qty")[0]
        var price = parseFloat(price_element.innerText)
        var quantity = quantity_element.value
        console.log(price, quantity)
        cart[i].qty = quantity
        sessionStorage.setItem("cart", JSON.stringify(cart));
        qty = parseFloat(cart[i].qty);
        var total_price = price * qty
        amount += parseFloat(qty);
        total = total + (price * qty);
        console.log(document.getElementsByClassName("total-price"))
        document.getElementsByClassName("total-price")[i].innerText = total_price + " ብር"
    }

    document.getElementsByClassName("order-total")[0].innerText = total + " ብር"
        // document.getElementsByClassName("total")[0].innerText = total + " ብር"
        // document.getElementsByClassName("quantity")[0].innerText = amount + " መጻሕፍት"
}

function removeCart() {
    alert('መጽሐፉን ሲረከቡ ክፍያ የፈፀሙበትን ደረሰኝ ይያዙ!')
    cart = sessionStorage.getItem('cart')
    sessionStorage.clear()
    updateCartTotal()
}