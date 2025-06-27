from app import db

class CampaignGoal(db.Model):
    __tablename__ = "campaign_goals"

    id           = db.Column(db.Integer, primary_key=True)
    goal_amount  = db.Column(db.Integer, nullable=False)   # cents / pennies
    @property
    def amount(self):
        return self.goal_amount
    @property
    def amount(self):
        return self.goal_amount
    @property
    def amount(self):
        return self.goal_amount
    total        = db.Column(db.Integer, default=0)        # raised so far
    active       = db.Column(db.Boolean, default=True)     # ← new field
