from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.UserProfile)
admin.site.register(models.Following)
admin.site.register(models.LoginLog)
# admin.site.register(models.UserProfilePicture)
