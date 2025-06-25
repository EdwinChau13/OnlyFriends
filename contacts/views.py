from django.shortcuts import render

# Create your views here.
def contact(request):
    contacts = []
    
    return render(request, 'contacts/contact.html', {'contacts':contacts})