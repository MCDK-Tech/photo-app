from flask import Response, request
from flask_restful import Resource
from models import User
from . import get_authorized_user_ids
import json
from flask_jwt_extended import current_user, jwt_required

class SuggestionsListEndpoint(Resource):

    
    @jwt_required()
    def get(self):
        suggestions = User.query.filter(~User.id.in_(get_authorized_user_ids(current_user))).limit(7)
        return Response(json.dumps([model.to_dict() for model in suggestions]), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        SuggestionsListEndpoint, 
        '/api/suggestions', 
        '/api/suggestions/', 

    )


