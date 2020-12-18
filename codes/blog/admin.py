from django.contrib import admin
from blog.models import *
# Register your models here.

admin.site.register(Blog)
admin.site.register(Picture)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Topic)
admin.site.register(Tag)
