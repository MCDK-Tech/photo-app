from flask import Response, request
from flask_restful import Resource
import json
from flask_jwt_extended import current_user, jwt_required

def get_path():
    return request.host_url + 'api/posts/'

class ProfileDetailEndpoint(Resource):


    @jwt_required()
    def get(self):
        
        return Response(json.dumps(current_user.to_dict()), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        ProfileDetailEndpoint, 
        '/api/profile', 
        '/api/profile/', 

    )
