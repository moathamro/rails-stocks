from django.contrib import admin

from .models import Profile, Stock, Portfolio, Notification

admin.site.register(Profile)
admin.site.register(Stock)
admin.site.register(Portfolio)
admin.site.register(Notification)
