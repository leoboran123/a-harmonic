from django.shortcuts import render,HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import ShopCart


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



