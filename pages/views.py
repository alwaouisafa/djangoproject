from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404
#from accounts.views import admin_only
from .models import Book, Author
from django.shortcuts import redirect
from .forms import BookForm
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_200_OK
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import requests
from rest_framework.permissions import IsAuthenticated


# Create your views here.

def homePageView(request):
    return HttpResponse("Hello world")

def index(request):
    context={"message":"hello from template"}
    template=loader.get_template("index.html")
    return HttpResponse(template.render(context,request))
# @admin_only
def listBooks(request):
    context={"books": Book.objects.all().order_by("title")}
    return render(request,"listBooks.html",context)

def show (request,book_id):
    context={"book":get_object_or_404(Book,pk =book_id)}
    
    return render(request,"show.html",context)

def show (request,book_id):
    context={"book":get_object_or_404(Book,pk =book_id)}
    return render(request,"show.html",context)

def add (request):
    author=Author.objects.get(name="Victor Hugo")
    book=Book.objects.create(title="Dragon ball 3", quantity=12, author=author)
    return redirect("listBooks")
def edit (request):
    book = Book.objects.get(title ="Dragon ball 3")
    book.title="Dragon ball 6"
    book.save()
    return redirect("listBooks")

def remove (request):
    book = Book.objects.filter(title__startswith="Dragon")
    book.delete()
    return redirect("listBooks")

def add_with_form(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listBooks') # Redirect after saving
    else:
        form = BookForm() # Now form is always defined
    return render(request, "book-form.html", {"form": form})

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

@api_view(['POST'])
@permission_classes([AllowAny]) # Explicitly allow unauthenticated access
def login(request):
    #get data sent by the user
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response({'error': 'Required username and password'}, status= HTTP_400_BAD_REQUEST)
    #Authenticate the user
    user = authenticate(username=username, password=password)
    if user is None or not user.is_active:
        return Response({"error": "Invalid credentials"}, status=HTTP_401_UNAUTHORIZED)
    #create or get existing token
    token, created = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=HTTP_200_OK)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def listBooks(request):
    books = Book.objects.all().order_by("title").values()
    return Response({"Books": list(books)}) # DRF handles JSON rendering


