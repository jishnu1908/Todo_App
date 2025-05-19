from django.contrib import admin
from .models import todo

# Register your models here.


class super(admin.ModelAdmin):
    list_display = ['task', 'dat']


admin.site.register(todo, super)