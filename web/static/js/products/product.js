$(document).ready(function () {
    var cursor = $("#product-cursor").val();
    var cateid = $("#product-cateid").val();
    var top = 2;
    $("#btn-loadmore").click(function () {
        if (!cateid) {
            cateid = "";
        }
        $.ajax({
            method: "GET",
            url: `/api/products?top=${top}&cursor=${cursor}&cateid=${cateid}`,
            success: function (response) {
                const data = JSON.parse(response);
                const container = $(".product-container");
                if (container.length > 0) {
                    container.append(data.products_html)
                }
                cursor = data.cursor;
                has_load_more = data.has_load_more;
                $("#product-cursor").val(cursor);
                if (has_load_more) {
                    $("#btn-loadmore").show();
                } else {
                    $("#btn-loadmore").hide();
                }
                if (!cursor) {
                    $("#btn-loadmore").hide();
                }

            },
            error: function (err) {
                console.log(err);
            }
        })
    });
});

$(document).on("click", ".btn-buy", function () {
    try {
        const productid = $(this).data("itemid");
        const name = $(this).data("itemname");
        const typeCode = $(this).data("typecode");
        handleClickBuy(productid, name, typeCode);
    }
    catch (e) {
        toastError("Có lỗi xảy ra khi thêm vào giỏ hàng");
    }
});

function handleClickBuy(productid, name, typeCode) {
    if (typeCode === "DRINK_SIZE_ONLY" || typeCode === "DRINK_FULL") {
        $.ajax({
            url: `/api/products/detail/${productid}`,
            method: "GET",
            success: function (response) {
                $("#modal-product-detail-body").html(response);
                $("#modal-product-detail").modal("show");
            },
            error: function (err) {
                toastError("Có lỗi xảy ra khi lấy thông tin sản phẩm");
            }
        });
    } else {
        addToCart(productid, name, 1);
    }
}

function addToCart(productid, name, quantity, callback) {
    var cart = JSON.parse(localStorage.getItem("cart")) || [];
    const existingItem = cart.find(item => item.productid === productid);
    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        const item = {
            id: generateTempCartID(),
            productid: productid,
            quantity: quantity || 1,
        };
        cart.push(item);
    }
    localStorage.setItem("cart", JSON.stringify(cart));
    toastSuccess(`Thêm "${name}" vào giỏ hàng thành công`);
    const cartNumber = $(".cart-number");

    if (cartNumber.length > 0) {
        cartNumber.text(cart.length);
    }

    if (callback) {
        callback();
    }
}

function addToCartWithDetails(productid, name, quantity, size, sugar, ice, toppings, callback) {
    var cart = JSON.parse(localStorage.getItem("cart")) || [];
    const existingItem = cart.find(item => item.productid === productid && item.size === size && item.sugar === sugar && item.ice === ice && JSON.stringify(item.toppings) === JSON.stringify(toppings));
    if (existingItem) {
        existingItem.quantity += quantity;
        existingItem.size = size;
        existingItem.sugar = sugar;
        existingItem.ice = ice;
        existingItem.toppings = toppings;
    } else {
        const item = {
            id: generateTempCartID(),
            productid: productid,
            name: name,
            quantity: quantity || 1,
            size: size,
            sugar: sugar,
            ice: ice,
            toppings: toppings
        };
        cart.push(item);
    }
    localStorage.setItem("cart", JSON.stringify(cart));
    toastSuccess(`Thêm "${name}" vào giỏ hàng thành công`);

    const cartNumber = $(".cart-number");

    if (cartNumber.length > 0) {
        cartNumber.text(cart.length);
    }

    if (callback) {
        callback();
    }
}