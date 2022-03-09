from models import User
import flask_jwt_extended
from flask import Response, request
from flask_restful import Resource
import json
from datetime import timezone, datetime, timedelta


class AccessTokenEndpoint(Resource):

    def post(self):
        body = request.get_json() or {}
        username = body.get('username')
        password = body.get('password')
        user = User.query.filter_by(username = username).first()
        if user is None:
            return Response(json.dumps({ 
                    "No user"
                }), mimetype="application/json", status=401)
        if user.check_password(password):
            access_token = flask_jwt_extended.create_access_token(user.id)
            refresh_token = flask_jwt_extended.create_refresh_token(user.id)
            return Response(json.dumps({ 
            "access_token": access_token, 
            "refresh_token": refresh_token
            }), mimetype="application/json", status=200)
        else:
            return Response(json.dumps({ 
                    "access_token": "new access token goes here"
                }), mimetype="application/json", status=401)

        # check username and log in credentials. If valid, return tokens
        

class RefreshTokenEndpoint(Resource):
    
    def post(self):

        body = request.get_json() or {}
        refresh_token = body.get('refresh_token')
        user = User.query.filter_by(refresh_token = refresh_token).first()
        if user is None:
            return Response(json.dumps({ 
                    "no refresh_token"
                }), mimetype="application/json", status=400)
        # print(refresh_token)
        '''
        https://flask-jwt-extended.readthedocs.io/en/latest/refreshing_tokens/
        Hint: To decode the refresh token and see if it expired:
        '''
        try:
            decoded_token = flask_jwt_extended.decode_token(refresh_token)
            exp_timestamp = decoded_token.get("exp")
            current_timestamp = datetime.timestamp(datetime.now(timezone.utc))
        except:
            return Response(json.dumps({ 
                "message": "Invalid refresh_token={0}. Could not decode.".format(refresh_token)
            }), mimetype="application/json", status=400)
        if exp_timestamp > current_timestamp:
            return Response(json.dumps({ 
                    "access_token": "new access token goes here"
                }), mimetype="application/json", status=200)
        else:
            return Response(json.dumps({ 
                    "message": "refresh_token has expired"
                }), mimetype="application/json", status=401)



def initialize_routes(api):
    api.add_resource(
        AccessTokenEndpoint, 
        '/api/token', '/api/token/'
    )

    api.add_resource(
        RefreshTokenEndpoint, 
        '/api/token/refresh', '/api/token/refresh/'
    )