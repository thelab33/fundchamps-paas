from app.extensions import db
import uuid

class SMSLog(db.Model):
    __tablename__ = "sms_logs"
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()))
    recipient = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(32), default="pending")  # sent, failed, delivered
    meta = db.Column(...)
    sent_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f"<SMSLog to {self.recipient} @ {self.sent_at}>"
