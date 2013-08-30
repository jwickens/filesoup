from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.setup.config import DATABASE_CONFIG, DATABASE_TESTING_CONFIG

def get_engine(database_uri):
	"""Returns an SQLAlchemy engine given a database uri."""
	return create_engine(
				database_uri,
				convert_unicode=True,
				)



def initialize_base(db_session):
	"""Binds the models with session."""
	from app.models import Base
	Base.query = db_session.query_property()

def get_session_from_engine(engine):
	"""
	Provides a database session, and also calls :class:`initialize_base`.
	:param engine: an SQLAlchemy engine to connect to the database.
	"""
	db_session = scoped_session(
				sessionmaker(
					autocommit=False,
					autoflush=False,
					bind=engine,
					)
				)
	initialize_base(db_session)
	return db_session

def get_session_from_uri(database_uri):
	"""Shortcut to :func`get_session_from_engine`"""
	return get_session_from_engine(get_engine(database_uri))

def create_base(Base, engine):
	"""
	Creates the tables
	:param Base: a SQLAlchemy DeclarativeBase instance.
	:param engine: an SQLAlchemy engine.
	"""
	from app.models import Archive
	Base.metadata.create_all(bind=engine)
