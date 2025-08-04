from urllib import request
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user
from web import app
from web.services import category as categoryService
from web.services import auth
from web.routes.products import products_bp
from web.routes.home import home_bp
from web.routes.admin.admin import admin_bp
from web.routes.admin.manage_products import admin_prod_bp
from web.routes.admin.manage_categories import admin_cate_bp

@app.context_processor
def init_menu():
    menu = categoryService.get_category_by_type(1)
    product_package = categoryService.get_category_by_type(2)
    return dict(menu=menu, product_package=product_package)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = auth.login(username, password)

        if user:
            login_user(user)
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/')
def home():
    return render_template("home/index.html")

#Register route
app.register_blueprint(products_bp)
app.register_blueprint(home_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(admin_prod_bp)
app.register_blueprint(admin_cate_bp)

if __name__ == '__main__':
    app.run(debug=True)