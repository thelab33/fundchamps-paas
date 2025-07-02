import uuid
from datetime import datetime
from app import db

# ──────────────────────────────────────────────────────────────
# Starforge Championship Mixins for All Models
# ──────────────────────────────────────────────────────────────

class TimestampMixin(object):
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
        doc="UTC time record created"
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        index=True,
        doc="UTC time record last updated"
    )

    @staticmethod
    def _update_timestamp(mapper, connection, target):
        target.updated_at = datetime.utcnow()

    @classmethod
    def __declare_last__(cls):
        from sqlalchemy import event
        event.listen(cls, 'before_update', cls._update_timestamp)

class SoftDeleteMixin(object):
    deleted = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
        index=True,
        doc="Soft-delete flag"
    )

    def soft_delete(self, commit=True):
        """Mark as soft-deleted."""
        self.deleted = True
        if commit:
            db.session.commit()

    def restore(self, commit=True):
        """Restore from soft-delete."""
        self.deleted = False
        if commit:
            db.session.commit()

    @classmethod
    def active(cls):
        """Query only non-deleted rows."""
        return cls.query.filter_by(deleted=False)

    @classmethod
    def trashed(cls):
        """Query only deleted rows."""
        return cls.query.filter_by(deleted=True)

# ──────────────────────────────────────────────────────────────
# Example Model Using Starforge Mixins
# ──────────────────────────────────────────────────────────────

class Example(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'example'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        db.String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Example {self.name}>"

    def as_dict(self, exclude=None, include=None):
        """Flexible dict serialization, with exclude/include lists."""
        columns = [c.name for c in self.__table__.columns]
        if include:
            columns = [c for c in columns if c in include]
        if exclude:
            columns = [c for c in columns if c not in exclude]
        return {c: getattr(self, c) for c in columns}

    @classmethod
    def by_uuid(cls, uuid_):
        """Get by UUID (string or UUID obj)."""
        return cls.query.filter_by(uuid=str(uuid_)).first()

# Add this after Example in models.py

class Sponsor(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'sponsors'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(32), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    # Add any other fields you use in your routes!

    def __repr__(self):
        return f"<Sponsor {self.name}: {self.amount} ({self.status})>"

# ──────────────────────────────────────────────────────────────
# End Starforge Model Pack
# ──────────────────────────────────────────────────────────────

