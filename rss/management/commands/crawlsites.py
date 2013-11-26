from django.core.management.base import BaseCommand

import feedparser
import datetime

from rss.models import Subscription
from rss.models import SubscriptionItem
from rss.models import User
# This is used for loading local RSS files for testing
class Command(BaseCommand):

	def handle(self, *args, **options):
		filepath = "rss/dummyfiles/google.xml"

		try:
			with open(filepath):
				d = feedparser.parse(filepath)

				user = User.objects.all()[0];

				newSub = Subscription.objects.get(title=d.feed.title)

				if(newSub is None):
					newSub = Subscription()
					newSub.title = d.feed.title
					newSub.url = d.feed.link
					newSub.user_id = user.id
					newSub.save()


				for item in d.entries:

					existingItem = SubscriptionItem.objects.filter(url=item.link).filter(url=item.link).count()

					if(existingItem != 0):
						continue

					self.stdout.write("Found item: "  + item.title + "\n")

					object = SubscriptionItem()
					object.title=item.title
					object.url=item.link
					object.subscription_id = newSub.id
					date = item.published_parsed

					object.published = datetime.date(int(date[0]),int(date[1]),int(date[2]))
					object.content = item.description
					object.save()

				
		except IOError:
			self.stdout.write("The file does not exist!")
			return

		
