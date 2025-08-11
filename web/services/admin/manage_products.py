from math import ceil
from web.extentions.pagination import calcPagination
from web.models import Product
from web import db

def update_product_status(product_id):
    """Hàm xử lý cập nhật trạng thái sản phẩm"""
    product: Product = Product.query.get(product_id)
    if product:
        product.Status = 0 if product.Status == 1 else 1
        db.session.commit()
        return product.Status
    else:
        return None
    
def get_products(search=None, page=1, page_size=10):
    """Hàm lấy danh sách sản phẩm với phân trang"""
    query = Product.query
    if search:
        query = query.filter(Product.Title.like(f"%{search}%"))

    total_records = query.count()
    total_pages = ceil(total_records / page_size)
    query = query.order_by(Product.ID.desc())
    products = query.offset((page - 1) * page_size).limit(page_size).all()

    for product in products:
        if product.Img and not product.Img.startswith('images/'):
            product.Img = f'images/{product.Img}'

    pagination = calcPagination(page, total_pages)
    
    return products, pagination, total_records
    

def create_product(title, price, description=None, status=None, category_id=None, image_filename=None):
    try:
        # Nếu không có ảnh, gán ảnh mặc định
        if not image_filename:
            image_filename = "no_image.jpg"

        new_product = Product(
            Title=title,
            Price=price,
            Description=description,
            Img=f"{image_filename}",
            Status=status,
            CategoryID=category_id,
        )
        db.session.add(new_product)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False
    
def check_product_exists(id):
    """Hàm kiểm tra sản phẩm đã tồn tại hay chưa"""
    return Product.query.filter(Product.ID == id).first() is not None

def get_product_by_id(product_id):
    """Hàm lấy sản phẩm theo ID"""
    return Product.query.get(product_id)

def update_product(product_id, title, price, description=None, status=None, category_id=None, image_filename=None):
    """Hàm cập nhật thông tin sản phẩm"""
    product: Product = get_product_by_id(product_id)
    if not product:
        return False

    product.Title = title
    product.Price = price
    product.Description = description
    product.Status = status
    product.CategoryID = category_id

    # Nếu có upload ảnh mới
    if image_filename:
        product.Img = f"{image_filename}"
    else:
        # Nếu trước đó không có ảnh hoặc ảnh bị xóa → gán ảnh mặc định
        if not product.Img or product.Img.strip() == "":
            product.Img = "no_image.jpg"

    db.session.commit()
    return True
