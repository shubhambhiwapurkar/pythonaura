from mongoengine import Document, EmbeddedDocument, fields, ReferenceField
from datetime import datetime

class Content(EmbeddedDocument):
    horoscope = fields.StringField(required=True)
    guidance = fields.StringField(required=True)

class DailyContent(Document):
    user = ReferenceField('User', required=True)
    date = fields.DateField(required=True, default=datetime.utcnow)
    content = fields.EmbeddedDocumentField(Content, required=True)
    type = fields.StringField(required=True, default="personalized_reading")
    read_status = fields.BooleanField(default=False)
    created_at = fields.DateTimeField(default=datetime.utcnow)