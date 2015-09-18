from django.contrib import admin
from .models import Report, GoogleClient, GoogleCampaign, GoogleAdGroup, GoogleKeyword, FacebookCampaign, FacebookAccount, Source, adSource

admin.site.register(Report)
admin.site.register(GoogleClient)
admin.site.register(GoogleCampaign)
admin.site.register(GoogleAdGroup)
admin.site.register(GoogleKeyword)
admin.site.register(FacebookCampaign)
admin.site.register(FacebookAccount)
admin.site.register(Source)
admin.site.register(adSource)
