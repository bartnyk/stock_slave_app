import sys

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager

from base import cfg
from base.auth.auth import User
from base.auth.routes import blueprint as auth_blueprint
from base.command import CommandRunner
from base.stock.routes import blueprint as stock_blueprint

load_dotenv()

app = Flask(__name__)
auth_manager = LoginManager()
app.secret_key = cfg.SECRET_KEY
app.debug = cfg.DEBUG

app.register_blueprint(stock_blueprint)
app.register_blueprint(auth_blueprint)

auth_manager.init_app(app)
auth_manager.login_view = "/auth/login"
auth_manager.login_message = "Prove that you are me."


@auth_manager.user_loader
def load_user(username):
    return User(username=username)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = CommandRunner(sys.argv[1])
        command.run()
    else:
        app.run()
