from django.test import SimpleTestCase
from django.urls import reverse


class IndexPageTestCase(SimpleTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.url = reverse("index")
        super().setUpClass()
    
    def test_expected_url(self):
        self.assertEqual(self.url, "/")

    def test_correct_template_used(self):
        request = self.client.get(self.url)
        self.assertTemplateUsed(request, "pages/index.html")
