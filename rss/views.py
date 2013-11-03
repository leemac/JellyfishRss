from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render_to_response
from django.template import RequestContext

import logging

logger = logging.getLogger('logview.userrequest')

class IndexView(View):
	def get(self, request):
		context = RequestContext(request)

		logger.info("User made request (test logging)")

		from django.contrib.auth.forms import AuthenticationForm
		context['form'] = AuthenticationForm()

		return render_to_response('static/index.html', context_instance=context)		

class LoginView(View):
	def get(self, request):
		return render(request, 'static/login.html')

class AboutView(View):
	def get(self, request):
		return render(request, 'static/about.html')
		
