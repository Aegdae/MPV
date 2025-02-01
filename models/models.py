from application import db, bcrypt
from datetime import datetime



class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), unique=True, nullable=False)
    user_password = db.Column(db.String(255), nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    user_account = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    liked_post = db.Column(db.ARRAY(db.Integer))
    bio = db.Column(db.Text)
    reset_code = db.Column(db.String(6), nullable=True)
    reset_code_created_at = db.Column(db.DateTime, nullable=True)
    posts = db.relationship('Post', back_populates='usuario')

    ## Login ##
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(user_email=email).first()
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(user_account=username).first()
    
    @staticmethod
    def hash_password(password):
        return bcrypt.generate_password_hash(password).decode("utf-8")
    
    def verify_password(self, password):
        return bcrypt.check_password_hash(self.user_password, password)
    


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    likes = db.Column(db.Integer, default=0)
    usuario = db.relationship('Usuario', back_populates='posts')

    @classmethod
    def create_post(cls, user_id, content):
        post = cls(user_id=user_id, content=content)
        db.session.add(post)
        db.session.commit()
        return post

    @classmethod
    def get_posts(cls, user_id):
        liked_posts = Usuario.query.get(user_id).liked_post
        liked_posts = liked_posts.split(",") if liked_posts else []
        posts = cls.query.order_by(cls.created_at.desc()).all()
        posts_data = []
        for post in posts:
            posts_data.append({
                'post_id': post.id,
                'content': post.content,
                'created_at':post.created_at,
                'user_account': post.usuario.user_account,
                'likes': post.likes,
                'user_id': post.user_id,
                'liked': str(post.id) in liked_posts
            })
        return posts_data

    @classmethod
    def delete_post(cls, post_id, user_id):
        """Deleta um post e seus comentarios, se o usuário for o dono"""
        post = cls.query.filter_by(id=post_id, user_id=user_id).first()

        if not post:
            return False
        
        Likes.query.filter_by(post_id=post_id).delete()

        db.session.delete(post)
        db.session.commit()

class Likes(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True, nullable=False)


class Follower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    followed_user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    follower = db.relationship('Usuario', foreign_keys=[follower_user_id], backref='following')
    followed = db.relationship('Usuario', foreign_keys=[followed_user_id], backref='followers')