from web.models.customer import Customer
from web import db
from web.models.user import User

def get_user_by_id(user_id):
    return db.session.query(Customer).filter_by(CustomerId=user_id).first()

def update_user_profile(user_id, role, full_name, email, address_street, ward, district, province):
    if role == "customer":
        user = Customer.query.get(user_id)
    else:
        user = User.query.get(user_id)

    if not user:
        return False, "Người dùng không tồn tại"

    # Bảo đảm chỉ lấy phần street (phòng trường hợp client gửi full address)
    street = address_street.split(",")[0].strip() if address_street else ""

    address_parts = [part for part in [street, ward, district, province] if part]
    full_address = ", ".join(address_parts) if address_parts else None

    user.Name = full_name
    user.Email = email
    user.Address = full_address

    try:
        db.session.commit()
        return True, "Cập nhật thông tin thành công"
    except Exception:
        db.session.rollback()
        return False, "Có lỗi xảy ra khi cập nhật"
