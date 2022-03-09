import string
from flask import Response, request
from flask_restful import Resource
from . import can_view_post
import json
from models import db, Comment, Post
from my_decorators import is_valid_id, is_valid_post_int, user_can_view_post_id
from flask_jwt_extended import current_user, jwt_required

class CommentListEndpoint(Resource):

    @jwt_required()
    @is_valid_post_int
    @user_can_view_post_id
    def post(self):
        body = request.get_json()
        id = body.get('post_id')
        text = body.get('text')
        if not text:
            return Response(json.dumps({'message': 'no text provided'}), mimetype="application/json", status = 400)
        comment = Comment(str(text), current_user.id, id)
        # these two lines save ("commit") the new record to the database:
        db.session.add(comment)
        db.session.commit()
        return Response(json.dumps(comment.to_dict()), mimetype="application/json", status=201)


class CommentDetailEndpoint(Resource):

    @jwt_required()
    @is_valid_id   
    def delete(self, id):
        comment = Comment.query.get(id)
        if not comment:
            return Response(json.dumps({'message': 'id not in database' }), mimetype="application/json", status=404)
        elif comment.user_id != current_user.id:
            return Response(json.dumps({'message': 'You did not create bookmark id={0}'.format(id)}), mimetype="application/json", status=404)
        
        Comment.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
            'message': 'Bookmark {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        CommentListEndpoint, 
        '/api/comments', 
        '/api/comments/',

    )
    api.add_resource(
        CommentDetailEndpoint, 
        '/api/comments/<id>', 
        '/api/comments/<id>',
    )
