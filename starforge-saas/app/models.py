import uuid
from datetime import datetime

from app.extensions import db

# ─── Mixins ───────────────────────────────────────────────────────────────────

class TimestampMixin:
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
        doc="UTC time record created",
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        index=True,
        doc="UTC time record last updated",
    )

    @staticmethod
    def _update_timestamp(mapper, connection, target):
        target.updated_at = datetime.utcnow()

    @classmethod
    def __declare_last__(cls):
        from sqlalchemy import event
        event.listen(cls, "before_update", cls._update_timestamp)


class SoftDeleteMixin:
    deleted = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
        index=True,
        doc="Soft-delete flag"
    )

    def soft_delete(self, commit=True):
        self.deleted = True
        if commit:
            db.session.commit()

    def restore(self, commit=True):
        self.deleted = False
        if commit:
            db.session.commit()

    @classmethod
    def active(cls):
        return cls.query.filter_by(deleted=False)

    @classmethod
    def trashed(cls):
        return cls.query.filter_by(deleted=True)

# ─── Models ───────────────────────────────────────────────────────────────────

class Sponsor(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "sponsors"
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()), index=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=True, index=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    status = db.Column(db.String(32), nullable=False, default="pending", index=True)
    message = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Sponsor {self.name} - ${self.amount}>"


class CampaignGoal(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "campaign_goals"
    id = db.Column(db.Integer, primary_key=True)
    goal_amount = db.Column(db.Numeric(10, 2), nullable=False, default=10000)
    total = db.Column(db.Numeric(10, 2), nullable=True)
    active = db.Column(db.Boolean, default=True, nullable=False, index=True)

    def __repr__(self):
        return f"<CampaignGoal ${self.goal_amount} active={self.active}>"


class Example(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "example"
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()), index=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Example {self.name}>"

    def as_dict(self, exclude=None, include=None):
        columns = [c.name for c in self.__table__.columns]
        if include:
            columns = [c for c in columns if c in include]
        if exclude:
            columns = [c for c in columns if c not in exclude]
        return {c: getattr(self, c) for c in columns}

    @classmethod
    def by_uuid(cls, uuid_):
        return cls.query.filter_by(uuid=str(uuid_)).first()

