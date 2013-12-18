from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout

from rss.models import Subscription
from rss.models import SubscriptionItem
from rss.models import User

import logging
import json
import datetime
import feedparser

logger = logging.getLogger('logview.userrequest')

def home(request):
	context = RequestContext(request)

	if request.user.is_authenticated:
		user = User.objects.all()[0];

		context.subscriptions = Subscription.objects.filter(user_id=user.id)
	else:
		logger.info("User made request (test logging)")

		from django.contrib.auth.forms import AuthenticationForm
		context['form'] = AuthenticationForm()

	return render_to_response('static/index.html', context_instance=context)		

def about(request):
	return render_to_response('static/index.html')

def login_redirect(request):
	return render_to_response('static/login.html')
	
def get_subscription_items(request):
	if(request.is_ajax()):
		subscription_id = request.POST["subscription_id"]

		subscription = Subscription.objects.get(id=subscription_id)

		itemset = subscription.item.all().order_by('-published')
		results = [ob.as_json() for ob in itemset]

		return HttpResponse(json.dumps(results), mimetype='application/json')

	return HttpResponse(json.dumps("Direct access is forbidden"), mimetype='application/json')

def get_subscriptions(request):
	if(request.is_ajax()):
		user_id = request.POST["user_id"]

		subscription = Subscription.objects.filter(user_id=user_id)

		itemset = subscription.all()
		results = [ob.as_json() for ob in itemset]

		return HttpResponse(json.dumps(results), mimetype='application/json')

	return HttpResponse(json.dumps("Direct access is forbidden"), mimetype='application/json')

def add_subscription(request):
	if(request.is_ajax()):
		user_id = request.POST["user_id"]
		subscription_url = request.POST["url"]

		try:
			newSub = Subscription.objects.get(url=subscription_url)
		except Subscription.MultipleObjectsReturned:
			return HttpResponse(json.dumps("already exists"), mimetype='application/json')
		except Subscription.DoesNotExist:
			d = feedparser.parse(subscription_url)

			newSub = Subscription()
			newSub.title = d.feed.title
			newSub.url = subscription_url
			newSub.user_id = user_id
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