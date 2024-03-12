from django.shortcuts import render,HttpResponse, HttpResponseRedirect
from .models import Category, Product, Images

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

    context = {
        "product":products,
        "productGallery":images,

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


