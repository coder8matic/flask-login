from flask import Flask
from handlers.auth import authentication_handlers
from handlers.dashboard import dashboard_handlers
from handlers.post import post_handlers

app = Flask(__name__)
app.register_blueprint(authentication_handlers)
app.register_blueprint(dashboard_handlers)
app.register_blueprint(post_handlers)


if __name__ == '__main__':
    app.run(use_reloader=True, port=12333)
