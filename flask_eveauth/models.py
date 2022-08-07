from secrets import token_urlsafe

from flask import current_app
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class ModelMixin:
    @staticmethod
    def _get_db():
        return current_app.extensions['sqlalchemy'].db

    def save(self):
        db = self._get_db()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db = self._get_db()
        db.session.delete(self)
        db.session.commit()


class User(Base, ModelMixin):
    __tablename__ = 'user'

    id = Column(String, primary_key=True, default=token_urlsafe)
    expires_in = Column(Integer, nullable=False)
    token_type = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    access_token = Column(String, nullable=False)
    name = Column(String, nullable=False)
    character_id = Column(Integer, nullable=False)

    def get(self, user_id):
        db = self._get_db()
        return db.session.get(User, user_id)

    def portrait_url(self, size=512):
        if size not in [64, 128, 256, 512]:
            size = 512
        return f'https://images.evetech.net/characters/{self.character_id}/portrait?tenant=tranquility&size={size}'


class Role(Base, ModelMixin):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return self.name


class Permission(Base, ModelMixin):
    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True)
    entity_name = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'))
    role = relationship(Role, backref=backref('entities', lazy='dynamic'), foreign_keys=[role_id])
