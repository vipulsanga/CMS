import json

from bson import ObjectId
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .models import Article
from .mongo_service import get_article_from_fallback, get_articles_collection

MAX_TITLE_LENGTH = 200
MAX_CONTENT_LENGTH = 20_000


def _json_error(message, status=400):
    return JsonResponse({'error': message, 'status': status}, status=status)


def _parse_json_body(request):
    if request.content_type != 'application/json':
        return None, _json_error('Content-Type must be application/json', status=415)
    if not request.body:
        return None, _json_error('A JSON request body is required')
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None, _json_error('Invalid JSON payload')
    if not isinstance(payload, dict):
        return None, _json_error('JSON payload must be an object')
    return payload, None


def _validate_article_payload(payload, *, partial=False):
    allowed_fields = {'title', 'content'}
    unknown_fields = set(payload) - allowed_fields
    if unknown_fields:
        return None, _json_error('Unsupported field(s): ' + ', '.join(sorted(unknown_fields)))
    if partial and not payload:
        return None, _json_error('At least one field must be supplied')
    if not partial and set(payload) != allowed_fields:
        return None, _json_error('Both title and content are required')

    validated = {}
    if 'title' in payload:
        if not isinstance(payload['title'], str):
            return None, _json_error('Title must be a string')
        title = payload['title'].strip()
        if not title:
            return None, _json_error('Title cannot be blank')
        if len(title) > MAX_TITLE_LENGTH:
            return None, _json_error(f'Title must not exceed {MAX_TITLE_LENGTH} characters')
        validated['title'] = title
    if 'content' in payload:
        if not isinstance(payload['content'], str):
            return None, _json_error('Content must be a string')
        if len(payload['content']) > MAX_CONTENT_LENGTH:
            return None, _json_error(f'Content must not exceed {MAX_CONTENT_LENGTH} characters')
        validated['content'] = payload['content']
    return validated, None


def _serialize_article(document):
    article_id = document.get('_id')
    if article_id is None:
        article_id = document.get('id')
    return {
        'id': str(article_id),
        'title': document.get('title', ''),
        'content': document.get('content', ''),
        'created_at': document.get('created_at').isoformat() if hasattr(document.get('created_at'), 'isoformat') else document.get('created_at'),
    }


def _resolve_article_id(pk):
    try:
        return int(pk)
    except (TypeError, ValueError):
        return pk


def _find_mongo_article(collection, pk):
    if collection is None:
        return None

    lookup_value = _resolve_article_id(pk)
    try:
        return collection.find_one({'_id': ObjectId(str(pk))})
    except Exception:
        return collection.find_one({'_id': lookup_value})


def _list_mongo_articles():
    """Return MongoDB articles, newest first, for the admin dashboard."""
    collection = get_articles_collection()
    if collection is None:
        return []
    articles = [_serialize_article(article) for article in collection.find()]
    return sorted(articles, key=lambda article: article['created_at'] or '', reverse=True)


@require_http_methods(["GET", "POST"])
def api_article_list(request):
    if request.method == 'GET':
        collection = get_articles_collection()
        if collection is not None:
            articles = [_serialize_article(article) for article in collection.find()]
            return JsonResponse(
                sorted(articles, key=lambda article: article['created_at'] or '', reverse=True),
                safe=False,
            )

        articles = Article.objects.all().order_by('-created_at')
        return JsonResponse(
            [
                {
                    'id': article.id,
                    'title': article.title,
                    'content': article.content,
                    'created_at': article.created_at.isoformat() if article.created_at else None,
                }
                for article in articles
            ],
            safe=False,
        )

    if not request.user.is_authenticated:
        return _json_error('Authentication required', status=401)

    payload, error = _parse_json_body(request)
    if error:
        return error
    article_data, error = _validate_article_payload(payload)
    if error:
        return error

    collection = get_articles_collection()
    if collection is None:
        article = Article.objects.create(**article_data)
        return JsonResponse(
            {
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'created_at': article.created_at.isoformat() if article.created_at else None,
            },
            status=201,
        )

    from datetime import datetime

    result = collection.insert_one({
        **article_data,
        'created_at': datetime.utcnow(),
    })
    document = collection.find_one({'_id': result.inserted_id})
    return JsonResponse(_serialize_article(document), status=201)


@require_http_methods(["GET", "PUT", "PATCH", "DELETE"])
def api_article_detail(request, pk):
    collection = get_articles_collection()
    article = _find_mongo_article(collection, pk)
    is_mongo_article = article is not None

    if article is None:
        fallback_article = get_article_from_fallback(pk)
        if fallback_article is None:
            return _json_error('Article not found', status=404)

        article = {
            '_id': fallback_article.pk,
            'title': fallback_article.title,
            'content': fallback_article.content,
            'created_at': fallback_article.created_at.isoformat() if fallback_article.created_at else None,
        }

    if request.method == 'GET':
        return JsonResponse(_serialize_article(article))

    if not request.user.is_authenticated:
        return _json_error('Authentication required', status=401)

    if request.method in {'PUT', 'PATCH'}:
        payload, error = _parse_json_body(request)
        if error:
            return error
        update_data, error = _validate_article_payload(payload, partial=request.method == 'PATCH')
        if error:
            return error
        if not is_mongo_article:
            fallback_article = get_article_from_fallback(pk)
            if fallback_article is None:
                return _json_error('Article not found', status=404)
            for field, value in update_data.items():
                setattr(fallback_article, field, value)
            fallback_article.save()
            return JsonResponse(
                {
                    'id': fallback_article.id,
                    'title': fallback_article.title,
                    'content': fallback_article.content,
                    'created_at': fallback_article.created_at.isoformat() if fallback_article.created_at else None,
                }
            )

        lookup_value = _resolve_article_id(pk)
        try:
            collection.update_one({'_id': ObjectId(str(pk))}, {'$set': update_data})
        except Exception:
            collection.update_one({'_id': lookup_value}, {'$set': update_data})

        updated_article = _find_mongo_article(collection, pk)
        return JsonResponse(_serialize_article(updated_article))

    if not is_mongo_article:
        fallback_article = get_article_from_fallback(pk)
        if fallback_article is None:
            return _json_error('Article not found', status=404)
        fallback_article.delete()
        return HttpResponse(status=204)

    lookup_value = _resolve_article_id(pk)
    try:
        collection.delete_one({'_id': ObjectId(str(pk))})
    except Exception:
        collection.delete_one({'_id': lookup_value})
    return HttpResponse(status=204)


@login_required(login_url='admin_login')
def admin_dashboard(request):
    articles = _list_mongo_articles()
    return render(request, 'admin_dashboard.html', {'articles': articles})


def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin_dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'admin_login.html', {'form': form})


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


def health_check(request):
    return JsonResponse({'status': 'ok', 'service': 'cms'})


def frontend(request, path=''):
    return render(request, 'articles/frontend.html')
