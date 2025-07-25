import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from mangum import Mangum
from starlette.middleware.wsgi import WSGIMiddleware
from src.server import app

asgi_app = WSGIMiddleware(app)
handler = Mangum(asgi_app, lifespan="off")

def lambda_handler(event, context):
    return handler(event, context)
