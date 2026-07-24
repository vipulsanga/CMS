import json

from bson import ObjectId
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .models import Article
from .mongo_service import get_article_from_fallback, get_articles_collection


def _json_error(message, status=400):
    return JsonResponse({'error': message}, status=status)


def _serialize_article(document):
    article_id = document.get('_id')
    if article_id is None:
        article_id = document.get('id')
    return {
        'id': str(article_id),
        'title': document.get('title', ''),
        'content': document.get('content', ''),
        'created_at': document.get('created_at'),
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


@require_http_methods(["GET", "POST"])
def api_article_list(request):
    if request.method == 'GET':
        collection = get_articles_collection()
        if collection is None:
            articles = Article.objects.all().order_by('-created_at')
            payload = [
                {
                    'id': article.id,
                    'title': article.title,
                    'content': article.content,
                    'created_at': article.created_at.isoformat() if article.created_at else None,
                }
                for article in articles
            ]
            return JsonResponse(payload, safe=False)

        articles = list(collection.find().sort('created_at', -1))
        return JsonResponse([_serialize_article(article) for article in articles], safe=False)

    if not request.user.is_authenticated:
        return _json_error('Authentication required', status=401)

    try:
        payload = json.loads(request.body.decode('utf-8')) if request.body else {}
    except json.JSONDecodeError:
        return _json_error('Invalid JSON payload')

    title = (payload.get('title') or '').strip()
    content = payload.get('content') or ''
    if not title:
        return _json_error('Title is required')

    collection = get_articles_collection()
    if collection is None:
        article = Article.objects.create(title=title, content=content)
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
        'title': title,
        'content': content,
        'created_at': datetime.utcnow(),
    })
    document = collection.find_one({'_id': result.inserted_id})
    return JsonResponse(_serialize_article(document), status=201)


@require_http_methods(["GET", "PUT", "PATCH", "DELETE"])
def api_article_detail(request, pk):
    collection = get_articles_collection()
    article = _find_mongo_article(collection, pk)

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

    try:
        payload = json.loads(request.body.decode('utf-8')) if request.body else {}
    except json.JSONDecodeError:
        return _json_error('Invalid JSON payload')

    if request.method in {'PUT', 'PATCH'}:
        if collection is None:
            fallback_article = get_article_from_fallback(pk)
            if fallback_article is None:
                return _json_error('Article not found', status=404)
            if 'title' in payload:
                fallback_article.title = (payload.get('title') or '').strip() or fallback_article.title
            if 'content' in payload:
                fallback_article.content = payload.get('content')
            fallback_article.save()
            return JsonResponse(
                {
                    'id': fallback_article.id,
                    'title': fallback_article.title,
                    'content': fallback_article.content,
                    'created_at': fallback_article.created_at.isoformat() if fallback_article.created_at else None,
                }
            )

        update_data = {}
        if 'title' in payload:
            update_data['title'] = (payload.get('title') or '').strip()
        if 'content' in payload:
            update_data['content'] = payload.get('content')

        lookup_value = _resolve_article_id(pk)
        try:
            collection.update_one({'_id': ObjectId(str(pk))}, {'$set': update_data})
        except Exception:
            collection.update_one({'_id': lookup_value}, {'$set': update_data})

        updated_article = _find_mongo_article(collection, pk)
        return JsonResponse(_serialize_article(updated_article))

    if collection is None:
        fallback_article = get_article_from_fallback(pk)
        if fallback_article is not None:
            fallback_article.delete()
        return JsonResponse({'deleted': True})

    lookup_value = _resolve_article_id(pk)
    try:
        collection.delete_one({'_id': ObjectId(str(pk))})
    except Exception:
        collection.delete_one({'_id': lookup_value})
    return JsonResponse({'deleted': True})


@login_required(login_url='admin_login')
def admin_dashboard(request):
    articles = Article.objects.all().order_by('-created_at')
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
