from flask import Response
from flask_restful import Resource
from models import Story
from . import get_authorized_user_ids
import json
from flask_jwt_extended import current_user, jwt_required

class StoriesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @jwt_required()
    def get(self):
        stories = Story.query.filter(Story.user_id.in_(get_authorized_user_ids(self.current_user)))
        return Response(json.dumps([model.to_dict() for model in stories]), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        StoriesListEndpoint, 
        '/api/stories', 
        '/api/stories/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
