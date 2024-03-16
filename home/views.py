from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib import messages

from product.models import Category
from .forms import ContactForm
from .models import ContactFormMessage
from product.models import Product, Comment

# Create your views here.
def index(request):
    categories = Category.objects.all()
    products = Product.objects.all().order_by('rewievcount')[:6]
    comments = Comment.objects.filter(rate__gt=3).order_by('-create_at')[:6]

    context = {
        "categories":categories,
        "products":products,
        "comments":comments,
    }

    return render(request, 'index.html', context)


def testimonal(request):
    comments = Comment.objects.filter(rate__gt=3).order_by('-create_at')[:6]

    context = {
            "comments":comments,
        }


    return render(request, 'testimonal.html', context)
    

def aboutus(request):
    return render(request, 'aboutus.html')


def contact(request):


    if request.method=="POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage()  # create relation with model
            data.name = form.cleaned_data['name']  # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save data to table
            messages.success(request, "Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')

    else:
        form = ContactForm

    context = {
        "form":ContactForm
    }
    return render(request, 'contact.html', context)

