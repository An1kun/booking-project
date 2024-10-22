from django.contrib import admin
from .models import Guest, Favorites, Employee, Review

# Register your models here.
admin.site.register(Guest)
admin.site.register(Favorites)
admin.site.register(Employee)
admin.site.register(Review)
