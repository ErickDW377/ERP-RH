from enum import unique

from sqlalchemy.sql.expression import column
from sqlalchemy.sql.sqltypes import VARCHAR
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,Date,Float,ForeignKey,Boolean
from sqlalchemy.orm import relationship


db=SQLAlchemy()