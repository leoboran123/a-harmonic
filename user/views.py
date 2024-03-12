from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from user.forms import LoginForm, RegisterForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

from order.models import ShopCart
from product.models import Product

# Create your views here.

def userLogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].lower()
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Başarıyla giriş yapıldı! {user.username}")
                return HttpResponseRedirect('/user/login')
            else:
                messages.warning(request, "Tekrar oturum açmayı deneyin")
                return HttpResponseRedirect('/user/login')

    else:
        login_form = LoginForm
        context = {
            "form":login_form
        }

        return render(request, "login.html", context)

def userLogout(request):
    logout(request)
    return HttpResponseRedirect("/")


def userRegister(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username'].lower()
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)

            
            messages.success(request, "Hesabınız başarıyla oluşturuldu!")
            return HttpResponseRedirect("/")
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/user/register")
        
    else:
        if request.POST != None:

            register_form = RegisterForm(request.POST)
        else:
            register_form = RegisterForm()

        context= {
            "form":register_form
        }

        return render(request, "register.html", context)

def userAccount(request):
    return render(request, "useraccount.html")


@login_required(login_url='/login')  # Check login
def userCart(request):
    current_user = request.user

    cart = ShopCart.objects.filter(user_id = current_user.id)

    totalPrice=0

    for product in cart:

        totalPrice = totalPrice + product.amount

    context = {
        "cart" : cart,
        "totalPrice":totalPrice,
    }

    return render(request, "cart.html", context)


