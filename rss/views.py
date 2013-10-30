from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render

class IndexView(View):
	def get(self, request):
		return render(request, 'static/index.html')		

class LoginView(View):
	def get(self, request):
		return render(request, 'static/login.html')

class AboutView(View):
	def get(self, request):
		return render(request, 'static/about.html')
		
