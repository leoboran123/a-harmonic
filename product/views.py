from django.shortcuts import render,HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .models import Category, Comment, Product, Images
from .forms import CommentForm

# Create your views here.


def product_search(request):
    url = request.META.get('HTTP_REFERER') # geldiğimiz sayfanın url bilgisini verir
    if request.method=="POST":
        query = request.POST['query']
        results = Product.objects.filter(title__icontains=query)

        context = {
            "products":results,
        }
        return render(request, "products_page.html", context)
    
    else:
        return HttpResponseRedirect(url)



def productDetail(request, slug):
    products = Product.objects.get(slug=slug)
    images = Images.objects.filter(product_id=products.id)
    product_comments = Comment.objects.filter(product_id=products.id)

    context = {
        "product":products,
        "productGallery":images,
        "product_comments":product_comments,
        

    }

    return render(request, "detail.html", context)    


def categoryProduct(request, id):

    category = Category.objects.get(id=id)
    # Brings the lower category products too...
    category_and_descendants = category.get_descendants(include_self=True)
    category_ids = [cat.id for cat in category_and_descendants]
    if request.method=="POST":
        price = request.POST['rangeInput']

        products = Product.objects.filter(category_id__in=category_ids, price__lte=price)
    else:
        products = Product.objects.filter(category_id__in=category_ids)

    context = {
        "products":products,
    }

    return render(request, "products_page.html", context)

@login_required(login_url='/user/login')  # Check login
def addComment(request, id):
    url = request.META.get('HTTP_REFERER') # geldiğimiz sayfanın url bilgisini verir
    current_user = request.user
    
    if not current_user:
        messages.success(request, "You have to login to post comments")
        return HttpResponseRedirect(url)
    else:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                data = Comment()
                data.subject = form.cleaned_data['subject']
                data.comment = form.cleaned_data['comment']
                data.rate = form.cleaned_data['rate']
                data.ip = request.META.get('REMOTE_ADDR')
                data.user_id = current_user.id
                data.product_id = id
                data.save()
                messages.success(request, "yorumunuz başarıyla kaydedildi")
                return HttpResponseRedirect(url)
        return HttpResponseRedirect(url)

@login_required(login_url='/user/login')  # Check login
def deleteComment(request, id):
    current_user = request.user
    url = request.META.get('HTTP_REFERER') # geldiğimiz sayfanın url bilgisini verir


    user_comment = Comment.objects.get(user_id=current_user.id, id=id)

    user_comment.delete()

    messages.success(request, "Comment successfully deleted...")
    return HttpResponseRedirect(url)

