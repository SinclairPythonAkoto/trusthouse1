from flask import Flask

def create_app():
    app = Flask(__name__)
    # Add your application configurations here
    return app

app = create_app()
