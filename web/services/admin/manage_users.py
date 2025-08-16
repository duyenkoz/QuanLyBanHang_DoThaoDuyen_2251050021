import datetime
from web.models.user import User
from werkzeug.security import generate_password_hash
from web import db


def get_users_by_role(current_role):
    """
    Lấy danh sách người dùng theo role:
    - admin xem được staff
    - staff xem được user
    """
    if current_role == "admin":
        return User.query.filter_by(Role="staff").all()
    elif current_role == "staff":
        return User.query.filter_by(Role="user").all()
    return []

def add_user(phone: str, password: str) -> dict:
    """Thêm user mới với role = staff, không cần CreatedAt"""
    if not phone or not password:
        return {'success': False, 'message': 'Phone và password không được trống'}

    # Kiểm tra phone đã tồn tại chưa
    if User.query.filter_by(Phone=phone).first():
        return {'success': False, 'message': 'Số điện thoại đã tồn tại'}

    new_user = User(
        Phone=phone,
        Password=generate_password_hash(password),
        Role='staff'
    )

    db.session.add(new_user)
    try:
        db.session.commit()
        return {'success': True, 'message': 'Thêm người dùng thành công'}
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': f'Lỗi: {str(e)}'}