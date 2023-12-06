from mongoengine import fields, Document


class VoteModel(Document):
    author = fields.ObjectIdField(required=True)
    post_id = fields.ObjectIdField(required=True)
    vote_value = fields.IntField(required=True)
    # In feed, upvote moves post point 1 up, downvote moves post point 2-3 down...
