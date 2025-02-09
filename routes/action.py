from flask import Blueprint, render_template, request, session, flash, redirect, jsonify, url_for
from models.models import Usuario, Post, Likes, Follower, db

actionView = Blueprint('actionView', __name__)



@actionView.route("/follow_unfollow/<int:user_id>", methods=["POST"])
def follow_unfollow(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        follower_user_id = session['user_id']

        existing_follow = Follower.query.filter_by(
            follower_user_id=follower_user_id, followed_user_id=user_id).first()
        
        if existing_follow:
            db.session.delete(existing_follow)
        else:
            new_follow = Follower(follower_user_id=follower_user_id, followed_user_id=user_id)
            db.session.add(new_follow)

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        flash("Erro. Tente novamente mais tarde")
        

@actionView.route("/like_post/<int:post_id>", methods=["POST"])
def like_post(post_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("loginView.login"))
    
    try:
        post = Post.query.get(post_id)
        
        like = Likes.query.filter_by(post_id=post_id, user_id=user_id).first()
        liked = False
        if like:
            db.session.delete(like)
            post.likes -= 1
        else:
            like = Likes(post_id=post_id, user_id=user_id)
            db.session.add(like)
            post.likes += 1
            liked = True

        db.session.commit()

        return jsonify({"likeCount": post.likes, "liked": liked})
    
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao curtir: {e}")
        return jsonify({"error": str(e)}), 500


@actionView.route("/delete_post/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    if 'user_id' not in session:
        return redirect(url_for('loginView.login'))
    
    user_id = session['user_id']

    post = Post.query.get(post_id)
    
    if post and post.user_id == user_id:
        Post.delete_post(post_id, user_id)
        return jsonify({"success": True, "message": "Postagem excluída com sucesso!"})
    else:
        return jsonify({"success": False, "message": "Erro: você não tem permissão para excluir este post."}), 400


@actionView.route("/edit_post/<int:post_id>", methods=["PUT"])
def edit_post(post_id):
    
    if "user_id" not in session:
        return redirect(url_for("loginView.login"))

    post = Post.query.get(post_id)
    if not post:
        return jsonify({"success": False, "message": "Post não encontrado."}), 404

    data = request.get_json()
    new_content = data.get('content', '').strip()

    if new_content:
        post.content = new_content
        db.session.commit()
        return jsonify({"success": True, "content": post.content})

    return jsonify({"success": False, "message": "Conteúdo vazio."}), 400
