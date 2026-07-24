import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from .models import Article

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://127.0.0.1:27017/')
MONGO_DB = os.getenv('MONGO_DB', 'cmsdb')


def get_articles_collection():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=500)
        client.admin.command('ping')
        return client[MONGO_DB]['articles']
    except (PyMongoError, OSError, Exception):
        return None


def get_article_from_fallback(pk):
    try:
        lookup_key = int(pk)
    except (TypeError, ValueError):
        lookup_key = pk

    try:
        return Article.objects.get(pk=lookup_key)
    except Article.DoesNotExist:
        return None
