from flask import Response, request
from flask_restful import Resource
from models import Following, User, db, following
import json

from tests.utils import get_authorized_user_ids
from my_decorators import is_valid_id, is_valid_post_int, user_can_view_post_id, id_is_valid

def get_path():
    return request.host_url + 'api/posts/'

class FollowingListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):

        following = Following.query.filter_by(user_id=self.current_user.id)
        return Response(json.dumps([model.to_dict_following() for model in following]), mimetype="application/json", status=200)
    
    
    def post(self):
        body = request.get_json()
        user_id = body.get('user_id')
        print(user_id)
        if not user_id:
            response_obj = {
                'message': 'no user_id'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        try:
            user_id= int(user_id)
        except:
            response_obj = {
                'message': 'You don\'t have access to id={0}'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        user = User.query.get(user_id)
        if not user:
            return Response(
                json.dumps({
                    'message': 'User id={0} does not exist'.format(user_id)
                }), mimetype="application/json", status=404)
        try:
            following = Following(self.current_user.id, user_id)
            db.session.add(following)
            db.session.commit() 
        except Exception:
            import sys
            print(sys.exc_info()[1])
            return Response(
                json.dumps({
                    'message': 'Database Insert error. Are you already following user={0}? Please see the log files.'.format(user_id)}
                ), 
                mimetype="application/json", 
                status=400
            ) 
        return Response(json.dumps(following.to_dict_following()), mimetype="application/json", status=201)
        


class FollowingDetailEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    @is_valid_id   
    def delete(self, id):
        following = Following.query.get(id)
        if not following:
            return Response(json.dumps({'message': 'id not in database' }), mimetype="application/json", status=404)
        elif following.user_id != self.current_user.id:
            return Response(json.dumps({'message': 'You did not create following id={0}'.format(id)}), mimetype="application/json", status=404)
        
        Following.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
            'message': 'following {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        FollowingListEndpoint, 
        '/api/following', 
        '/api/following/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
    api.add_resource(
        FollowingDetailEndpoint, 
        '/api/following/<id>', 
        '/api/following/<id>/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
