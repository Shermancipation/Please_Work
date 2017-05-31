from django.shortcuts import render, redirect
from django.contrib import messages
from ..login.models import User
from .models import Item

# Create your views here.
def index(request):
    try:
        if request.session['id']:
            current_user = User.objects.get(id=request.session['id'])
            yourWishList = Item.objects.your_wishlist(current_user)
            otherWishList = Item.objects.other_wishlist(current_user)

            context = {
                'yourWishList': yourWishList,
                'otherWishList': otherWishList
            }

            return render(request, 'items/index.html', context)
        else:
            return redirect('/')
    except:
        return redirect('/')

def item_page(request):
    try:
        if request.session['id']:
            return render(request, 'items/additem.html')
        else:
            return redirect('/')
    except:
        return redirect('/')

def add_item(request):

    if request.method == "POST":
        current_user = User.objects.get(id=request.session['id'])

        form_response = {
            'user': current_user,
            'item': request.POST['item']
        }

        response_from_models = Item.objects.add_item(form_response)

        if response_from_models['success'] == False:
            for error in response_from_models['errors']:
                messages.error(request, error)
            return redirect('items:itemPage')

        return redirect('items:index')
    else:
        return redirect('items:itemPage')


def delete_item(request, id):

    try:
        if request.session['id']:
            Item.objects.get(id=id).delete()
            return redirect('items:index')
        else:
            return redirect('/')
    except:
            return redirect('/')

def wishlist_add(request, id):

    try:
        if request.session['id']:
            current_user = User.objects.get(id=request.session['id'])
            Item.objects.add_wishlist(id, current_user)
            return redirect('items:index')
        else:
            return redirect('/')
    except:
        return redirect('/')

def wishlist_remove(request, id):

    try:
        if request.session['id']:
            current_user = User.objects.get(id=request.session['id'])
            Item.objects.remove_wishlist(id, current_user)
            return redirect('items:index')
        else:
            return redirect('/')
    except:
        return redirect('/')

def item_specific(request, id):

    try:
        if request.session['id']:
            current_item = Item.objects.current_item(id)
            context = {
                'current_item': current_item
            }
            return render(request, 'items/itemspecific.html', context)
        else:
            return redirect('/')
    except:
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('login:index')
