from web.models.category import Category
from sqlalchemy import and_, asc
from web import db

def get_categories_by_parent_id(parent_id):
    return Category.query.filter(Category.ParentID == parent_id).all()

def get_categories_parent_id_notnull():
    return Category.query.filter(Category.ParentID != None).all()

def get_category_by_type(type: int):
    try:
        data = Category.query.filter_by(Status=1, Type=type, ParentID=None).all()
        return data
    except Exception as e:
        raise e

def get_grouped_categories():
    types = db.session.query(Category.Type).distinct().all()
    results = []
    for type_value, in types:
        parents = Category.query.filter_by(ParentID=None, Type=type_value, Status=1).order_by(asc(Category.ID)).all()
        for p in parents:
            p.children = Category.query.filter_by(ParentID=p.ID, Status=1).order_by(asc(Category.ID)).all()

        results.append({
            'type': type_value,
            'type_name': f'Loại {type_value}',
            'parents': parents
        })
    return results
