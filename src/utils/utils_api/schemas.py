"""Module containing schemas used in request and response in routes"""

from marshmallow import Schema, fields, validate
from config.regex_patterns import Patterns


class UserSchema(Schema):
    """
    Class for defining User Schema having username and password properties
    ...
    Properties:
    username: fields.str -> validated using regex and also mandatory
    """

    username = fields.Str(
        required=True, validate=validate.Regexp(Patterns.USERNAME_PATTERN)
    )
    password = fields.Str(
        required=True, validate=validate.Regexp(Patterns.PASSWORD_PATTERN)
    )


class UrlInputSchema(Schema):
    """
    Class for defining Url Schema having youtube url property
    ...
    Properties:
    youtube_url: fields.str -> validated using regex and also mandatory
    """

    youtube_url = fields.Str(
        required=True, validate=validate.Regexp(Patterns.YOUTUBE_PATTERN)
    )


class PremiumListSchema(Schema):
    """
    Class for defining Premium List Schema having youtube url and username properties
    ...
    Properties:
    youtube_url: fields.str -> validated using regex and also mandatory
    username: fields.str -> validated using regex and also mandatory
    """

    youtube_url = fields.Str(
        required=True, validate=validate.Regexp(Patterns.YOUTUBE_PATTERN)
    )
    user_id = fields.Str(
        required=True, validate=validate.Regexp(Patterns.USERNAME_PATTERN)
    )


class UserMessageSchema(Schema):
    """
    Class for defining User message Schema having description property
    ...
    Properties:
    description: fields.str -> mandatory
    """

    description = fields.Str(required=True)
