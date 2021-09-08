var addToCartBtns = document.querySelectorAll(".addtocart");
var cartBtn = document.querySelector('.cart');
var cart = [];

// add event listener to `cart` button
cartBtn.addEventListener('click', openCart);

// add event listener to `add to cart` buttons
for (let btn of addToCartBtns) {
    btn.addEventListener('click', addToCart);
}

function addToCart (event) {
    const target = event.target
    const itemName = target.getAttribute('data-attribute')

    if (cart.includes(itemName)) {
        // remove from list
        cart = cart.filter((el) => {
            return el != itemName
        })
        target.classList.remove('btn-danger')
        target.classList.add('btn-primary')
        target.innerText = 'Add to Cart'
    } else {
        cart.push(itemName)
        target.classList.remove('btn-primary')
        target.classList.add('btn-danger')
        target.innerText = 'Remove from Cart'
    }
}

