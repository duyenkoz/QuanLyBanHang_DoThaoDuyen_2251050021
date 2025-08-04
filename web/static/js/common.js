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