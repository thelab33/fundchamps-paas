import pytest
from app import create_app, db
from app.models import Example

@pytest.fixture
def app_context():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_soft_delete_restore(app_context):
    ex = Example(name="Test", description="Testing")
    db.session.add(ex)
    db.session.commit()
    assert ex.deleted is False

    # Soft delete
    ex.soft_delete()
    assert ex.deleted is True
    # Restore
    ex.restore()
    assert ex.deleted is False

def test_timestamps_autoset(app_context):
    ex = Example(name="Timestamps")
    db.session.add(ex)
    db.session.commit()
    assert ex.created_at is not None
    assert ex.updated_at is not None

    old_updated = ex.updated_at
    ex.name = "Updated"
    db.session.commit()
    assert ex.updated_at > old_updated
