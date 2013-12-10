from django.contrib import admin
from insider.webapp import models


admin.site.register(models.LinkedInUserData)
admin.site.register(models.LinkedInConnection)
