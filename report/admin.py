from django.contrib import admin
from .models import GoogleCampaign, GoogleAdGroup, GoogleKeyword

admin.site.register(GoogleCampaign)
admin.site.register(GoogleAdGroup)
admin.site.register(GoogleKeyword)
