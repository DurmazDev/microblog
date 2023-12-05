from mongoengine import fields, Document
from bson import ObjectId
from datetime import datetime


class VoteEmbedded(fields.EmbeddedDocument):
    up = fields.IntField(required=True, default=0, min_value=0)
    down = fields.IntField(required=True, default=0, min_value=0)
    # In feed, upvote moves post point 1 up, downvote moves post point 2-3 down...


class CommentModel(Document):
    author = fields.ObjectIdField(required=True)
    post_id = fields.ObjectIdField(required=True)
    content = fields.StringField(reuqired=True, max_length=1024)  # 1024 is random value
    vote = fields.EmbeddedDocumentField(
        document_type=VoteEmbedded, default=VoteEmbedded
    )
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

    @classmethod
    def create_comment(cls, post_id: ObjectId, author: ObjectId, content: str):
        comment = CommentModel(post_id=post_id, author=author, content=content).save()
        return comment

    # WARN(ahmet): this method is nesting too much...
    @classmethod
    def get_by_id(cls, comment_id: ObjectId):
        post = cls.objects.filter(id=comment_id, deleted_at=None).first()
        return post if post else None
