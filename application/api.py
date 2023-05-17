from flask import Blueprint, make_response, jsonify, abort

from application.models import User, Comment, Article

api = Blueprint('api', __name__)


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@api.route('/api/comments')
def get_all_comments():
    comments = Comment.query.all()
    if not comments or len(comments) == 0:
        abort(404)
    return jsonify(
        list(
            map(
                Comment.to_dict,
                comments
            )
        )
    )


@api.route('/api/comments/<int:id>')
def get_comment_by_id(id):
    comment = Comment.query.filter_by(id=id).first()
    if not comment:
        abort(404)
    return jsonify(comment.to_dict())


@api.route('/api/users/<string:name>')
def get_user_by_name(name):
    user = User.query.filter_by(name=name).first()
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@api.route('/api/users')
def get_all_users():
    users = User.query.all()
    if not users or len(users) == 0:
        abort(404)
    return jsonify(
        list(
            map(
                User.to_dict,
                users
            )
        )
    )


@api.route('/api/users/<int:id>')
def get_user_by_id(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        abort(404)
    return jsonify(user.to_dict())

@api.route('/api/posts')
def get_all_posts():
    posts = Article.query.all()
    if not posts or len(posts) == 0:
        abort(404)
    return jsonify(
        list(
            map(
                Article.to_dict,
                posts
            )
        )
    )

@api.route('/api/posts/<int:id>')
def get_post_by_id(id):
    post = Article.query.filter_by(id=id).first()
    if not post:
        abort(404)
    return jsonify(post.to_dict())
