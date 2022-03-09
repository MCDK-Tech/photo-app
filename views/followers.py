from flask import Response, request
from flask_restful import Resource
from models import Following
import json
from flask_jwt_extended import current_user, jwt_required

def get_path():
    return request.host_url + 'api/posts/'

class FollowerListEndpoint(Resource):
    
    @jwt_required()
    def get(self):
        follower = Following.query.filter_by(following_id=current_user.id)
        return Response(json.dumps([model.to_dict_follower() for model in follower]), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        FollowerListEndpoint, 
        '/api/followers', 
        '/api/followers/', 
    )
