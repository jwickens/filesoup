"""Defines the SQLAlchemy models to store the apps data."""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Archive(Base):
	"""The model representation SQLAlchemy must use to store files into the database."""
	__tablename__ = 'files'

	id = Column(Integer, primary_key = True)
	file_name = Column(String(260))
	size = Column(Integer)
	modified = Column(Integer) #Todo: implement as datetime for greater flexibility.
	created = Column(Integer)

	def __repr__(self):
		return '<File %r>' % (self.file_name)


	#def dump_datetime(value):
	#	"""Deserialize datetime object into string form for JSON processing."""
	#	if value is None:
	#		return None
	#	return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

	@property
	def serialize(self):
		"""Returns a python dictionary representation of the file for easy serialization to JSON"""
		return {
				'file_name': self.file_name,
				'size': self.size,
				'modified': self.modified,
				'created': self.created,
				}
