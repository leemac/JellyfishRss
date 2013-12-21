from django.db import models
from django.contrib.auth.models import User

class Subscription(models.Model):
	last_crawled = models.CharField(max_length=200)
	url = 		models.TextField()
	site_url = 	models.TextField()
	user = 		models.ForeignKey(User)
	title = 	models.TextField()
	
	def as_json(self):
		return dict(
				id=self.id,
				url=self.url,
				title=self.title
			)

	def __str__(self):
		return self.title

class SubscriptionItem(models.Model):
	content = 	models.TextField()
	published = models.DateTimeField()
	title = 	models.TextField()
	url = 		models.TextField()
	subscription = models.ForeignKey(Subscription, related_name="item")

	def as_json(self):
		return dict(
				url=self.url,
				title=self.title,
				content=self.content,
				published=str(self.published)
			)

	def __str__(self):
		return self.title