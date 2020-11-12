from django.contrib import admin

from .models import Profile, Stock,Portfolio

admin.site.register(Profile)
admin.site.register(Stock)
admin.site.register(Portfolio)