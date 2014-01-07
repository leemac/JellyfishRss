from datetime import datetime
from time import mktime

from urlparse import urlparse

from rss.models import Subscription
from rss.models import SubscriptionItem

import lxml.html as lh
import urllib2
import feedparser

class SitePoller:

	def add_site_and_poll(self, rss_url):
		self.add_site(rss_url)
		
		subscription = Subscription.objects.get(url=rss_url)
		self.poll_site(subscription)

	def add_site(self, rss_url):
		try:
			subscription = Subscription.objects.get(url=rss_url)
		except Subscription.DoesNotExist:
			d = feedparser.parse(rss_url)

			subscription = Subscription()
			subscription.title = d.feed.title
			subscription.url = rss_url
			subscription.color = ""
			subscription.save()

	def poll_site(self, subscription):
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
				favicon = link + "/favicon.ico"

			if favicon:
				fav_url = favicon

				if not fav_url.startswith("http"):
					fav_url = link + favicon
					
				subscription.favicon_url = fav_url
				subscription.save()

		for item in d.entries:
			existingItem = SubscriptionItem.objects.filter(url=item.link).filter(url=item.link).count()

			if(existingItem != 0):
				continue

			object = SubscriptionItem()
			object.title=item.title
			object.url=item.link
			object.subscription_id = subscription.id

			try :
				object.published = datetime.fromtimestamp(mktime(item.published_parsed))
			except AttributeError:
				object.published = datetime.fromtimestamp(mktime(item.date_parsed))

			try:
				object.content = item.content[0]
			except AttributeError:
				try:
					object.content = item.description
				except AttributeError:
					object.content = ""

			object.save()

	def poll(self, logger):

		for subscription in Subscription.objects.all():			
			self.poll_site(subscription)
