from flask import Blueprint, render_template, request, session, flash, redirect, jsonify, url_for
from models.models import Post, Usuario, Likes, Follower, db
from services.time_created import time_since_creation


homeView = Blueprint('homeView', __name__)


@homeView.route("/", methods=["GET", "POST"])
def home():
    if "user_id" not in session:
        return redirect(url_for("loginView.login"))

    user_id = session["user_id"]

    if request.method == "POST":
        content = request.form.get("content")
        if not content or len(content.strip()) == 0:
            flash("Postagem vazia.", "error")
            return redirect(url_for("homeView.home"))
        
        try:
            Post.create_post(user_id, content)
            flash("Postagem criada com sucesso!", "success")
            return redirect(url_for("homeView.home"))
        except Exception as e:
            flash(f"Erro ao criar postagem: {e}", "error")

    posts = Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).all()

    liked_posts_id = {like.post_id for like in Likes.query.filter_by(user_id=user_id).all()}

    posts_data = [
        {
            "post_id": post.id,
            "user_id": post.user_id,
            "user_account": post.usuario.user_account,
            "content": post.content,
            "created_at": post.created_at,
            "likes": post.likes,
            "liked": post.id in liked_posts_id
        }
        for post in posts
    ]

    return render_template("home.html", posts=posts_data, user_id=user_id, time_since_creation=time_since_creation)


@homeView.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('loginView.login'))


@homeView.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    logged_in_user_id = session["user_id"]

    user = Usuario.query.get(user_id)
    if not user:
        flash("Usuario não encontrado", "error")
        return redirect(url_for("homeView.home"))
    
    followers_count = Follower.query.filter_by(followed_user_id=user_id).count()
    following_count = Follower.query.filter_by(follower_user_id=user_id).count()

    num_posts = Post.query.filter_by(user_id=user_id).count()

    is_following = Follower.query.filter_by(follower_user_id=logged_in_user_id, followed_user_id=user.id).first() is not None

    posts = Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).all()

    liked_posts_id = {like.post_id for like in Likes.query.filter_by(user_id=logged_in_user_id).all()}

    posts_data = [
        {
            "post_id": post.id,
            "content": post.content,
            "created_at": post.created_at,
            "time_since": time_since_creation(post.created_at),
            "likes": post.likes,
            "liked": post.id in liked_posts_id

        }
        for post in posts
    ]
    

    return render_template(
        'profile.html',
        user=user,
        posts=posts_data,
        num_posts=num_posts,
        time_since_creation=time_since_creation,
        followers_count=followers_count,
        following_count=following_count,
        is_following=is_following,
        logged_in_user_id=session['user_id']  
)


@homeView.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = Usuario.query.get(user_id)


    if request.method == 'POST':
        new_user_account = request.form.get('user_account', '').strip()
        new_user_name = request.form.get('user_name', '').strip()
        new_bio = request.form.get('bio', '').strip()

        if ' ' in new_user_account:
            flash("Nome de usuario invalido.", "error")
            return redirect(url_for('homeView.edit_profile'))

        if new_user_account or new_user_name or new_bio:
            user.user_account = new_user_account or user.user_account
            user.user_name = new_user_name or user.user_name
            user.bio = new_bio or user.bio
            db.session.commit()
            return redirect(url_for('homeView.profile', user_id=user_id))
    
    bio = user.bio.strip() if user.bio else ''
    
    return render_template('edit_profile.html',
                            user_account=user.user_account,
                            user_name=user.user_name,
                            bio=user.bio if user.bio else "") 