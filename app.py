import sys

from flask import Flask as _Flask
from flask_login import LoginManager

from base import cfg
from base.auth.auth import User
from base.auth.routes import blueprint as auth_blueprint
from base.command import CommandRunner
from base.stock.routes import blueprint as stock_blueprint

logger = cfg.logger


class Flask(_Flask):
    def logger(self):
        return cfg.logger


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


@app.route("/")
def index():
    return {"email": cfg.ADMIN_EMAIL, "phone": cfg.ADMIN_PHONE}


def run():
    if len(sys.argv) > 1:
        logger.info("Attempting to run command: '%s'", sys.argv[1])
        command = CommandRunner(sys.argv[1])
        command.run()
    else:
        app.run()
        logger.info("App started successfully, ")


if __name__ == "__main__":
    run()
