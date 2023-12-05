from mongoengine import Document, fields
from bson import ObjectId
from datetime import datetime
from app.config import ALLOWED_TAGS, ALLOWED_ATTRIBUTES, DOMAIN_ROOT
from app.models.comment import CommentModel, VoteEmbedded
from random import randint
import bleach
import re


class PostModel(Document):
    title = fields.StringField(required=True)
    author = fields.ObjectIdField(required=True)
    content = fields.StringField(required=True)
    vote = fields.EmbeddedDocumentField(
        document_type=VoteEmbedded, default=VoteEmbedded
    )
    comments = fields.ListField(fields.ObjectIdField(), default=[])
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
        return "http://" + DOMAIN_ROOT + "/post/" + endpoint

    def soft_delete(self):
        if not self.deleted_at:
            self.deleted_at = datetime.now()
            self.save()

    @classmethod
    def create(cls, title: str, author_id: ObjectId, content: str):
        title = bleach.clean(
            title,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
        )
        content = bleach.clean(
            content,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
        )
        return cls(title=title, author=author_id, content=content).save()

    @classmethod
    def update(cls, post_id, update_values):
        post = cls.objects.filter(id=post_id).first()
        if not post:
            return None

        for key, value in update_values.items():
            setattr(post, key, value)
        post.save()

        return post

    @classmethod
    def get_by_id(cls, post_id: ObjectId):
        post = cls.objects.filter(id=post_id, deleted_at=None).first()
        return post if post else None

    @classmethod
    def get_by_url(cls, url: str):
        post = cls.objects.filter(url=url, deleted_at=None).first()
        return post if post else None

    @classmethod
    def get_user_posts(cls, user_id: ObjectId, excluded_fields: list = None):
        posts = cls.objects.filter(author=user_id, deleted_at=None).order_by(
            "-updated_at"
        )
        if excluded_fields:
            posts.exclude(*excluded_fields)

        return posts if posts else None
