from django.db import models
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.auth.models import User
from pytz import timezone
from time import gmtime, strftime

class Folder(models.Model):
	color = models.TextField(max_length=20,blank=True)
	user = 		models.ForeignKey(User)
	title = 	models.TextField()
	
	def as_json(self):
		return dict(
				id=self.id,
				title=self.title,
				color=self.color,
			)

	def __str__(self):
		return self.title

class Subscription(models.Model):
	last_crawled = models.CharField(max_length=200)
	url = 		models.TextField()
	site_url = 	models.TextField()
	title = 	models.TextField()
	favicon_url = models.TextField()
	
	def as_json(self):
		return dict(
				id=self.id,
				url=self.url,
				title=self.title,
				favicon_url=self.favicon_url
			)

	def __str__(self):
		return self.title

class SubscriptionUserRelation(models.Model):
	user = 			models.ForeignKey(User)
	folder = 		models.ForeignKey(Folder)
	subscription = 	models.ForeignKey(Subscription)
	
	def __str__(self):
		return self.user.id

class SubscriptionItem(models.Model):

	content = 	models.TextField()
	published = models.DateTimeField()
	title = 	models.TextField()
	url = 		models.TextField()
	is_read = 		models.BooleanField(default=False)
	is_favorite = 	models.BooleanField(default=False)
	subscription = models.ForeignKey(Subscription, related_name="item")

	def as_json(self):
		local_timezone = timezone("America/New_York")

		return dict(
				url=self.url,
				title=self.title,
				content=self.content,
				published= str(self.published),
				is_read=self.is_read,
				is_favorite = self.is_favorite,
				subscriptionTitle = self.subscription.title
			)

	def __str__(self):
		return self.title