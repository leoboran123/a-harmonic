from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from user.forms import LoginForm, RegisterForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

from order.models import ShopCart
from product.models import Product
from order.models import Coupon, UserCoupon
from .forms import UserProfileForm, UserUpdateForm
from .models import UserProfile

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
                return HttpResponseRedirect('/user/myaccount')
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

@login_required(login_url='/login')  # Check login
def userAccount(request):
    return render(request, "useraccount.html")


@login_required(login_url='/login')  # Check login
def userCart(request):
    url = request.META.get('HTTP_REFERER') # geldiğimiz sayfanın url bilgisini verir
    totalPrice=0
    dsc = 0
    subtotal=0
    current_user = request.user

    try:
        user_coupon = UserCoupon.objects.filter(user_id = current_user.id)
    except:
        messages.warning(request, "Coupon is not valid...")
        return HttpResponseRedirect(url)

    cart = ShopCart.objects.filter(user_id = current_user.id)

    # Resets UserCoupon.used section
    for coupons in user_coupon:
        coupons.used = False
        coupons.save()

    for product in cart:
        totalPrice = totalPrice + product.amount
        subtotal = subtotal + product.amount

    context = {
        "cart" : cart,
        "totalPrice" : totalPrice,
        "discount" : dsc,
        "subtotal" : subtotal

    }


    if request.method == "POST":
        user_coupon_code = request.POST['coupon_code'].upper()
        coupon_check = Coupon.objects.get(code = user_coupon_code)

        if coupon_check:
            try:
                user_coupon_check = UserCoupon.objects.get(coupon_id = coupon_check.id, user_id=current_user.id)
            except:
                messages.warning(request, "Coupon is not valid...")
                return HttpResponseRedirect(url)
            
            dsc = user_coupon_check.coupon.discount
            
            if dsc < 1:
                totalPrice = totalPrice - (totalPrice * dsc)
            else:
                totalPrice = totalPrice - dsc

            user_coupon_check.used = True
            user_coupon_check.save()

            context = {
                "cart" : cart,
                "totalPrice" : totalPrice,
                "discount" : dsc,
                "coupon" : coupon_check,
                "subtotal" : subtotal
            }
            
            messages.warning(request, "Coupon is successfully added..")
            return render(request, "cart.html", context)   
            
        else:
            messages.warning(request, "Coupon is not valid...")
            return HttpResponseRedirect(url)

    else:

        return render(request, "cart.html", context)


@login_required(login_url='/login')  # Check login
def userProfileUpdate(request):
    url = request.META.get('HTTP_REFERER') # geldiğimiz sayfanın url bilgisini verir
    current_user = request.user

    if request.method == "POST":
        user_update_form = UserProfileForm(request.POST, instance=current_user.userprofile)

        if user_update_form.is_valid():
            user_update_form.save()    
            messages.success(request,"Profile updated!")
            return HttpResponseRedirect(url)    
        else:
            messages.warning(request,"Profile could not updated! Please try again")
            return HttpResponseRedirect(url)    
            

    else:
        form = UserProfileForm(instance=current_user.userprofile)
    
        context = {
            "form":form
        }
    
        return render(request, "userprofile.html", context)


@login_required(login_url='/login')  # Check login
def userUpdate(request):
    url = request.META.get('HTTP_REFERER') # geldiğimiz sayfanın url bilgisini verir
    current_user = request.user

    if request.method == "POST":
        user_update_form = UserUpdateForm(request.POST, instance=current_user)

        if user_update_form.is_valid():
            user_update_form.save()    
            messages.success(request,"User updated!")
            return HttpResponseRedirect(url)    
        else:
            messages.warning(request,"User could not updated! Please try again")
            return HttpResponseRedirect(url)    
            

    else:
        form = UserUpdateForm(instance=current_user)
    
        context = {
            "form":form
        }
    
        return render(request, "useraccountupdate.html", context)


@login_required(login_url='/login')  # Check login
def changeUserPassword(request):
    url = request.META.get('HTTP_REFERER') # geldiğimiz sayfanın url bilgisini verir

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request,"Şifre başarıyla güncellendi!")
            return HttpResponseRedirect(url)
        else:
            messages.warning(request, "Hata oluştu. Bir daha deneyin")
            return HttpResponseRedirect(url)
    else:

        form = PasswordChangeForm(request.user)
        
        context= {
            "form":form,
        }

        return render(request, "userpasswordupdate.html", context)


def userOrders(request):
    current_user = request.user



    return render(request, "userorders.html")