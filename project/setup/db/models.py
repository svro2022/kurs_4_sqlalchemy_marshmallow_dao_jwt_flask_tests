from sqlalchemy import Column, DateTime, func, Integer

from project.setup.db import db


"""Базовый класс для создания моделей"""
"""created - запись была создана"""
"""updated - запись обновлена"""
"""func.now() - текущее время, чтобы знать, когда запись была создана и обновлена"""
class Base(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, nullable=False, default=func.now())
    updated = Column(DateTime, default=func.now(), onupdate=func.now())
