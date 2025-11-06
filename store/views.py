from django.shortcuts import render
from .models import item, category
from django.shortcuts import get_object_or_404
# Create your views here.
def home(request):
    items = item.objects.filter(is_sold=False)
    categories=category.objects.all()

    context = {
        'items':items,
        'categories': categories
    }
    return render(request, 'store/home.html', context)

def contact(request):
    context={
        'msg' : 'Quieres otros productos contactame!'
    }

    return render(request, 'store/contact.html', context)

def detail(request, pk):
    item = get_object_or_404(item, pk=pk)
    related_item= item.objects.filter(category=item.category,is_sold= False).exclude(pk=pk)[0:3]

    context={
     'item': item,
     'related_items': related_item

    }

    return render(request, 'store/item.html', context)