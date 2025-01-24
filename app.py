from flask import Flask, request, render_template, redirect, url_for, session, jsonify, flash
from flask_cors import CORS
from flask_sslify import SSLify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from psycopg2 import sql
from datetime import datetime
from dotenv import load_dotenv
import smtplib
import random
import bcrypt
import psycopg2
import os


load_dotenv(dotenv_path="env/db_config.env")
app = Flask(__name__)
sslify = SSLify(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'


CORS(app)

db_config =  {
    "dbname": os.getenv('DB_NAME'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD'),
    "host": os.getenv('DB_HOST'),
    "port": os.getenv('DB_PORT')
}



def time_since_creation(created_at):
            if isinstance(created_at, str): 
                created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            delta = now - created_at

            if delta.days > 0:
                if delta.days == 1:
                    return "1 dia atrás"
                return f"{delta.days} dias atrás"
            elif delta.seconds < 3600:
                minutes = delta.seconds // 60
                if minutes == 1:
                    return "1 minuto atrás"
                return f"{minutes} minutos atrás"
            elif delta.seconds < 86400:
                hours = delta.seconds // 3600
                if hours == 1:
                    return "1 hora atrás"
                return f"{hours} horas atrás"
            else:
                return "Agora mesmo"



def send_email(recipient_email, subject, body):
    sender_email = "jonnathasg@gmail.com"
    password = "mqbr ncdn alfi xoau"

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    message = MIMEMultipart()
    message["From"] = "MPV - Aplicativo <mpv@gmail.com>"
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit() 
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("Por favor, preencha todos os campos.", "error")
            return render_template("login.html"), 400

        try:
            connect = psycopg2.connect(**db_config)
            cursor = connect.cursor()

            query = sql.SQL("SELECT ID, USER_PASSWORD FROM usuarios WHERE USER_EMAIL = %s")
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
                session['user_id'] = user[0]
                return redirect(url_for("home"))
            else:
                flash("E-mail ou senha incorretos.", "error")
                return render_template("login.html"), 401

        except Exception as e:
            app.logger.error(f"Erro ao tentar logar: {e}")
            flash("Ocorreu um erro ao processar seu login. Tente novamente.", "error")
            return render_template("login.html"), 500

        finally:
            if cursor:
                cursor.close()
            if connect:
                connect.close()

    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        Email = request.form['email']
        Password = request.form['password']
        Name = request.form['name']
        Username = request.form['user']

        if not Email or not Password or not Name or not Username:
            return "Preencha todos os campos.", 400

        try:
            connect = psycopg2.connect(**db_config)
            cursor = connect.cursor()

            cursor.execute("SELECT COUNT(*) FROM USUARIOS WHERE LOWER(user_account) = LOWER(%s)", (Username,))
            username_exists = cursor.fetchone()[0] > 0

            if username_exists:
                flash("Nome de usuário já está em uso. Escolha outro.", "error")
                return render_template("register.html"), 400

            Hash_pass = bcrypt.hashpw(Password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            query = sql.SQL(
                "INSERT INTO usuarios (USER_EMAIL, USER_PASSWORD, USER_NAME, USER_ACCOUNT) VALUES (%s, %s, %s, %s) RETURNING ID"
            )

            cursor.execute(query, (Email, Hash_pass, Name, Username))
            user_id = cursor.fetchone()[0]
            connect.commit()
            session['user_id'] = user_id
            return redirect(url_for('login'))

        except Exception as e:
            return f"Erro ao criar conta {e}"

        finally:
            if cursor:
                cursor.close()
            if connect:
                connect.close()

    return render_template('register.html')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        if not email:
            flash("Por favor, insira seu e-mail.", "error")
            return render_template('forgot_password.html')

        try:
            connect = psycopg2.connect(**db_config)
            cursor = connect.cursor()
            cursor.execute("SELECT ID FROM USUARIOS WHERE USER_EMAIL = %s", (email,))
            user = cursor.fetchone()

            if not user:
                flash("E-mail não encontrado.", "error")
                return render_template('forgot_password.html')

            reset_code = str(random.randint(100000, 999999))

            cursor.execute("UPDATE USUARIOS SET RESET_CODE = %s WHERE USER_EMAIL = %s", (reset_code, email))
            connect.commit()

            subject = "Redefinição de Senha"
            body = f"Seu código para redefinição de senha é: {reset_code}"
            send_email(email, subject, body)

            flash("Código enviado para o seu e-mail.", "success")
            return redirect(url_for('reset_password'))

        except Exception as e:
            app.logger.error(f"Erro no envio de e-mail: {e}")
            flash("Erro ao processar solicitação. Tente novamente.", "error")
        finally:
            if cursor:
                cursor.close()
            if connect:
                connect.close()

    return render_template('forgot_password.html')


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        code = request.form.get('code')
        new_password = request.form.get('new_password')

        if not email or not code or not new_password:
            flash("Preencha todos os campos.", "error")
            return render_template('reset_password.html')

        try:
            connect = psycopg2.connect(**db_config)
            cursor = connect.cursor()
            cursor.execute("SELECT RESET_CODE FROM USUARIOS WHERE USER_EMAIL = %s", (email,))
            user = cursor.fetchone()

            if not user or user[0] != code:
                flash("Código inválido ou e-mail incorreto.", "error")
                return render_template('reset_password.html')

            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute("UPDATE USUARIOS SET USER_PASSWORD = %s, RESET_CODE = NULL WHERE USER_EMAIL = %s",
                           (hashed_password, email))
            connect.commit()

            flash("Senha redefinida com sucesso.", "success")
            return redirect(url_for('login'))

        except Exception as e:
            app.logger.error(f"Erro ao redefinir senha: {e}")
            flash("Erro ao processar redefinição. Tente novamente.", "error")
        finally:
            if cursor:
                cursor.close()
            if connect:
                connect.close()

    return render_template('reset_password.html')





@app.route("/", methods=["GET", "POST"])
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    if request.method == "POST":
        content = request.form.get("content")
        if not content:
            return "Postagem vazia", 400

        try:
            connect = psycopg2.connect(**db_config)
            cursor = connect.cursor()

            query = sql.SQL(
                "INSERT INTO POSTS (USER_ID, CONTENT) VALUES (%s, %s) RETURNING ID"
            )
            cursor.execute(query, (user_id, content))
            connect.commit()

            return redirect(url_for("home"))

        except Exception as e:
            return f"Erro ao criar postagem: {e}"

        finally:
            if cursor:
                cursor.close()
            if connect:
                connect.close()

    try:
        connect = psycopg2.connect(**db_config)
        cursor = connect.cursor()

        cursor.execute("SELECT LIKED_POSTS FROM USUARIOS WHERE ID = %s", (user_id,))
        liked_posts = cursor.fetchone()[0] or ""
        liked_post_ids = [int(pid) for pid in liked_posts.split(",") if pid]

        cursor.execute(
            """
            SELECT P.ID, P.CONTENT, P.CREATED_AT, U.USER_ACCOUNT, P.LIKES, P.USER_ID
            FROM POSTS P
            JOIN USUARIOS U ON P.USER_ID = U.ID
            ORDER BY P.CREATED_AT DESC
            """
        )
        posts = cursor.fetchall()  
        posts = [
            {
                'post_id': post[0],
                'content': post[1],
                'created_at': post[2],
                'user_account': post[3],
                'likes': post[4],
                'user_id': post[5],
                'liked': post[0] in liked_post_ids,
                'time_since_creation': time_since_creation(post[2])
            }
            for post in posts
        ]

    except Exception as e:
        return f"Erro ao recuperar postagens: {e}"

    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()

    return render_template("home.html", posts=posts, user_id=user_id)


@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        connect = psycopg2.connect(**db_config)
        cursor = connect.cursor()

        cursor.execute("SELECT ID, USER_NAME, USER_ACCOUNT, BIO FROM USUARIOS WHERE ID = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            return "Usuário não encontrado.", 404

        cursor.execute("SELECT COUNT(*) FROM FOLLOWERS WHERE FOLLOWED_USER_ID = %s", (user_id,))
        followers_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM FOLLOWERS WHERE FOLLOWER_USER_ID = %s", (user_id,))
        following_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM POSTS WHERE USER_ID = %s", (user_id,))
        num_posts = cursor.fetchone()[0]

        cursor.execute(""" 
            SELECT COUNT(*) FROM FOLLOWERS
            WHERE follower_user_id = %s AND followed_user_id = %s
        """, (session['user_id'], user_id))
        is_following = cursor.fetchone()[0] > 0

        cursor.execute(""" 
            SELECT p.id, p.content, p.created_at, 
           COALESCE(COUNT(l.post_id), 0) AS like_count
            FROM posts p
            LEFT JOIN likes l ON l.post_id = p.id
            WHERE p.user_id = %s
            GROUP BY p.id
            ORDER BY p.created_at DESC
        """, (user_id,))

        posts = cursor.fetchall()

        liked_post_ids = []
        cursor.execute(""" 
            SELECT post_id FROM likes WHERE user_id = %s
        """, (session['user_id'],))
        liked_posts = cursor.fetchall()
        liked_post_ids = [row[0] for row in liked_posts]

        posts = [
            post + (post[0] in liked_post_ids,) 
        for post in posts
        ]

        posts = [(post[0], post[1], post[2], post[3], time_since_creation(post[2]), post[4]) for post in posts]

    except Exception as e:
        return f"Erro ao carregar perfil: {e}"

    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()

    return render_template(
        'profile.html',
        user=user,
        posts=posts,
        num_posts=num_posts,
        followers_count=followers_count,
        following_count=following_count,
        is_following=is_following,
        logged_in_user_id=session['user_id']  
)


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    try:
        connect = psycopg2.connect(**db_config)
        cursor = connect.cursor()

        cursor.execute("""
            SELECT user_name, user_account, bio FROM usuarios WHERE id = %s
        """, (user_id,))
        user = cursor.fetchone()

        if user:
            user_name, user_account, bio = user
        else:
            user_name, user_account, bio = '', '', '' 

        if request.method == 'POST':
            new_user_account = request.form.get['user_account']
            new_user_name = request.form.get['user_name']
            new_bio = request.form.get['bio'].strip()

            cursor.execute("""
                UPDATE usuarios
                SET user_name = %s, user_account = %s, bio = %s
                WHERE id = %s
            """, (new_user_name, new_user_account, new_bio, user_id))
            connect.commit()

            return redirect(url_for('profile', user_id=user_id))

        return render_template('edit_profile.html', user_name=user_name, user_account=user_account, bio=bio)

    except Exception as e:
        return f"Erro ao editar perfil: {e}"

    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()







@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        user_name = request.form['user_name']
        user_account = request.form['user_account']
        bio = request.form['bio']

        try:
            connect = psycopg2.connect(**db_config)
            cursor = connect.cursor()

            cursor.execute("SELECT ID FROM USUARIOS WHERE LOWER(user_account) = LOWER(%s) AND ID != %s", (user_account, user_id))
            existing_user = cursor.fetchone()

            if existing_user:
                return "O nome de conta (user_account) já está em uso. Escolha outro.", 400

            cursor.execute("""
                UPDATE USUARIOS
                SET user_name = %s, user_account = %s, bio = %s
                WHERE ID = %s
            """, (user_name, user_account, bio, user_id))

            connect.commit()

        except Exception as e:
            return f"Erro ao atualizar perfil: {e}"
        finally:
            if cursor:
                cursor.close()
            if connect:
                connect.close()

        return redirect(url_for('profile', user_id=user_id))
    

    try:
        connect = psycopg2.connect(**db_config)
        cursor = connect.cursor()

        cursor.execute("SELECT user_name, user_account, bio FROM USUARIOS WHERE ID = %s", (user_id,))
        user_info = cursor.fetchone()

        if not user_info:
            return "Usuário não encontrado", 404

        user_name, user_account, bio = user_info

    except Exception as e:
        return f"Erro ao carregar informações do perfil: {e}"
    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()

    return render_template('edit_profile.html', user_name=user_name, user_account=user_account, bio=bio)




@app.route('/check_user_account', methods=['POST'])
def check_user_account():
    user_account = request.form.get('user_account')
    
    try:
        connect = psycopg2.connect(**db_config)
        cursor = connect.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM USUARIOS WHERE LOWER(user_account) = LOWER(%s)
        """, (user_account,))
        exists = cursor.fetchone()[0] > 0

        return jsonify({'exists': exists})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()




@app.route("/follow_unfollow/<int:user_id>", methods=["POST"])
def follow_unfollow(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        connect = psycopg2.connect(**db_config)
        cursor = connect.cursor()

        cursor.execute("""
            SELECT 1 FROM FOLLOWERS WHERE FOLLOWER_USER_ID = %s AND FOLLOWED_USER_ID = %s
        """, (session['user_id'], user_id))
        
        existing_follow = cursor.fetchone()

        if existing_follow:
            cursor.execute("""
                DELETE FROM FOLLOWERS WHERE FOLLOWER_USER_ID = %s AND FOLLOWED_USER_ID = %s
            """, (session['user_id'], user_id))
        else:
            cursor.execute("""
                INSERT INTO FOLLOWERS (FOLLOWER_USER_ID, FOLLOWED_USER_ID) VALUES (%s, %s)
            """, (session['user_id'], user_id))

        connect.commit()
        return redirect(url_for('profile', user_id=user_id))

    except Exception as e:
        return f"Erro ao seguir/deixar de seguir: {e}"

    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()



@app.route("/like_post/<int:post_id>", methods=["POST"])
def like_post(post_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    try:
        connect = psycopg2.connect(**db_config)
        cursor = connect.cursor()

        cursor.execute("SELECT LIKED_POSTS FROM USUARIOS WHERE ID = %s", (user_id,))
        liked_posts = cursor.fetchone()[0] or ""
        liked_post_ids = [int(pid) for pid in liked_posts.split(",") if pid]

        liked = False
        if post_id in liked_post_ids:
            liked_post_ids.remove(post_id)
            cursor.execute("UPDATE POSTS SET LIKES = COALESCE(LIKES, 0) - 1 WHERE ID = %s", (post_id,))
        else:
            liked_post_ids.append(post_id)
            cursor.execute("UPDATE POSTS SET LIKES = COALESCE(LIKES, 0) + 1 WHERE ID = %s", (post_id,))
            liked = True

        new_liked_posts = ",".join(map(str, liked_post_ids))
        cursor.execute("UPDATE USUARIOS SET LIKED_POSTS = %s WHERE ID = %s", (new_liked_posts, user_id))
        connect.commit()

        cursor.execute("SELECT COALESCE(LIKES, 0) FROM POSTS WHERE ID = %s", (post_id,))
        like_count = cursor.fetchone()[0]

        return jsonify({"likeCount": like_count, "liked": liked})

    except Exception as e:
        print(f"Erro ao curtir/descurtir: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()


@app.route("/delete_post/<int:post_id>", methods=["POST"])
def delet_post(post_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        connect = psycopg2.connect(**db_config)
        cursor = connect.cursor()

        cursor.execute("SELECT USER_ID FROM POSTS WHERE ID = %s", (post_id,))
        post_owner_id = cursor.fetchone()

        if not post_owner_id or post_owner_id[0] != session["user_id"]:
            return "Você não tem permissão para apagar esta postagem.", 403


        delete_comments_query = sql.SQL("DELETE FROM COMMENTS WHERE POST_ID = %s")
        cursor.execute(delete_comments_query, (post_id,))

        delete_post_query = sql.SQL("DELETE FROM POSTS WHERE ID = %s AND USER_ID = %s")
        cursor.execute(delete_post_query, (post_id, session["user_id"]))

        connect.commit()
    except Exception as e:
        return f"Erro ao apagar postagem: {e}"
    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()
    
    return redirect(url_for("home"))


@app.route("/comment_post/<int:post_id>", methods=["POST"])
def comment_post(post_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    content = request.form.get("comment_content")
    if not content:
        return "Comentario vazio", 400
    try:
        connect = psycopg2.connect(**db_config)
        cursor = connect.cursor()
        query = sql.SQL(
            "INSERT INTO COMMENTS (POST_ID, USER_ID, CONTENT) VALUES (%s, %s, %s)"
        )
        cursor.execute(query, (post_id, session["user_id"],content))
        connect.commit()
    except Exception as e:
        return f"Erro ao comentar a postagem: {e}"
    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)