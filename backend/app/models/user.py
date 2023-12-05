from mongoengine import Document, fields
from bcrypt import hashpw, gensalt
from bson import ObjectId
from datetime import datetime
from app.models.post import PostModel


class UserModel(Document):
    name = fields.StringField(required=True)
    email = fields.EmailField(required=True)
    password = fields.StringField(required=True)
    created_at = fields.DateTimeField(required=True)
    updated_at = fields.DateTimeField(required=True)
    deleted_at = fields.DateTimeField(required=False, default=None)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(UserModel, self).save(*args, **kwargs)

    def soft_delete(self):
        if not self.deleted_at:
            self.deleted_at = datetime.now()
            # PostModel.objects.filter(author=self.id).soft_delete(many=True)
            # TODO(ahmet): Posts, likes, comments needs to be updated after deletion.
            self.save()

    @classmethod
    def get_by_id(cls, user_id: ObjectId):
        user = cls.objects.filter(id=user_id, deleted_at=None).first()
        return user if user else None

    @classmethod
    def get_by_email(cls, email: str):
        user = cls.objects.filter(email=email, deleted_at=None).first()
        return user if user else None

    @classmethod
    def create(cls, name: str, email: str, password: str):
        return cls(
            name=name,
            email=email,
            password=hashpw(password.encode("utf-8"), gensalt(rounds=12)),
        ).save()

    @classmethod
    def update(cls, user_id, update_values):
        user = cls.objects.filter(id=user_id).first()
        if not user:
            return None

        for key, value in update_values.items():
            setattr(user, key, value)
        user.save()

        return user
