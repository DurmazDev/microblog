from mongoengine import fields, Document, EmbeddedDocument
from datetime import datetime


class AuthorEmbedded(EmbeddedDocument):
    id = fields.ObjectIdField(required=True)
    name = fields.StringField(required=True)


class CommentModel(Document):
    author = fields.EmbeddedDocumentField(AuthorEmbedded, required=True)
    post_id = fields.ObjectIdField(required=True)
    content = fields.StringField(reuqired=True, max_length=1024)  # 1024 is random value
    created_at = fields.DateTimeField(required=True)
    updated_at = fields.DateTimeField(required=True)
    deleted_at = fields.DateTimeField(required=False, default=None)

    class Meta:
        exclude = ["deleted_at"]

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(CommentModel, self).save(*args, **kwargs)

    def soft_delete(self):
        if not self.deleted_at:
            self.deleted_at = datetime.now()
            self.save()
