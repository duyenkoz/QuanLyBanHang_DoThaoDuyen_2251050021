from ..models.user import Users
from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@home_bp.route('/home')
def home_page():
    return render_template('home/index.html')