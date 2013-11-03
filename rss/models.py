from django.db import models
from django.contrib.auth.models import User

class Subscription(models.Model):
	last_crawled = models.CharField(max_length=200)
	url = 		models.URLField()
	site_url = 	models.URLField()
	user = 		models.ForeignKey(User)
	title = 	max_length=200
	def __str__(self):
		return self.title

class SubscriptionItem(models.Model):
	content = 	models.TextField()
	published = models.DateTimeField()
	title = 	max_length=200
	url = 		models.URLField()
	subscription = models.ForeignKey(Subscription)
	def __str__(self):
		return self.title