import json
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Article


class ArticleReactPagesTests(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            title='React Integration Test',
            content='This article is used to verify the React-powered pages.'
        )

    def test_article_list_api_returns_json(self):
        response = self.client.get(reverse('api_article_list'))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data[0]['title'], self.article.title)

    def test_article_detail_api_returns_json(self):
        response = self.client.get(reverse('api_article_detail', args=[self.article.pk]))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], self.article.title)
        self.assertEqual(data['content'], self.article.content)

    def test_frontend_index_page_serves_react_shell(self):
        response = self.client.get(reverse('frontend'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div id="root"></div>')
        self.assertContains(response, 'assets/index.js')

    def test_admin_login_page_is_available(self):
        response = self.client.get(reverse('admin_login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin Login')
        self.assertContains(response, 'Sign in with your Django account')

    def test_admin_dashboard_redirects_anonymous_users_to_login(self):
        response = self.client.get(reverse('admin_dashboard'))

        self.assertRedirects(response, f"{reverse('admin_login')}?next={reverse('admin_dashboard')}")

    def test_admin_dashboard_contains_interactive_article_form(self):
        user = get_user_model().objects.create_user(username='admin', password='secret123')
        self.client.force_login(user)

        response = self.client.get(reverse('admin_dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Article')
        self.assertContains(response, 'id="article-form"')

    def test_article_create_rejects_unauthenticated_requests(self):
        response = self.client.post(
            reverse('api_article_list'),
            data=json.dumps({'title': 'New article', 'content': 'Content'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 401)

    def test_article_create_validates_payload(self):
        user = get_user_model().objects.create_user(username='editor', password='secret123')
        self.client.force_login(user)

        response = self.client.post(
            reverse('api_article_list'),
            data=json.dumps({'title': '', 'content': 'Content'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Title cannot be blank')

    def test_article_delete_returns_no_content(self):
        user = get_user_model().objects.create_user(username='deleter', password='secret123')
        self.client.force_login(user)

        response = self.client.delete(reverse('api_article_detail', args=[self.article.pk]))

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b'')

    @patch('articles.views.get_articles_collection')
    def test_local_article_can_be_updated_when_mongo_is_available(self, get_collection):
        mongo_collection = Mock()
        mongo_collection.find_one.return_value = None
        get_collection.return_value = mongo_collection
        user = get_user_model().objects.create_user(username='editor2', password='secret123')
        self.client.force_login(user)

        response = self.client.patch(
            reverse('api_article_detail', args=[self.article.pk]),
            data=json.dumps({'title': 'Updated title'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Updated title')
        mongo_collection.update_one.assert_not_called()


class SmokeTests(TestCase):
    """Fast checks that the public application endpoints are reachable."""

    def test_health_endpoint_reports_ok(self):
        response = self.client.get(reverse('health_check'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok', 'service': 'cms'})

    @patch('articles.views.get_articles_collection', return_value=None)
    def test_article_list_endpoint_returns_a_json_list(self, _get_collection):
        response = self.client.get(reverse('api_article_list'))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_frontend_shell_is_reachable(self):
        response = self.client.get(reverse('frontend'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div id="root"></div>')
