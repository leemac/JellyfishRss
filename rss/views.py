from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

import logging

logger = logging.getLogger('logview.userrequest')

class IndexView(View):
	def get(self, request):
		context = RequestContext(request)

		logger.info("User made request (test logging)")

		from django.contrib.auth.forms import AuthenticationForm
		context['form'] = AuthenticationForm()

		return render_to_response('static/index.html', context_instance=context)		

def login_user(request):
	logout(request)
	username = password = ""

	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/static/welcome.html')

	context = RequestContext(request)
	from django.contrib.auth.forms import AuthenticationForm
	context['form'] = AuthenticationForm()

	return render_to_response('static/index.html', context_instance=context)

class AboutView(View):
	def get(self, request):
		return render(request, 'static/about.html')
		
