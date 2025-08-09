from flask import Blueprint, render_template, request, jsonify
from web.services import product as productService
import json
products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
@products_bp.route('/products/<int:id>', methods=['GET'])
def products_page(id=None):
    top = int(request.args.get('top', 10))
    cursor = int(request.args.get('cursor', 0))
    keyword = request.args.get('kw')
    cateid = request.args.get('cateid') or id
    products, cursor = productService.get_product_filter(keyword=keyword, cate_id=cateid, cursor=cursor, top=top)
    return render_template("products/index.html", products=products, cursor=cursor)

@products_bp.route('/products/detail/<int:product_id>', methods=['GET'])
def product_detail(product_id):
    product = productService.get_product_by_id(product_id)
    return render_template("products/product_detail.html", product=product)

#API
@products_bp.get('/api/products')
def api_get_product_filter():
    top = int(request.args.get('top'))
    cursor = int(request.args.get('cursor'))
    keyword = request.args.get('kw')
    cateid = request.args.get('cateid')
    products, cursor = productService.get_product_filter(keyword=keyword, cate_id=cateid, cursor=cursor, top=top)
    template_html = ""
    for product in products:
        template_html += render_template("components/product_card.html", product=product)
    result = {
        "products_html": template_html,
        "cursor": cursor
    }
    return json.dumps(result, ensure_ascii=False)

@products_bp.route('/api/products/detail/<int:product_id>', methods=['GET'])
def api_get_product_detail(product_id):
    product = productService.get_product_by_id(product_id)
    return render_template("components/product_detail.html", product=product)
