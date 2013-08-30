from flask import Blueprint

index_page = Blueprint('index_page', __name__)

@index_page.route('/')
@index_page.route('/index')
def index():
	"""Hello, World!"""
	return "Hello, World!"
