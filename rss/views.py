from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth import authenticate, login, logout

from rss.models import Subscription
from rss.models import User

import logging

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