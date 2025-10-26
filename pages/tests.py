from django.test import SimpleTestCase
from django.urls import reverse


class HomePageTests(SimpleTestCase):
    def test_urls(self):
        response = self.client.get("/")
        response_name = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_name.status_code, 200)

    def test_homepageview(self):
        response = self.client.get(reverse("home"))

        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "Home")
