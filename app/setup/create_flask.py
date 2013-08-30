from flask import Flask, g
from flask.ext.restful import Api
from app.setup.database import get_session_from_uri, initialize_base
from app.views import index_page
from app.resources import FileList, FileInfo

def create_flask(flask_config, database_config):
	"""A factory that outputs a flask app given config objects"""
	app = Flask('app')
	app.config.from_object(flask_config)
	app.register_blueprint(index_page)
	api = Api(app)
	api.add_resource(FileList, '/files')
	api.add_resource(FileInfo, '/files/<string:file_name>')
	
	@app.before_request
	def before_request():
	        g.db = get_session_from_uri(database_config.URI)
	        initialize_base(g.db)
	
	@app.teardown_appcontext
	def shutdown_session(exception=None):
	        db = getattr(g, 'db', None)
	        if db is not None:
			db.remove()
	
	return app
