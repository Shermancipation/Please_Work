from django.db import models
from ..login.models import User

# Create your models here.

class ItemManager(models.Manager):
    def add_item(self, form_response):
        errors = []
        response_to_views = {}

        if len(form_response['item']) < 4:
            errors.append("Item must be more than 3 characters.")

        if errors:
            response_to_views['success'] = False
            response_to_views['errors'] = errors
        else:
            response_to_views['success'] = True
            item1 = Item.objects.create(name=form_response['item'], added_by=form_response['user'])
            item1.user.add(form_response['user'])

        return response_to_views

    def add_wishlist(self, id, current_user):
        item1 = Item.objects.get(id=id)
        item1.user.add(current_user)

        return item1

    def remove_wishlist(self, id, current_user):
        item1 = Item.objects.get(id=id)
        item1.user.remove(current_user)

        return item1

    def your_wishlist(self, current_user):

        response_to_views = Item.objects.filter(user=current_user)

        return response_to_views

    def other_wishlist(self, current_user):

        response_to_views = Item.objects.all().exclude(user=current_user)

        return response_to_views

    def current_item(self, id):

        response_to_views = Item.objects.get(id=id)

        return response_to_views

class Item(models.Model):
    name = models.CharField(max_length=255)
    user = models.ManyToManyField(User, related_name="all_items_all_users")
    added_by = models.ForeignKey(User, related_name="all_items")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()
