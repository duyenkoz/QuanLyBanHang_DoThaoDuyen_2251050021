from web.models.order import Order
from web import db


def update_order_status(order_id, new_status=None, shipper_id=None, remove_shipper=False, cancel_reason=None):
    order = Order.query.filter_by(ID=order_id).first()
    if not order:
        return False, "Không tìm thấy đơn hàng"

    if new_status:
        order.Status = new_status

    if shipper_id and new_status == "SHIPPING":
        order.ShipperId = shipper_id

    if remove_shipper:
        order.ShipperId = None

    if cancel_reason is not None and new_status == "CANCELED":
        order.CancelReason = cancel_reason   # cần cột CancelReason trong bảng Order

    try:
        db.session.commit()
        return True, "Cập nhật thành công"
    except Exception as e:
        db.session.rollback()
        return False, str(e)