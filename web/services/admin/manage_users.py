import datetime
from math import ceil
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash
from web.models.customer import Customer
from web.models.user import User
from web.models.role import Role
from web import db

def get_users(page=1, page_size=10, search=None):
    query = User.query.options(joinedload(User.role))

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (User.Name.like(search_pattern)) | 
            (User.Phone.like(search_pattern))
        )

    total_records = query.count()
    total_pages = ceil(total_records / page_size) if total_records else 1
    users = (
        query.order_by(User.UserId.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return users, total_pages, total_records

def get_customers(page=1, page_size=10, search=None):
    query = Customer.query

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Customer.Name.like(search_pattern)) | 
            (Customer.Phone.like(search_pattern)) |
            (Customer.Email.like(search_pattern))
        )

    total_records = query.count()
    total_pages = ceil(total_records / page_size) if total_records else 1
    customers = (
        query.order_by(Customer.CustomerId.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return customers, total_pages, total_records

def create_staff(phone, password, role_id):
    if not phone or not password or not role_id:
        return None, "Thiếu thông tin"

    phone = str(phone).strip()

    # Kiểm tra trùng số điện thoại
    existing = User.query.filter_by(Phone=phone).first()
    if existing:
        return None, "Số điện thoại đã tồn tại"

    # Kiểm tra role_id có hợp lệ và không phải Customer
    role = Role.query.filter(Role.RoleId == role_id, Role.RoleId != 3).first()
    if not role:
        return None, "Role không hợp lệ"

    staff = User(
        Phone=phone,
        Password=generate_password_hash(password),
        RoleId=role.RoleId
    )

    db.session.add(staff)
    db.session.commit()
    return staff, None


def delete_staff(staff_id: int):
    staff = User.query.filter(User.UserId == staff_id, User.RoleId != 3).first()
    if not staff:
        return False, "Không tìm thấy nhân viên hoặc không hợp lệ"

    try:
        db.session.delete(staff)
        db.session.commit()
        return True, "Đã xóa nhân viên"
    except Exception as e:
        db.session.rollback()
        return False, f"Có lỗi khi xóa: {str(e)}"
    

def create_role(role_name: str, description: str):
    # Validate
    if not role_name.strip():
        return {"status": "error", "message": "Tên vai trò không được để trống"}, 400
    
    # Kiểm tra trùng tên
    existing_role = Role.query.filter(
        func.lower(Role.RoleName) == role_name.strip().lower()
    ).first()
    if existing_role:
        return {"status": "error", "message": "Tên vai trò đã tồn tại"}, 400

    try:
        new_role = Role(
            RoleName=role_name.strip(),
            Description=description.strip() if description else None
        )
        db.session.add(new_role)
        db.session.commit()

        return {
            "status": "success",
            "message": "Thêm role thành công",
            "role": {
                "RoleId": new_role.RoleId,
                "RoleName": new_role.RoleName,
                "Description": new_role.Description,
                "CreatedAt": new_role.CreatedAt.strftime("%Y-%m-%d %H:%M")
            }
        }, 201
    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": f"Lỗi: {str(e)}"}, 500

def toggle_role_status(role_id: int):
    role = Role.query.get(role_id)
    if not role:
        return {"status": "error", "message": "Role không tồn tại"}, 404
    
    try:
        role.IsActive = not role.IsActive
        db.session.commit()
        return {
            "status": "success",
            "message": "Cập nhật trạng thái thành công",
            "role": {
                "RoleId": role.RoleId,
                "IsActive": role.IsActive
            }
        }, 200
    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": str(e)}, 500
    

def update_role_service(role_id: int, role_name: str, description: str):
    role = Role.query.get(role_id)
    if not role:
        return {"status": "error", "message": "Role không tồn tại"}, 404

    if not role_name:
        return {"status": "error", "message": "Tên role không được để trống"}, 400

    # check trùng tên (ngoại trừ chính nó)
    existing = Role.query.filter(func.lower(Role.RoleName) == role_name.lower(), Role.RoleId != role_id).first()
    if existing:
        return {"status": "error", "message": "Tên role đã tồn tại"}, 400

    try:
        role.RoleName = role_name
        role.Description = description or None
        db.session.commit()

        return {
            "status": "success",
            "message": "Cập nhật role thành công",
            "role": {
                "RoleId": role.RoleId,
                "RoleName": role.RoleName,
                "Description": role.Description
            }
        }, 200
    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": f"Lỗi: {str(e)}"}, 500