from flask import Response
from flask_restful import Resource
from models import LikePost, db, like_post, Post
import json
from . import can_view_post, get_authorized_user_ids
from my_decorators import is_valid_id, is_valid_post_int, user_can_view_post_id, id_is_valid

class PostLikesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def post(self, post_id):
        try:
            post_id= int(post_id)
        except:
            response_obj = {
                'message': 'id is not an int'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)

        likes = Post.query.get(post_id)

        if not likes:
            return Response(json.dumps({'message': 'id not in database' }), mimetype="application/json", status=404)
        elif likes.user_id not in get_authorized_user_ids(self.current_user):
            return Response(json.dumps({'message': 'You did not create likes id={0}'.format(id)}), mimetype="application/json", status=404)

        try: 
            likes = LikePost(self.current_user.id, post_id)
            db.session.add(likes)
            db.session.commit()
        except:
            return Response(json.dumps({'message': 'post already liked' }), mimetype="application/json", status=400)


        
            
        
        return Response(json.dumps(likes.to_dict()), mimetype="application/json", status=201)


class PostLikesDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    
    def delete(self, post_id, id):
        try:
            id= int(id)
        except:
            response_obj = {
                'message': 'id is not an int'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        likes = LikePost.query.get(id)
        if not likes:
            return Response(json.dumps({'message': 'id not in database' }), mimetype="application/json", status=404)
        elif likes.user_id != self.current_user.id:
            return Response(json.dumps({'message': 'You did not create likes id={0}'.format(id)}), mimetype="application/json", status=404)
    
            
        LikePost.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
            'message': 'Like {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        PostLikesListEndpoint, 
        '/api/posts/<post_id>/likes', 
        '/api/posts/<post_id>/likes/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        PostLikesDetailEndpoint, 
        '/api/posts/<post_id>/likes/<id>', 
        '/api/posts/<post_id>/likes/<id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
