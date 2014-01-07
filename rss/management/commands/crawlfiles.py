from django.core.management.base import BaseCommand

import feedparser
from datetime import datetime
from time import mktime

from rss.models import Subscription
from rss.models import SubscriptionItem

# This is used for loading local RSS files for testing
class Command(BaseCommand):

	def handle(self, *args, **options):
		self.CrawlFile("rss/dummyfiles/scotthanselman.xml", "http://feeds.hanselman.com/scotthanselman")
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

				try:
					newSub = Subscription.objects.get(title=d.feed.title)
				except Subscription.DoesNotExist:
					newSub = Subscription()
					newSub.title = d.feed.title
					newSub.url = rss_url
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

					try :
						object.published = datetime.fromtimestamp(mktime(item.published_parsed))
					except AttributeError:
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

				
		except IOError:
			self.stdout.write("The file does not exist!")
			return	

		
