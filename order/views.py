from django.shortcuts import render,HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string

from .models import ShopCart, UserCoupon, Order, OrderProduct, Coupon
from user.forms import UserProfile, User
from .forms import OrderForm
from product.models import Product

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
        messages.success(request, "Aynı ürün sepete bir kez daha eklendi!")
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
    url = request.META.get('HTTP_REFERER') # geldiğimiz sayfanın url bilgisini verir


    user_form = OrderForm(instance=current_user)
    user_cart = ShopCart.objects.filter(user_id=current_user.id)
    
    if not(user_cart):
        messages.warning(request, "You don't have anything in your cart...")
        return render(request, "index.html")


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
            "user_form":user_form,

        }

    except:
        context = {
            "cart":user_cart,
            "totalPrice":totalPrice,
            "user_form":user_form


        }

    if request.method=="POST":
        form = OrderForm(request.POST)
        # return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............
            data = Order()
            data.first_name = form.cleaned_data['first_name']  # get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.adress = form.cleaned_data['adress']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.country = form.cleaned_data['country']
            data.user_id = current_user.id
            data.total = totalPrice
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()  # random cod
            data.code = ordercode
            data.save()  #

            for rs in user_cart:
                detail = OrderProduct()
                detail.order_id = data.id  # Order Id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.price = rs.product.price
                detail.amount = rs.amount
                detail.save()

                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()

            ShopCart.objects.filter(user_id=current_user.id).delete()  # Clear & Delete shopcart
            request.session['cart_items'] = 0

            user_coupons.delete()
            messages.success(request, "Your Order has been completed. Thank you ")

            return render(request, 'order_completed.html', {'ordercode': ordercode,})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect(url)
    else:
        return render(request, "checkout.html", context)
    

