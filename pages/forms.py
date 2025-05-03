from django import forms
from .models import Author, Book
class BookForm(forms.ModelForm):
    author=forms.ModelChoiceField(queryset=Author.objects.all(),label="Author of the book")
    class Meta:
        model=Book
        fields=['title','author', 'quantity']
        labels={'title': 'Title of the book', 'quantity':'Quantity of books', 'author':'Author of the book'}
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0 or quantity > 100:
            raise forms.ValidationError("The quantity of booksmust be between 1 and 100.")
        return quantity
    def clean(self):
        cleaned_data = super().clean()
        title=self.cleaned_data.get('title')
        quantity=self.cleaned_data.get('quantity')
        if title and quantity:
            if title.startswith('Dragon') and quantity<=10 :
                raise forms.ValidationError("Minimum quantity of 10 is required for a Dragon book")
        return cleaned_data