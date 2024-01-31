from functools import wraps
from flask_smorest import abort
from flask_jwt_extended import get_jwt, get_jwt_identity
from flask_jwt_extended import verify_jwt_in_request


def role_required(role_list: list):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] in role_list:
                return fn(*args, **kwargs)
            else:
                abort(403, message="Permission not granted!")

        return decorator

    return wrapper


def status_required(status_list: list):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["ban_status"] in status_list:
                return fn(*args, **kwargs)
            else:
                abort(403, message="Permission not granted!")

        return decorator

    return wrapper
