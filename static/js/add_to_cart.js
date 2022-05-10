if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready)
} else {
    ready()
}

function ready() {
    cart = sessionStorage;
    var addToCartButtons = document.getElementsByClassName('add-to-cart-btn')
    val = []

    for (var i = 0; i < addToCartButtons.length; i++) {
        var button = addToCartButtons[i]
        button.addEventListener('click', addToCartClicked)
    }

    // document.getElementsByClassName('btn-purchase')[0].addEventListener('click', purchaseClicked)
}

function addToCartClicked(event) {

    var button = event.target
    var shopItem = button.parentElement.parentElement.parentElement
    // console.log(shopItem.getElementsByClassName("book-id")[0].innerText)
    var title = shopItem.getElementsByClassName("product-name")[0].innerText
    var price = parseInt(shopItem.getElementsByClassName("product-price")[0].innerText)
    var book = shopItem.getElementsByClassName("book-id")[0].innerText
    var image = shopItem.parentElement.parentElement.getElementsByClassName("product-preview")[0].firstElementChild.src
    var package = shopItem.getElementsByClassName("package")[0].value
    console.log(package)
    session = JSON.parse(sessionStorage.getItem("cart"));
    if (session) {
        val = JSON.parse(sessionStorage.getItem("cart"))
        for (var i = 0; i < session.length; i++) {
            if (session[i].id == book) {
                alert('This item is already added to the cart')
                return
            }
        }
        val.push({
            id: book,
            title: title,
            price: price,
            qty: 1,
            image: image,
            package: package
        })

    } else {
        val.push({
            id: book,
            title: title,
            price: price,
            qty: 1,
            image: image,
            package: package
        })
    }
    console.log(val)
    cart.setItem("cart", JSON.stringify(val))

}