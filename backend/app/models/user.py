from mongoengine import Document, fields
from datetime import datetime
from app.models.post import PostModel
from app.config import APP_NAME
import pyotp


class UserModel(Document):
    name = fields.StringField(required=True)
    email = fields.EmailField(required=True, unique=True)
    password = fields.StringField(required=True)
    is_2fa_enabled = fields.BooleanField(required=True, default=False, null=False)
    secret_token_2fa = fields.StringField(required=False, default=None)
    created_at = fields.DateTimeField(required=True)
    updated_at = fields.DateTimeField(required=True)
    deleted_at = fields.DateTimeField(required=False, default=None)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(UserModel, self).save(*args, **kwargs)

    def set_2fa_secret_token(self):
        if self.is_2fa_enabled:
            return self.secret_token_2fa
        self.is_2fa_enabled = True
        self.secret_token_2fa = pyotp.random_base32()
        self.save()
        return self.secret_token_2fa

    def get_authentication_setup_uri(self):
        return pyotp.totp.TOTP(self.secret_token_2fa).provisioning_uri(
            name=self.name, issuer_name=APP_NAME
        )

    def is_otp_valid(self, user_otp):
        totp = pyotp.parse_uri(self.get_authentication_setup_uri())
        return totp.verify(user_otp)

    def soft_delete(self):
        if not self.deleted_at:
            self.deleted_at = datetime.now()
            PostModel.objects.filter(author=self.id).soft_delete(many=True)
            self.save()


class UserFollowModel(Document):
    follower_id = fields.StringField(required=True)
    followee_id = fields.StringField(required=True)
    created_at = fields.DateTimeField(required=True)
    deleted_at = fields.DateTimeField(required=False, default=None)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        return super(UserFollowModel, self).save(*args, **kwargs)

    def soft_delete(self):
        if not self.deleted_at:
            self.deleted_at = datetime.now()
            self.save()
