import os

import torch
from flask import Flask, request, jsonify
from .config import Config
from dotenv import load_dotenv
import logging
from logging.handlers import TimedRotatingFileHandler
from flask_cors import CORS



def create_app(config_class=Config):
    """
    Create a Flask application using the app factory pattern.
    :param config_class: Configuration class 
    :return:  Flask app
    """""
    load_dotenv()

    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.config.from_object(config_class)
    if not os.path.exists('logs'):
        os.mkdir('logs')

    handler = TimedRotatingFileHandler(app.config['LOG_FILE'], when="midnight", interval=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    # Routes

    @app.route('/')
    def index():
        return jsonify({'message': 'Welcome to the Image Detection API'})

    @app.route('/gpu')
    def gpu():
        import torch
        print("PyTorch version:", torch.__version__)
        print("CUDA built:", torch.backends.cuda.is_built())
        print("CUDA available:", torch.cuda.is_available())
        app.logger.info(f"PyTorch version: {torch.__version__}")
        app.logger.info(f"CUDA built: {torch.backends.cuda.is_built()}")
        app.logger.info(f"CUDA available: {torch.cuda.is_available()}")
        cuda_available = torch.cuda.is_available()

        if cuda_available:
            # Force CUDA initialization
            torch.cuda.init()
            gpu_count = torch.cuda.device_count()
            gpu_name = torch.cuda.get_device_name(0)
            return {
                "cuda_available": True,
                "gpu_count": gpu_count,
                "gpu_name": gpu_name,
                "cuda_version": torch.version.cuda
            }

        return {
            "cuda_available": False,
            "error": "CUDA not available",
            "cuda_built": torch.backends.cuda.is_built()
        }

    return app