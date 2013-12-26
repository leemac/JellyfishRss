from __future__ import absolute_import

from celery import task
from celery.utils.log import get_task_logger

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

			theDate = item.date_parsed
			object.published = datetime.date(int(theDate[0]),int(theDate[1]),int(theDate[2]))

			try:
				object.content = item.content[0]
			except AttributeError:
				logger.info("No content provided. Looking for a description...")

				try:
					object.content = item.description
				except AttributeError:
					logger.info("No content or description provided")														

			object.save()