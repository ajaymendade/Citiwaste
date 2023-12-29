from django.shortcuts import render
from website.models import Contact
from django.contrib import messages

# Create your views here.
def homepage(request):
    return render(request, 'website/homepage.html')

def about(request):
    return render(request, 'website/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        details = Contact(name=name, email=email, message=message)
        details.save()
        messages.info(request, 'Details saved, we will reach out to you soon.')
        return render(request, 'website/contact.html')
    else:
         return render(request, 'website/contact.html')

