"""
Shared SQLAlchemy metadata for this project's tables.
All table definitions in db/tables/ import this instance so
metadata.create_all() can be used to reflect all tables at once.
"""

from sqlalchemy import MetaData

metadata = MetaData()
