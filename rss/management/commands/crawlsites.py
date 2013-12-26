from django.core.management.base import BaseCommand
from datetime import datetime
from time import mktime
import feedparser


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

				object.published = datetime.fromtimestamp(mktime(item.date_parsed))

				try:
					object.content = item.content[0]
				except AttributeError:
					self.stdout.write("No content provided. Looking for a description...")

					try:
						object.content = item.description
					except AttributeError:
						self.stdout.write("No content or description provided")														

				object.save()
	

		
