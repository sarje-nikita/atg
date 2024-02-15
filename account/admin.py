from django.contrib import admin
from .models import User


# class UserAdmin(admin.ModelAdmin):
#     readonly_fields = ('id',)


# Register your models here.
admin.site.register(User)
