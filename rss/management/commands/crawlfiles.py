from django.core.management.base import BaseCommand

import feedparser
import datetime

from rss.models import Subscription
from rss.models import SubscriptionItem
from rss.models import User
# This is used for loading local RSS files for testing
class Command(BaseCommand):

	def handle(self, *args, **options):
		self.CrawlFile("rss/dummyfiles/google.xml", "http://rss.cnn.com/rss/cnn_topstories.rss")
		self.CrawlFile("rss/dummyfiles/cnn_us.xml", "http://rss.cnn.com/rss/cnn_us.rss")
		self.CrawlFile("rss/dummyfiles/cnn_financial.xml", "http://rss.cnn.com/rss/money_latest.rss")
		self.CrawlFile("rss/dummyfiles/cnn_political.xml", "http://rss.cnn.com/rss/cnn_allpolitics.rss")
		self.CrawlFile("rss/dummyfiles/cnn_top_stories.xml", "http://rss.cnn.com/rss/cnn_topstories.rss")

	def CrawlFile(self, filepath, rss_url):

		self.stdout.write("Importing file: "  + filepath + "\n")
		try:
			with open(filepath):
				d = feedparser.parse(filepath)

				self.stdout.write(d.feed.title)

				user = User.objects.all()[0];

				try:
					newSub = Subscription.objects.get(title=d.feed.title)
				except Subscription.DoesNotExist:
					newSub = Subscription()
					newSub.title = d.feed.title
					newSub.url = rss_url
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

		
