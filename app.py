from application import create_app
from dotenv import load_dotenv
import os

app = create_app()


load_dotenv(dotenv_path="env/secret_key.env")
app.secret_key = os.getenv('SECRET_KEY')

app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'



from flask_cors import CORS
CORS(app)



if __name__ == "__main__":
    app.run(debug=True)