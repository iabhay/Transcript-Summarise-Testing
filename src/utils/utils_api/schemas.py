from marshmallow import Schema, fields, validate
from config.regex_patterns import Patterns


class UserSchema(Schema):
    username = fields.Str(
        required=True, validate=validate.Regexp(Patterns.USERNAME_PATTERN)
    )
    password = fields.Str(
        required=True, validate=validate.Regexp(Patterns.PASSWORD_PATTERN)
    )


class UrlInputSchema(Schema):
    youtube_url = fields.Str(
        required=True, validate=validate.Regexp(Patterns.YOUTUBE_PATTERN)
    )


class PremiumListSchema(Schema):
    youtube_url = fields.Str(
        required=True, validate=validate.Regexp(Patterns.YOUTUBE_PATTERN)
    )
    username = fields.Str(
        required=True, validate=validate.Regexp(Patterns.USERNAME_PATTERN)
    )


class UserMessageSchema(Schema):
    description = fields.Str(required=True)
