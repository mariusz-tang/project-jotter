from django.test import SimpleTestCase
from django.urls import reverse


class IndexPageTestCase(SimpleTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.request = self.client.get(reverse("index"))

    def test_accessible_by_name(self):
        self.assertEqual(self.request.status_code, 200)

    def test_correct_template_used(self):
        self.assertTemplateUsed(self.request, "pages/index.html")
