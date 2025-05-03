from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from .models import Book,Author # adjust if your model is in another file

class BookAndAuthorTests(TestCase):
    @classmethod
    def setUpTestData(self):
        """Run once for the whole TestCase (faster)."""
        self.author = Author.objects.create(name="Victor Hugo")
        self.book = Book.objects.create(
            title="Les Misérables",
            quantity=10,
            author=self.author
        )
    def test_book_creation(self):
        """Test that the book was created."""
        self.assertEqual(Book.objects.count(), 1)

    def test_add_book_with_valid_form(self):
        # Simulate valid POST data
        author = Author.objects.create(name="Victor hugo")
        data = {
            'title': 'Test Book',
            'author': author.id,
            'quantity': 30
        }
        response = self.client.post(reverse('add book form'), data)
        # Check redirection
        self.assertEqual(response.status_code, 302)
        # Verify that the book was created
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.last().title, 'Test Book')
        
    def test_list_books_page_loads(self):
        url = reverse('listBooks') # or use the actual path if name isn't set
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) # Page loads correctly
        # self.assertTemplateUsed(response, 'listBooks.html') # Optional: check template