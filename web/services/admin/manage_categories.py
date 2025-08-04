from math import ceil
from web import db
from web.models import Category
from web.extentions.pagination import calcPagination

def get_categories(search=None, page=1, page_size=10):
    """Hàm lấy danh sách danh mục với phân trang"""
    query = Category.query.filter(Category.ParentID == None)
    if search:
        query = query.filter(Category.Title.like(f"%{search}%"))

    total_records = query.count()
    total_pages = ceil(total_records / page_size)

    query = query.order_by(Category.ID.desc())
    categories = query.offset((page - 1) * page_size).limit(page_size).all()

    pagination = calcPagination(page, total_pages)

    return categories, pagination, total_records

def create_category(title, type_, status=1, parent_id=None):
    """Hàm tạo danh mục (lớn hoặc nhỏ)."""
    if not title:
        raise ValueError("Tên danh mục không được để trống")

    category = Category(
        Title=title,
        Type=type_,
        Status=status,
        ParentID=parent_id
    )
    db.session.add(category)
    db.session.commit()
    return category