from flask import request


def handle_request_type(func):
    def func_wrapper(*args, **kwargs):
        # FIXME: Potential security issues
        return func(*args, **kwargs)[request.method.lower()]()

    return func_wrapper