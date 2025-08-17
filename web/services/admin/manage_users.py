import datetime
from math import ceil
from web.models.user import User
from werkzeug.security import generate_password_hash
from web import db

def get_users_by_role(role, page=1, page_size=10, search=None):
    """Lấy danh sách user theo role với phân trang"""
    query = User.query.filter(User.Role == role)

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(User.Name.like(search_pattern) | User.Phone.like(search_pattern))

    total_records = query.count()
    total_pages = ceil(total_records / page_size)
    users = query.order_by(User.Id.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return users, total_pages, total_records

def create_staff(phone, password):
    if not phone or not password:
        return None, "Thiếu thông tin"
    
    phone = str(phone).strip()

    # Kiểm tra trùng số điện thoại
    existing = User.query.filter_by(Phone=phone).first()
    if existing:
        return None, "Số điện thoại đã tồn tại"

    staff = User(
        Phone=phone,
        Password=generate_password_hash(password),  
        Role="staff"
    )

    db.session.add(staff)
    db.session.commit()
    return staff, None

def delete_staff(staff_id: int):
    """Xóa staff theo ID, trả về (True/False, message)"""
    staff = User.query.get(staff_id)
    if not staff:
        return False, "Không tìm thấy nhân viên"

    db.session.delete(staff)
    db.session.commit()
    return True, "Đã xóa nhân viên"