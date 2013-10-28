from django.contrib import admin
from rss.models import Subscription
from rss.models import SubscriptionItem

admin.site.register(Subscription)
admin.site.register(SubscriptionItem)