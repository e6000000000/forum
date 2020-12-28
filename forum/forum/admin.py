from django.contrib import admin

from . import models


admin.site.register(models.Section)
admin.site.register(models.Thread)
admin.site.register(models.Post)
