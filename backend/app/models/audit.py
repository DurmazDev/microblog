from mongoengine import Document, fields
from datetime import datetime

# Event ID's:
# 0: Unauthorized request
# 1: User events
# 2: Authentication failure
# 3: System error
# 4: 2FA enabled/disabled
# 5: Any data update events


class AuditModel(Document):
    event_id = fields.IntField(required=True)
    request_ip = fields.StringField(required=True, default=None, null=True)
    request_user_agent = fields.StringField(required=True, default=None, null=True)
    description = fields.StringField(required=True)
    created_at = fields.DateTimeField(required=True)
    updated_at = fields.DateTimeField(required=True)
    deleted_at = fields.DateTimeField(required=False, default=None)

    class Meta:
        exclude = ["deleted_at"]

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(AuditModel, self).save(*args, **kwargs)

    def soft_delete(self):
        if not self.deleted_at:
            self.deleted_at = datetime.now()
            self.save()
