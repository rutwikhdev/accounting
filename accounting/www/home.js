let addToCartBtns = document.querySelectorAll(".addtocart");
let cartBtn = document.querySelector('.cart');
let cart = [];

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
    let itemsList = document.querySelectorAll('.item');

    for (let i = 0; i < itemsList.length; i++) {
        argsData.push({
            itemName: itemsList[i].getAttribute('item-name'),
            quantity: itemsList[i].value
        })
    }

    frappe.call({
        method: 'accounting.accounting.doctype.sales_invoice.sales_invoice.generate_sales_invoice',
        args: {
            data: JSON.stringify(argsData)
        },
        callback: (res) => {
            getPDF('Sales Invoice', res.message, 'pdf')
        }
    })
}

function getPDF(doctype, docname, print_format, letterhead='', lang_code='') {

    let full_pdf_url = get_full_url(
        '/printview?doctype=' +
        encodeURIComponent(doctype) +
        '&name=' +
        encodeURIComponent(docname) +
        '&trigger_print=1' +
        '&format=' +
        encodeURIComponent(print_format) +
        '&no_letterhead=' +
        (letterhead ? '0' : '1') +
        '&letterhead=' +
        encodeURIComponent(letterhead) +
        (lang_code ? '&_lang=' + lang_code : '')
    )

    const w = window.open(full_pdf_url)

    if (!w) {
        frappe.msgprint('Please enable popup!')
    }
}

function get_full_url(url) {
    if(url.indexOf("http://")===0 || url.indexOf("https://")===0) {
        return url;
    }
    return url.substr(0,1)==="/" ?
        (get_base_url() + url) :
        (get_base_url() + "/" + url);
}

function get_base_url() {
    // base url
    var url = (frappe.base_url || window.location.origin);
    if(url.substr(url.length-1, 1)=='/') url = url.substr(0, url.length-1);

    return url
}
