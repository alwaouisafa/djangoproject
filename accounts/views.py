from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages # import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden




# Create your views here.
# Create your views here.
def login_user(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("listBooks")
        else:
            messages.info(request, "Incorrect username or password")
    return render(request, "accounts/login.html", {"form": form}) 

def logout_user(request): 
    logout(request)
    return redirect("home")

def register_user(request): 
    if request.method== 'POST':
        form =UserCreationForm(request.POST) 
        if form.is_valid(): 
            form.save()
            return redirect("home")
    else:
        form =UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

def admin_only(view_func):
    @login_required # Ensures that the user is authenticated
    
    def _wrapped_view(request, *args, **kwargs):
        if request.user.username== "test@StaffUser" and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to access this page.")
    return _wrapped_view
