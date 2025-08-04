from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from web.models import Product
from web.services.product import get_product_by_title, get_all_products
from web.services import category as cateService
from web import db
from werkzeug.utils import secure_filename
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/', methods=['GET'])
def admin_dashboard():
    return render_template('admin/layout_admin/base.html')


