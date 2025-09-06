from math import ceil
from web import db
from web.models import Category
from web.extentions.pagination import calcPagination

def get_categories(search=None, page=1, page_size=10):
    """Hàm lấy danh sách danh mục với phân trang"""
    query = Category.query.filter(Category.ParentID.is_(None))  # Lấy danh mục cha
    if search:
        query = query.filter(Category.Title.like(f"%{search}%"))

    total_records = query.count()
    total_pages = ceil(total_records / page_size)

    query = query.order_by(Category.ID.desc())
    categories = query.offset((page - 1) * page_size).limit(page_size).all()

    pagination = calcPagination(page, total_pages)

    return categories, pagination, total_records

def get_category_by_id(category_id):
    return Category.query.filter_by(ID=category_id).first()


def get_children_by_parent_id(parent_id):
    return Category.query.filter_by(ParentID=parent_id).all()

def get_all_parent_categories():
    return Category.query.filter_by(ParentID=None).all()


def update_category_status(category_id):
    category = Category.query.get(category_id)
    if not category:
        return None

    # Đảo ngược trạng thái
    category.Status = 0 if category.Status == 1 else 1
    new_status = category.Status
    is_parent = category.ParentID is None

    # Nếu là danh mục cha, cập nhật luôn các danh mục con
    if is_parent:
        children = Category.query.filter_by(ParentID=category.ID).all()
        for child in children:
            child.Status = new_status

    db.session.commit()
    return {
        "new_status": new_status,
        "is_parent": is_parent
    }

def create_child_category(title, parent_id, type, type_code, status):
    try:
        parent = get_category_by_id(parent_id)
        if not parent:
            raise Exception("Danh mục cha không tồn tại")

        new_category = Category(
            Title=title,
            ParentID=parent_id,
            Type=type,
            TypeCode=type_code,
            Status=status
        )

        db.session.add(new_category)
        db.session.commit()

        return {
            "id": new_category.ID,
            "title": new_category.Title,
            "status": new_category.Status,
            "type_code": new_category.TypeCode
        }
    except Exception as e:
        db.session.rollback()
        raise e
    
def update_inline_category_service(cate_id, title, type, is_parent, type_code=None):
    category = Category.query.get(cate_id)
    if not category:
        return {"status_code": "ERROR", "message": "Danh mục không tồn tại"}

    category.Title = title

    if is_parent:
        category.Type = int(type)

        # Cập nhật tất cả danh mục con theo cha
        children = Category.query.filter_by(ParentID=cate_id).all()
        for child in children:
            child.Type = int(type)
    else:
        # Nếu là child thì cập nhật TypeCode (nếu có truyền vào)
        if type_code:
            category.TypeCode = type_code

    db.session.commit()
    return {"status_code": "SUCCESS"}


def create_category(title, parent_id, type_value, type_code_value, status):
    try:
        if not parent_id:  # Danh mục cha
            new_cate = Category(
                Title=title,
                ParentID=None,
                Type=int(type_value),
                TypeCode=None,
                Status=int(status)
            )
        else:  # Danh mục con
            # Lấy danh mục cha từ CSDL để lấy Type
            parent_cate = Category.query.get(parent_id)
            if not parent_cate:
                return {"success": False, "error": "Danh mục cha không tồn tại"}

            new_cate = Category(
                Title=title,
                ParentID=parent_id,
                Type=parent_cate.Type,
                TypeCode=type_code_value,
                Status=int(status)
            )

        db.session.add(new_cate)
        db.session.commit()
        return {"success": True, "category": new_cate}

    except Exception as e:
        db.session.rollback()
        return {"success": False, "error": str(e)}
    

def delete_category(cate_id):
    category = Category.query.get(cate_id)
    if not category:
        return None, "Không tìm thấy danh mục"

    # Kiểm tra xem danh mục có sản phẩm không
    if category.products and len(category.products) > 0:
        return None, "Danh mục đang có sản phẩm, không thể xóa!"

    # Nếu không có sản phẩm thì cho phép xóa
    db.session.delete(category)
    db.session.commit()
    return category, None