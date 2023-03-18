from flask import blueprints, Blueprint

bookmarks = Blueprint('bookmarks', __name__, url_prefix='/api/v1/bookmarks')


@bookmarks.get('/')
def get_all():
    return []
