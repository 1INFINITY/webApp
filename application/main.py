import datetime

from flask import Blueprint, flash, Flask, render_template, url_for, request, redirect
from flask_login import login_required, current_user
from application.models import Article, Comment
from application import db

main = Blueprint('main', __name__)


@main.route('/hello')
@login_required
def hello():
    return render_template("hello.html", name=current_user.name)


@main.route('/')
def index():
    return render_template("index.html")


@main.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date).all()
    return render_template("posts.html", articles=articles)


@main.route('/posts/<int:id>')
def post_details(id):
    article = Article.query.get(id)
    return render_template("post_details.html", article=article)


@main.route('/posts/<int:id>/delete')
@login_required
def post_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        flash("Something went wrong while deleting")
        return redirect(f'/posts/{id}')


@main.route('/posts/<int:id>/update', methods=['POST', 'GET'])
@login_required
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/posts')
        except:
            flash("Something went wrong while editng")
            return redirect(f'/posts/{id}')
    else:
        return render_template("post_update.html", article=article)


@main.route('/create-article', methods=['POST', 'GET'])
@login_required
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text, user_id=current_user.id)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            flash("Something went wrong while add post")
            return redirect('/create-article')
    else:
        return render_template("create_article.html")


@main.route('/posts/<int:id>/comment/add', methods=['POST', 'GET'])
@login_required
def create_comment(id):
    if request.method == 'POST':
        message = request.form['comment']
        user_id = current_user.id
        article_id = id
        comment = Comment(message=message, user_id=user_id, article_id=article_id)
        try:
            db.session.add(comment)
            db.session.commit()
        except:
            flash("Something went wrong when adding a comment")
    return redirect(f'/posts/{id}')


@main.route('/posts/<int:id>/comment/<int:comment_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_comment(id, comment_id):
    comment = Comment.query.get_or_404(comment_id)
    try:
        db.session.delete(comment)
        db.session.commit()
        return redirect(f'/posts/{id}')
    except:
        flash("Something went wrong when deleting a comment")
    return redirect(f'/posts/{id}')


