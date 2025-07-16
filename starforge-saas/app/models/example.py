import uuid
from app.extensions import db
from .mixins import TimestampMixin, SoftDeleteMixin


class Example(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "example"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        db.String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Example {self.name}>"

    def as_dict(self, exclude=None, include=None):
        cols = [c.name for c in self.__table__.columns]
        if include:
            cols = [c for c in cols if c in include]
        if exclude:
            cols = [c for c in cols if c not in exclude]
        return {c: getattr(self, c) for c in cols}

    @classmethod
    def by_uuid(cls, uuid_):
        return cls.query.filter_by(uuid=str(uuid_)).first()
