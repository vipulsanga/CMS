import json

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
        self.assertContains(response, 'index-')

    def test_admin_login_page_is_available(self):
        response = self.client.get(reverse('admin_login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin Login')
        self.assertContains(response, 'Sign in with your Django account')

    def test_admin_dashboard_contains_interactive_article_form(self):
        user = get_user_model().objects.create_user(username='admin', password='secret123')
        self.client.force_login(user)

        response = self.client.get(reverse('admin_dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Article')
        self.assertContains(response, 'id="article-form"')
