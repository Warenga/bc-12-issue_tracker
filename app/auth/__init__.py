from flask import Blueprint
from app import oauth

auth = Blueprint('auth', __name__)

twitter = oauth.remote_app(
    'twitter',
    consumer_key='KgZLj3iVMzoq9fQkJ9yQr6NEL',
    consumer_secret='FMXHqutxG2mRSZGA2QPf3JKTpASCewzwwgRcM5z9CvOBDsXzBU',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
)

from . import views