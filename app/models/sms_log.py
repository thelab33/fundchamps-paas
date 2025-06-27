from app import db

class SmsLog(db.Model):
    __tablename__='sms_logs'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(32))
    message = db.Column(db.Text)
