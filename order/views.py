from django.shortcuts import render,HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import ShopCart, UserCoupon
from user.forms import UserProfile, User


@login_required(login_url='/login')  # Check login
# Create your views here.
def addProductToCart(request, id):
    url = request.META.get('HTTP_REFERER') # geldiğimiz sayfanın url bilgisini verir
    current_user = request.user

    cart = ShopCart()
    # Checking if the user already has this product in his/her cart...
    try:

        check_shopcart = ShopCart.objects.get(user_id=current_user.id, product_id=id)

    
        check_shopcart.quantity = check_shopcart.quantity + 1
        check_shopcart.save()
        messages.success(request, "Sepete bir kez daha eklendi!")
        return HttpResponseRedirect(url)

    except:

        cart.quantity = 1
        cart.user_id = current_user.id
        cart.product_id = id

        cart.save()
        messages.success(request, "Sepete başarıyla eklendi!")

        return HttpResponseRedirect(url)


@login_required(login_url='/login')  # Check login
def deleteFromCart(request, id):
    current_user = request.user

    cart_product = ShopCart.objects.get(product_id=id, user_id=current_user.id)
    cart_product.delete()

    url = request.META.get('HTTP_REFERER') # geldiğimiz sayfanın url bilgisini verir
    return HttpResponseRedirect(url)
    

@login_required(login_url='/login')  # Check login
def lessQuantityCart(request, id):
    current_user = request.user

    cart_product = ShopCart.objects.get(user_id = current_user.id, product_id=id)

    cart_product.quantity = cart_product.quantity - 1

    if(cart_product.quantity == 0):
        cart_product.delete()
    else:
        cart_product.save()
    url = request.META.get('HTTP_REFERER') # geldiğimiz sayfanın url bilgisini verir
    return HttpResponseRedirect(url)


@login_required(login_url='/login')  # Check login
def moreQuantityCart(request, id):
    current_user = request.user

    cart_product = ShopCart.objects.get(user_id=current_user.id, product_id=id)

    cart_product.quantity = cart_product.quantity + 1

    cart_product.save()
    url = request.META.get('HTTP_REFERER') # geldiğimiz sayfanın url bilgisini verir
    return HttpResponseRedirect(url)


@login_required(login_url='/login')  # Check login
def checkout(request):
    current_user = request.user
    totalPrice = 0

    user_form = UserProfile(instance=current_user)
    user_cart = ShopCart.objects.filter(user_id=current_user.id)
    
    for prices in user_cart:
        totalPrice = totalPrice + prices.amount

    
    try:
        user_coupons = UserCoupon.objects.get(user_id=current_user.id, used=True)

        if user_coupons.coupon.discount < 1:
            totalPrice = totalPrice - (totalPrice * user_coupons.coupon.discount)
        else:
            totalPrice = totalPrice - user_coupons.coupon.discount

        context = {
            "cart":user_cart,
            "totalPrice":totalPrice,
            "user_coupon":user_coupons,
            "user_form":user_form

        }

    except:
        context = {
            "cart":user_cart,
            "totalPrice":totalPrice,
            "user_form":user_form


        }


    return render(request, "checkout.html", context)
    

