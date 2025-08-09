from web.models.user import User
from web import db

def get_user_by_id(user_id):
    return db.session.query(User).filter_by(Id=user_id).first()

def update_user_profile(user_id, full_name, address, ward, district, province):
    user = get_user_by_id(user_id)
    if not user:
        return False, "Người dùng không tồn tại"

    # Gộp địa chỉ đầy đủ
    full_address = f"{address}, {ward}, {district}, {province}"

    user.Name = full_name
    user.Address = full_address

    try:
        db.session.commit()
        return True, "Cập nhật thông tin thành công"
    except Exception as e:
        db.session.rollback()
        return False, "Có lỗi xảy ra khi cập nhật"
