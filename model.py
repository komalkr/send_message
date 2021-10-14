import uuid
from sqlalchemy.dialects.postgresql import UUID
from app import db

class Intent(db.Model):
    __tablename__ = 'intent'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    senderPhone = db.Column(db.String())
    receiverPhone = db.Column(db.String())
    messageText = db.Column(db.String())
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4)

    def __init__(self, senderPhone, receiverPhone, messageText):
        self.senderPhone = senderPhone
        self.receiverPhone = receiverPhone
        self.messageText = messageText

    def __repr__(self):
        return '<id {}>'.format(self.id)