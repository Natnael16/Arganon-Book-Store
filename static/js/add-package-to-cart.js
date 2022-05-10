if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready)
} else {
    ready()
}

function ready() {
    cart = sessionStorage;
    var addToCartButtons = document.getElementsByClassName('order-submit');
    val = []

    for (var i = 0; i < addToCartButtons.length; i++) {
        var button = addToCartButtons[i]
        button.addEventListener('click', addToCartClicked);
    }


}

function addToCartClicked(event) {

    var button = event.target
    var shopItem = button.parentElement.parentElement
    console.log(shopItem.parentElement.getElementsByClassName("product-img-nice")[0].src)
    var title = shopItem.getElementsByClassName("product-name")[0].innerText
    var price = parseInt(shopItem.getElementsByClassName("product-price")[0].innerText)
    var id = shopItem.getElementsByClassName("book-id")[0].innerText
    var image = shopItem.parentElement.getElementsByClassName("product-img-nice")[0].src
    var package = shopItem.getElementsByClassName("package")[0].value
    session = JSON.parse(sessionStorage.getItem("cart"));
    if (session) {
        val = JSON.parse(sessionStorage.getItem("cart"))
        for (var i = 0; i < session.length; i++) {
            if (session[i].id == id) {
                alert('This item is already added to the cart')
                return
            }
        }
            val.push({
                id: id,
                title: title,
                price: price,
                qty: 1,
                image: image,
                package: package
            })
        
    } else {
        val.push({
            id: id,
            title: title,
            price: price,
            qty: 1,
            image: image,
            package: package
        })
    }
    cart.setItem("cart", JSON.stringify(val))

}