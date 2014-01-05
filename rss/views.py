from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout

from rss.models import Folder
from rss.models import Subscription
from rss.models import SubscriptionItem
from rss.models import SubscriptionUserRelation
from rss.models import User

from urlparse import urlparse

import lxml.html as lh
import urllib2
import logging
import json
import datetime
import feedparser

logger = logging.getLogger('logview.userrequest')

def home(request):
	context = RequestContext(request)

	if request.user.is_authenticated:
		user = User.objects.all()[0];
	else:
		logger.info("User made request (test logging)")

		from django.contrib.auth.forms import AuthenticationForm
		context['form'] = AuthenticationForm()

	return render_to_response('static/index.html', context_instance=context)		

def about(request):
	return render_to_response('static/index.html')

def login_redirect(request):
	return render_to_response('static/login.html')

def mark_subscription_read(request):
	if(request.is_ajax()):
		subscription_id = request.POST["subscription_id"]

		if int(subscription_id) == 0:
			itemset = SubscriptionItem.objects.all().order_by('-published')

			for item in itemset:
				item.is_read = True
				item.save()

			itemset = SubscriptionItem.objects.filter(is_read=False).order_by('-published')
			results = [ob.as_json() for ob in itemset]

			return HttpResponse(json.dumps(results), mimetype='application/json')
		else:	
			subscription = Subscription.objects.get(id=subscription_id)
			itemset = subscription.item.all().order_by('-published')

			for item in itemset:
				item.is_read = True
				item.save()

			itemset = subscription.item.filter(is_read=False).order_by('-published')
			results = [ob.as_json() for ob in itemset]

			return HttpResponse(json.dumps(results), mimetype='application/json')

	return HttpResponse(json.dumps("Direct access is forbidden"), mimetype='application/json')

def change_subscription_color(request):
	if(request.is_ajax()):
		subscription_id = request.POST["subscription_id"]
		color = request.POST["color"]

		subscription = Subscription.objects.get(id=subscription_id)

		subscription.color = color

		subscription.save()

		return HttpResponse(json.dumps("ok"), mimetype='application/json')

	return HttpResponse(json.dumps("Direct access is forbidden"), mimetype='application/json')


def get_subscription_items(request):
	if(request.is_ajax()):
		subscription_id = request.POST["subscription_id"]

		if int(subscription_id) == 0:
			itemset = SubscriptionItem.objects.filter(is_read=False)
		else:
			subscription = Subscription.objects.get(id=subscription_id)
			itemset = subscription.item.filter(is_read=False)

		results = [ob.as_json() for ob in itemset.order_by('-published')]

		return HttpResponse(json.dumps(results), mimetype='application/json')

	return HttpResponse(json.dumps("Direct access is forbidden"), mimetype='application/json')

def get_sidebar_data(request):
	if(request.is_ajax()):
		user_id = request.POST["user_id"]

		subscription = SubscriptionUserRelation.objects.filter(user_id=user_id)

		itemset = subscription.all()
		results = [ob.as_json() for ob in itemset]

		return HttpResponse(json.dumps(results), mimetype='application/json')

	return HttpResponse(json.dumps("Direct access is forbidden"), mimetype='application/json')

def add_subscription(request):
	if(request.is_ajax()):
		user_id = request.POST["user_id"]
		subscription_url = request.POST["url"]

		existingSubscriptionCount = Subscription.objects.filter(url=subscription_url).count()

		if existingSubscriptionCount == 1:
			existingSubscription = Subscription.objects.get(url=subscription_url)
			relation = SubscriptionUserRelation()
			relation.user_id = user_id
			relation.subscription_id = existingSubscription.id

			# Grab folder and create default if none exist
			try:
				defaultFolder = Folder.objects.get(user_id=user_id,title="Feeds")
			except Folder.DoesNotExist:				
				defaultFolder = Folder()
				defaultFolder.user_id = user_id
				defaultFolder.Title = "Feeds"
				defaultFolder.save()

			relation.folder_id = defaultFolder.id
			relation.save()

		else:
			d = feedparser.parse(subscription_url)
			
			newSub.title = d.feed.title
			newSub.url = subscription_url
			newSub.user_id = user_id
	
			if not newSub.favicon_url:
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
					favicon = "favicon.ico"

				if favicon:
					fav_url = favicon

					if not fav_url.startswith("http"):
						fav_url = link + favicon
						
					newSub.favicon_url = fav_url
			
			newSub.save()
			
			for item in d.entries:

				existingItem = SubscriptionItem.objects.filter(url=item.link).filter(url=item.link).count()

				if(existingItem != 0):
					continue

				logger.info("Found item: "  + item.title + "\n")

				object = SubscriptionItem()
				object.title=item.title
				object.url=item.link
				object.subscription_id = newSub.id

				theDate = item.date_parsed
				object.published = datetime.date(int(theDate[0]),int(theDate[1]),int(theDate[2]))
				
				try:
					object.content = item.content[0]
				except AttributeError:
					logger.error('Could not locate content')

				try:
					object.content = item.description
				except AttributeError:
					logger.error('Could not locate description')

				object.save()

			return HttpResponse(json.dumps("ok"), mimetype='application/json')

		return HttpResponse(json.dumps("already exists"), mimetype='application/json')

	return HttpResponse(json.dumps("Direct access is forbidden"), mimetype='application/json')


# AUTHENTICATION

def login_user(request):
	logout(request)
	username = password = ""

	context = RequestContext(request)

	if request.POST:
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
		if user is not None:
			logger.info("User " + username + " authenticated successfully.")
			if user.is_active:
				login(request, user)
				return render_to_response('static/login.html', context_instance=context)


	logger.info("Showing user index with login form....")

	from django.contrib.auth.forms import AuthenticationForm
	context['form'] = AuthenticationForm()

	return render_to_response('static/index.html', context_instance=context)

def logout_user(request):
	logout(request)

	context = RequestContext(request)
	return render_to_response('static/index.html', context_instance=context)