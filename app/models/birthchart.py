from datetime import datetime
from mongoengine import Document, EmbeddedDocument, ReferenceField, DictField, DateTimeField, StringField, FloatField, EmbeddedDocumentField

class BirthData(EmbeddedDocument):
    date = DateTimeField(required=True)
    time = StringField(required=True)
    city = StringField(required=True)
    state = StringField(required=True)
    country = StringField(required=True)
    latitude = FloatField(required=True)
    longitude = FloatField(required=True)
    timezone = StringField(required=True)

class ChartData(EmbeddedDocument):
    ascendant = StringField(required=True)
    sun_sign = StringField(required=True)
    moon_sign = StringField(required=True)
    planets = DictField(required=True)
    houses = DictField(required=True)
    aspects = DictField(required=True)

class BirthChart(Document):
    user = ReferenceField('User', required=True)
    birth_data = EmbeddedDocumentField(BirthData, required=True)
    chart_data = EmbeddedDocumentField(ChartData, required=True)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'birth_charts',
        'indexes': [
            'user',
            'created_at'
        ]
    }
