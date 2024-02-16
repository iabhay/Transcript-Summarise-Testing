"""Module containing utility functions used throughout the project"""

import re


def password_validation(password: str) -> bool:
    """
    Method to validate password using regex
    Parameter -> password: str
    Return Type -> bool
    """
    pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,20}$"
    answer = re.match(pattern, password)
    if answer:
        return True
    else:
        return False


def username_validation(username: str) -> bool:
    """
    Method to validate username using regex
    Parameter -> username: str
    Return Type -> bool
    """
    pattern = "^([A-z0-9@_\-\.]{4,20})"
    answer = re.match(pattern, username)
    if answer:
        return True
    else:
        return False


def url_validation(url: str) -> bool:
    """
    Method to validate youtube url using regex
    Parameter -> url: str
    Return Type -> bool
    """
    pattern = "(https:\/\/)?(www.)?youtube.(com)\/watch\?v=[a-zA-Z0-9\-\_]{11}"
    answer = re.match(pattern, url)
    if answer:
        return True
    else:
        return False
