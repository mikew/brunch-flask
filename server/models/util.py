from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func

import datetime

db = SQLAlchemy()


def make_index(table_name, *columns):
    columns_joined = '_'.join(columns)
    return db.Index('%s_%s' % (table_name, columns_joined), *columns)


class IdMixin(object):
    """
    Provides the :attr:`id` primary key column
    """
    id = db.Column(db.Integer, primary_key=True)


class TimestampMixin(object):
    """
    Provides the :attr:`created_at` and :attr:`updated_at` audit timestamps
    """
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=datetime.datetime.utcnow, nullable=False)
