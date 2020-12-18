from django.contrib import admin
from user.models import *
# Register your models here.

admin.site.register(User)
admin.site.register(VerificationCode)
admin.site.register(Profile)
admin.site.register(Follow)