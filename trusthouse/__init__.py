from flask import Flask

def create_app() -> Flask:
    app: Flask = Flask(__name__)
    # Add your application configurations here
    return app

app: create_app = create_app()
