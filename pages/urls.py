from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, login
from .views import homePageView,index,listBooks,show,add,edit,remove,add_with_form

# Create the router and register your ViewSet
router = DefaultRouter()
router.register(r'api/books', BookViewSet, basename='book')

app_name= 'pages'
urlpatterns=[
    path('', homePageView, name="home"),
    path('index', index, name="index"),
    path('books', listBooks, name='listBooks'),
    path('<int:book_id>/', show,name='show'),
    path('ajouter_livre/', add ,name='add'),
    path('modifier_livre/', edit,name='edit'),
    path('supprimer_livre/', remove,name='remove'),
    path('ajouter_livre_form/',add_with_form,name='add book form'),
    path('', include(router.urls)),
    path('login', login, name="login")
    ]

