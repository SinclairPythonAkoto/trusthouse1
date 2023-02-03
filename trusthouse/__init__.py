import os
from flask import Flask

def create_app() -> Flask:
    app: Flask = Flask(__name__)
    # Add your application configurations here
    app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "uploads")

    # create the uploads folder if it doesn't exist
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    return app

app: create_app = create_app()
