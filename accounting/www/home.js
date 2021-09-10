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

function openCart (event) {
    frappe.msgprint({
        message: cart.length == 0 ? 'Cart Empty!' : getCartItems(),
        title: 'Cart Checkout',
        primary_action: {
            'label': __('Checkout Invoice'),
            action: checkoutInvoice
        }
    })
}

function getCartItems() {
    var html = ``

    for (let i = 0; i < cart.length; i++) {
        html += `<div style="margin-bottom: 5px;">
                    <p>${cart[i]}</p>
                    <input class="item" type="number" min="1" value="1" item-name="${cart[i]}" style="width: 60px;">
                    <br>
                    <hr>
                </div>`
    }

    return html
}


function checkoutInvoice() {
    var argsData = [];
    var itemsList = document.querySelectorAll('.item');

    for (let i = 0; i < itemsList.length; i++) {
        argsData.push({
            itemName: itemsList[i].getAttribute('item-name'),
            quantity: itemsList[i].value
        })
    }

    console.log(argsData)

    frappe.call({
        method: 'accounting.accounting.doctype.sales_invoice.sales_invoice.generate_sales_invoice',
        args: {
            data: JSON.stringify(argsData)
        },
        callback: () => {
            //location.reload()
            alert('callback complete')
        }
    })
}
