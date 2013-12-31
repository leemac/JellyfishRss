from __future__ import absolute_import

from celery import task
from celery.utils.log import get_task_logger

import lxml.html as lh
import urllib2
import feedparser
import datetime

from rss.models import Subscription
from rss.models import SubscriptionItem
from rss.models import User

logger = get_task_logger(__name__)

@task(name='rss.tasks.poll')
def poll():
	logger.info("Crawling sites!")

	for subscription in Subscription.objects.all():
		logger.info("Crawling " + subscription.title +  "! \n")
		
		d = feedparser.parse(subscription.url)

		if not subscription.favicon_url:
			link = d.feed.link

			hostname = urlparse(d.feed.link).hostname
			link = "http://" + hostname

			self.stdout.write("Looking for missing favicon..." + link + "\n")
							
			doc = lh.parse(link)

			favicons = doc.xpath('//link[@rel="Shortcut Icon"]/@href')

			if len(favicons) == 0:
				favicons = doc.xpath('//link[@rel="shortcut icon"]/@href')

			self.stdout.write("*New* Found Favicon: " + str(len(favicons)))

			if len(favicons) > 0:
				favicon = favicons[0]
			else:
				favicon = ""

			if favicon:
				fav_url = favicon

				if not fav_url.startswith("http"):
					fav_url = link + favicon
					
				self.stdout.write(fav_url)
				subscription.favicon_url = fav_url
				subscription.save()

		user = User.objects.all()[0];

		for item in d.entries:
			existingItem = SubscriptionItem.objects.filter(url=item.link).filter(url=item.link).count()

			if(existingItem != 0):
				continue

			logger.info("*New* - "  + item.title + "\n")

			object = SubscriptionItem()
			object.title=item.title
			object.url=item.link
			object.subscription_id = subscription.id

			object.published = datetime.fromtimestamp(mktime(item.date_parsed))

			try:
				object.content = item.content[0]
			except AttributeError:
				logger.info("No content provided. Looking for a description...")

				try:
					object.content = item.description
				except AttributeError:
					logger.info("No content or description provided")														

			object.save()