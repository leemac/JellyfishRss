from django.db import models
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.auth.models import User
from pytz import timezone
from time import gmtime, strftime


class Folder(models.Model):
	user = 		models.ForeignKey(User)
	title = 	models.TextField()
	color = 	models.TextField(max_length=20, blank=True)
	
	def as_json(self):
		return dict(
				id=self.id,
				title=self.title,
				color=self.color
			)

	def __str__(self):
		return self.title

class Subscription(models.Model):
	last_crawled = models.CharField(max_length=200)
<<<<<<< HEAD
	color = models.TextField(max_length=20, blank=True)
=======
	color = models.TextField(max_length=20,blank=True)
>>>>>>> 54889cfd23a016ffca6fda7d32a455a9c76a9d49
	url = 		models.TextField()
	site_url = 	models.TextField()
	title = 	models.TextField()
	favicon_url = models.TextField(blank=True)
	
	def as_json(self):
		return dict(
				id=self.id,
				url=self.url,
				title=self.title,
				color=self.color,
				favicon_url=self.favicon_url
			)

	def __str__(self):
		return self.title

class SubscriptionUserRelation(models.Model):
	user = models.ForeignKey(User)
	subscription = models.ForeignKey(Subscription)
	folder = models.ForeignKey(Folder)

	def __str__(self):
		return "Relation - User [" + self.user.id + "]"

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
				subscriptionTitle = self.subscription.title,
				subscriptionColor = self.subscription.color
			)

	def __str__(self):
		return self.title