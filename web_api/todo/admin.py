from django.contrib import admin

from todo.models import Item, ToDo

admin.site.register(ToDo)
admin.site.register(Item)
