from urllib import request
from flask import Flask, render_template
from flask_login import login_user
from web import app
from web.services import category as categoryService
from web.routes.products import products_bp
from web.routes.home import home_bp
from web.routes.admin.admin import admin_bp
from web.routes.admin.manage_products import admin_prod_bp
from web.routes.admin.manage_categories import admin_cate_bp
from web.routes.auth import auth_bp
from web.routes.user import user_bp
from web.routes.cart import cart_bp
from web.routes.order import order_bp
from web.routes.admin.manage_orders import admin_order_bp
from web.routes.admin.manage_users import admin_user_bp
from web.routes.admin.dashboard import admin_dashboard_bp



@app.context_processor
def init_menu():
    menu = categoryService.get_category_by_type(1)
    product_package = categoryService.get_category_by_type(2)
    return dict(menu=menu, product_package=product_package)


@app.route('/')
def home():
    return render_template("home/index.html")

#Register route
app.register_blueprint(products_bp)
app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(order_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(admin_prod_bp)
app.register_blueprint(admin_cate_bp)
app.register_blueprint(admin_order_bp)
app.register_blueprint(admin_user_bp)
app.register_blueprint(admin_dashboard_bp)

if __name__ == '__main__':
    app.run(debug=True)