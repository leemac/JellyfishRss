from django.core.management.base import BaseCommand

import feedparser
import datetime

from rss.models import Subscription
from rss.models import SubscriptionItem
from rss.models import User
# This is used for loading local RSS files for testing
class Command(BaseCommand):

	def handle(self, *args, **options):

		self.stdout.write("Crawling sites! \n")

		for subscription in Subscription.objects.all():
			self.stdout.write("Crawling " + subscription.title +  "! \n")
			
			d = feedparser.parse(subscription.url)

			user = User.objects.all()[0];

			for item in d.entries:
				existingItem = SubscriptionItem.objects.filter(url=item.link).filter(url=item.link).count()

				if(existingItem != 0):
					continue

				self.stdout.write("*New* - "  + item.title + "\n")

				object = SubscriptionItem()
				object.title=item.title
				object.url=item.link
				object.subscription_id = subscription.id
				date = item.published_parsed

				object.published = datetime.date(int(date[0]),int(date[1]),int(date[2]))
				object.content = item.description
				object.save()
	

		
