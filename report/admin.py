from django.contrib import admin
from .models import Report, GoogleCampaign, GoogleAdGroup, GoogleKeyword, FacebookCampaign, FacebookAccount

admin.site.register(Report)
admin.site.register(GoogleCampaign)
admin.site.register(GoogleAdGroup)
admin.site.register(GoogleKeyword)
admin.site.register(FacebookCampaign)
admin.site.register(FacebookAccount)
