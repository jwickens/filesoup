"""Defines API endpoints using the Flask-RESTful extension."""
from flask.ext.restful import Resource
from flask import jsonify, g
from models import Archive

class FileList(Resource):
	""""An implementation of the flask-restful Resource that defines get to return a list of all Archive objects, serializing them."""
	def get(self):
		result = g.db.query(Archive).order_by('file_name').all()
		return jsonify({item.file_name: item.serialize for item in result})

class FileInfo(Resource):
	""""An implementation of the flask-restful Resource that defines get to return a serialized Archive object."""
	def get(self, file_name):
		'''
		:param file_name: the name of the file to look up.
		:type file_name: string
		'''
		result = g.db.query(Archive).filter_by(file_name = file_name).first()
		if result != None:
			return jsonify(result.serialize)
		else:
			return jsonify({'name': 'DOES_NOT_EXIT'})

