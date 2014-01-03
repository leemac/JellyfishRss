from datetime import datetime
from time import mktime

from urlparse import urlparse

from rss.models import Subscription
from rss.models import SubscriptionItem
from rss.models import User

import lxml.html as lh
import urllib2
import feedparser

class SitePoller:

    def poll(self, logger):

    	logger.info("here!")

    	for subscription in Subscription.objects.all():			
			d = feedparser.parse(subscription.url)

			if not subscription.favicon_url:
				link = d.feed.link

				hostname = urlparse(d.feed.link).hostname
				link = "http://" + hostname
								
				doc = lh.parse(link)

				favicons = doc.xpath('//link[@rel="Shortcut Icon"]/@href')

				if len(favicons) == 0:
					favicons = doc.xpath('//link[@rel="shortcut icon"]/@href')

				if len(favicons) > 0:
					favicon = favicons[0]
				else:
					favicon = ""

				if favicon:
					fav_url = favicon

					if not fav_url.startswith("http"):
						fav_url = link + favicon
						
					subscription.favicon_url = fav_url
					subscription.save()

			user = User.objects.all()[0];

			for item in d.entries:
				existingItem = SubscriptionItem.objects.filter(url=item.link).filter(url=item.link).count()

				if(existingItem != 0):
					continue

				object = SubscriptionItem()
				object.title=item.title
				object.url=item.link
				object.subscription_id = subscription.id

				object.published = datetime.fromtimestamp(mktime(item.date_parsed))

				try:
					object.content = item.content[0]
				except AttributeError:
					try:
						object.content = item.description
					except AttributeError:
						object.content = ""

				object.save()