from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from services.email_service import Send_email
from datetime import datetime, timedelta
from application import bcrypt, db
from models.models import Usuario
import logging
import random

loginView = Blueprint('loginView', __name__)
@loginView.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')


        if not email or not password:
            flash("Digite e-mail e senha")
            return render_template("login.html"), 400
        
        user = Usuario.find_by_email(email)

        if user and user.verify_password(password):
            session['user_id'] = user.id
            return redirect(url_for("homeView.home"))
        else:
            flash("E-mail ou senha incorretos.", "error")
            return render_template("login.html"), 401
        
    return render_template("login.html")

    

@loginView.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        username = request.form['user']

        
        if not email or not password or not name or not username:
            flash("Preencha todos os campos", "error")
            return render_template("register.html"), 400
    
        if Usuario.find_by_email(email):
            flash("E-mail ja cadastrado, Use outro e-mail", "error")
            return render_template("register.html"), 400
    
        if Usuario.find_by_username(username):
            flash("Nome de usuario ja cadastrado. Escolha outro nome", "error")
            return render_template("register.html"), 400
        

        try:
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            new_user = Usuario(
                user_email=email,
                user_password=hashed_password,
                user_name=name,
                user_account=username
            )
            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id
            flash("Conta criada com sucesso!", "success")
            return redirect(url_for("loginView.login"))

        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao criar conta. Tente novamente", "error")
            return render_template("register.html"), 500


    return render_template('register.html')



@loginView.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        if not email:
            flash("Por favor, insira seu e-mail.", "error")
            return render_template('forgot_password.html')
        
        user = Usuario.find_by_email(email)

        if not user:
            flash("E-mail não encontrado", "error")
            return render_template("forgot_password.html")

        try:
            reset_code = str(random.randint(100000, 999999))
            user.reset_code = reset_code
            db.session.commit()

            
            Send_email(
                email,
                "Redefinição de Senha",
                f"Seu código para redefinição da senha é: {reset_code}"
                )
            
            flash("Codigo enviado para o seu e-mail.", "success")
            return redirect(url_for('loginView.reset_password'))

        except Exception as e:
            db.session.rollback()
            login.logger.error(f"Erro no envio de e-mail: {e}")
            flash("Erro ao processar solicitação. Tente novamente.", "error")


    return render_template('forgot_password.html')


@loginView.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        code = request.form.get('code')
        new_password = request.form.get('new_password')

        if not email or not code or not new_password:
            flash("Preencha todos os campos.", "error")
            return render_template('reset_password.html')

        try:
            user = Usuario.find_by_email(email)

            if not user or user.reset_code != code:
                flash("Código invalido ou e-mail incorreto", "error")
                return render_template("reset_password.html")
            
            if user.reset_code_created_at and datetime.now() - user.reset_code_created_at > timedelta(minutes=5):
                flash("O seu código expirou. Solicite um novo codigo", "error")
                return redirect(url_for("loginView.forgot_password"))
            
            hashed_password = bcrypt.generate_password_hash(new_password).decode("utf-8")

            user.user_password = hashed_password
            user.reset_code = None
            db.session.commit()

            flash("Senha redefinica com sucesso", "success")
            return redirect(url_for("loginView.login"))
        
        except Exception as e:
            db.session.rollback()
            logging.error(f"Erro ao redefinir a senha: {e}")
            flash("Erro ao processar redefinição. Tente novamente", "error")

    return render_template('reset_password.html')
