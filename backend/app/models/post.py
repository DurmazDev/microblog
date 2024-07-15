from mongoengine import Document, fields
from datetime import datetime
from random import randint
from app.config import FRONTEND_ROOT
import re


class PostModel(Document):
    title = fields.StringField(required=True)
    author = fields.ObjectIdField(required=True)
    content = fields.StringField(required=True)
    vote = fields.IntField(default=0, required=True)
    comments = fields.ListField(fields.ObjectIdField(), default=[])
    tags = fields.ListField(fields.ObjectIdField(), default=[])
    url = fields.StringField(required=True)
    created_at = fields.DateTimeField(required=True)
    updated_at = fields.DateTimeField(required=True)
    deleted_at = fields.DateTimeField(required=False, default=None)

    class Meta:
        exclude = ["deleted_at"]

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
            self.url = self.create_url(self.title, self.created_at)
        self.updated_at = datetime.now()
        return super(PostModel, self).save(*args, **kwargs)

    def create_url(self, title, created_at):
        raw_url = f"{'-'.join(title.lower().split())}-{created_at.strftime('%Y%m%d')}{randint(1000, 9999)}"
        endpoint = re.sub(r"[^a-zA-Z0-9\-]", "", raw_url)
        return "http://" + FRONTEND_ROOT + "/post/" + endpoint

    def soft_delete(self):
        if not self.deleted_at:
            self.deleted_at = datetime.now()
            self.save()
