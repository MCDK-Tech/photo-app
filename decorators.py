import flask_jwt_extended
from flask import redirect,request,Response
import json

def jwt_or_login(view_function):
    def wrapper(*args, **kwargs):
        try:
            flask_jwt_extended.verify_jwt_in_request()
            return view_function(*args, **kwargs)
        except:
            return redirect('/login', code=302)
            
    # https://stackoverflow.com/questions/17256602/assertionerror-view-function-mapping-is-overwriting-an-existing-endpoint-functi
    wrapper.__name__ = view_function.__name__
    return wrapper 

def _id_is_valid(self, func, key, *args, **kwargs):
    try:
        body = request.get_json()
        # if int parse is successful, then id is valid it:
        int(kwargs.get(key) or body.get(key))
    except:
        return Response(
            json.dumps({'message': 'Invalid {0}={1}'.format(key, kwargs.get(key))}), 
            mimetype="application/json", 
            status=400
        )
    return func(self, *args, **kwargs)


def id_is_valid(func):
    def wrapper(self, *args, **kwargs):
        return _id_is_valid(self, func, 'id', *args, **kwargs)
    return wrapper

def post_id_is_valid(func):
    def wrapper(self, *args, **kwargs):
        return _id_is_valid(self, func, 'post_id', *args, **kwargs)
    return wrapper
