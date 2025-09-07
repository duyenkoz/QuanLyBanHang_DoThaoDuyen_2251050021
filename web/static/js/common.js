function toastSuccess(text){
    $.toast({
        heading: "Thành công",
        text: text,
        showHideTransition: 'slide',
        icon: 'success',
        hideAfter: 3000,
        position: 'bottom-right',
    })
}

function toastError(text){
    $.toast({
        heading: "Lỗi",
        text: text,
        showHideTransition: 'slide',
        icon: 'error',
        hideAfter: 3000,
        position: 'bottom-right',
    })
}

function toastWarning(text){
    $.toast({
        heading: "Cảnh báo",
        text: text,
        showHideTransition: 'slide',
        icon: 'warning',
        hideAfter: 3000,
        position: 'bottom-right',
    })
}

function toastNewOrder(text){
    $.toast({
        heading: "Đơn hàng mới",
        text: text,
        hideAfter: false,
        showHideTransition: 'fade',
        position: 'top-right',
        bgColor: '#156c14',
        stack: 1
    })
}

function updateCartCount() {
    let cart = JSON.parse(localStorage.getItem("cart") || "[]");
    let count = cart.length;
    $(".cart-number").text(count);

    // Update number in the cart page
    if($(".cart-count-item")){
        $(".cart-count-item").text(count);
    }
}

function generateTempCartID() {
    const cart = JSON.parse(localStorage.getItem("cart") || "[]");
    const countCart = cart.length;
    return "ITEM_" + (countCart + 1);
}