import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from .models import Article

User = get_user_model()


class ArticleModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser", email="testuser@test.com", password="Test1234"
        )

    def setUp(self):
        self.article = Article.objects.create(
            title="Test Title", body="Test Body", author=self.user
        )

    def test_article_content(self):
        """Ensure fields and methods behave correctly."""
        self.assertEqual(self.article.title, "Test Title")
        self.assertEqual(self.article.body, "Test Body")
        self.assertEqual(str(self.article), "Test Title")
        self.assertEqual(self.article.author, self.user)

    def test_snippet_field(self):
        """Snippet should show trimmed preview."""
        self.assertTrue(self.article.snippet.endswith("..."))
        self.assertIn("Test Body", self.article.snippet)

    def test_article_id_is_uuid(self):
        """Ensure UUID field is valid."""
        self.assertIsInstance(self.article.article_id, uuid.UUID)

    def test_article_id_is_unique(self):
        """Ensure article IDs are unique."""
        another = Article.objects.create(
            title="Another", body="Another body", author=self.user
        )
        self.assertNotEqual(self.article.article_id, another.article_id)

    def test_ordering(self):
        """Newest article appears first."""
        older = self.article
        newer = Article.objects.create(
            title="Newer", body="Newer body", author=self.user
        )
        articles = list(Article.objects.all())
        self.assertEqual(articles[0], newer)
        self.assertEqual(articles[1], older)

    def test_get_absolute_url(self):
        """Ensure get_absolute_url works properly."""
        expected = reverse("article_detail", kwargs={"pk": self.article.pk})
        self.assertEqual(self.article.get_absolute_url(), expected)

    def test_updated_at_changes_on_save(self):
        """Ensure updated_at updates on save."""
        original_updated = self.article.updated_at
        # simulate change without sleep
        self.article.title = "Updated Title"
        self.article.save()
        self.article.refresh_from_db()
        self.assertGreater(self.article.updated_at, original_updated)

    def test_author_deletion_cascades(self):
        """Deleting author deletes related articles."""
        self.user.delete()
        self.assertEqual(Article.objects.count(), 0)


class ArticleURLTests(TestCase):
    """Ensure that URL routing and templates work correctly."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser", email="testuser@test.com", password="Test1234"
        )

    def setUp(self):
        self.client.login(username="testuser", password="Test1234")
        self.article = Article.objects.create(
            title="Test Article", body="Test Body", author=self.user
        )

    def test_urls_status_code(self):
        """Ensure core routes return correct status codes."""
        urls = {
            "list": reverse("article_list"),
            "detail": reverse("article_detail", kwargs={"pk": self.article.pk}),
            "edit": reverse("article_edit", kwargs={"pk": self.article.pk}),
            "delete": reverse("article_delete", kwargs={"pk": self.article.pk}),
        }
        for name, url in urls.items():
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, msg=f"{name} failed")

        invalid = self.client.get(
            reverse("article_detail", kwargs={"pk": uuid.uuid4()})
        )
        self.assertEqual(invalid.status_code, 404)

    def test_templates_used(self):
        """Ensure correct templates and content are used."""
        list_resp = self.client.get(reverse("article_list"))
        detail_resp = self.client.get(
            reverse("article_detail", kwargs={"pk": self.article.pk})
        )
        edit_resp = self.client.get(
            reverse("article_edit", kwargs={"pk": self.article.pk})
        )
        delete_resp = self.client.get(
            reverse("article_delete", kwargs={"pk": self.article.pk})
        )

        self.assertTemplateUsed(list_resp, "articles/article_list.html")
        self.assertTemplateUsed(detail_resp, "articles/article_detail.html")
        self.assertTemplateUsed(edit_resp, "articles/article_edit.html")
        self.assertTemplateUsed(delete_resp, "articles/article_delete.html")

        self.assertContains(list_resp, "Articles")
        self.assertContains(detail_resp, "Test Article")
        self.assertContains(delete_resp, "Delete Test Article")
        self.assertContains(edit_resp, "Edit Test Article")

    def test_template_context(self):
        """Ensure correct context vars exist."""
        list_resp = self.client.get(reverse("article_list"))
        detail_resp = self.client.get(
            reverse("article_detail", kwargs={"pk": self.article.pk})
        )
        self.assertIn("articles", list_resp.context)
        self.assertIn("article", detail_resp.context)

        # confirm updated list after adding another
        Article.objects.create(title="Another", body="Body", author=self.user)
        updated_resp = self.client.get(reverse("article_list"))
        self.assertEqual(updated_resp.context["articles"].count(), 2)


class ArticleViewsTests(TestCase):
    """Test behaviors and permissions in views."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="author", email="author@test.com", password="Test1234"
        )
        cls.other_user = User.objects.create_user(
            username="not_author", email="not_author@test.com", password="Test1234"
        )

    def setUp(self):
        self.article = Article.objects.create(
            title="View Test Article", body="View Test Body", author=self.user
        )

    def test_views_require_login(self):
        """Unauthenticated users get redirected."""
        create = self.client.get(reverse("article_create"))
        list_articles = self.client.get(reverse("article_list"))
        edit = self.client.get(reverse("article_detail", kwargs={"pk": self.article.pk}))
        
        self.assertEqual(create.status_code, 302)
        self.assertEqual(list_articles.status_code, 302)
        self.assertEqual(edit.status_code, 302)

        self.assertTrue(create.url.startswith("/accounts/login/"))
        self.assertTrue(list_articles.url.startswith("/accounts/login/"))
        self.assertTrue(edit.url.startswith("/accounts/login/"))


    def test_logged_in_user_can_create_article(self):
        """Logged-in user can create and becomes author."""
        self.client.login(username="author", password="Test1234")
        response = self.client.post(
            reverse("article_create"),
            {"title": "Brand New", "body": "Some content"},
        )
        self.assertEqual(response.status_code, 302)
        new_article = Article.objects.latest("created_at")
        self.assertEqual(new_article.author, self.user)

    def test_non_author_cannot_edit_article(self):
        """PermissionDenied for non-authors on edit."""
        self.client.login(username="not_author", password="Test1234")
        response = self.client.get(
            reverse("article_edit", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_non_author_cannot_delete_article(self):
        """PermissionDenied for non-authors on delete."""
        self.client.login(username="not_author", password="Test1234")
        response = self.client.get(
            reverse("article_delete", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_author_can_edit_and_delete(self):
        """Author can access edit/delete normally."""
        self.client.login(username="author", password="Test1234")
        edit_resp = self.client.get(
            reverse("article_edit", kwargs={"pk": self.article.pk})
        )
        delete_resp = self.client.get(
            reverse("article_delete", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(edit_resp.status_code, 200)
        self.assertEqual(delete_resp.status_code, 200)
