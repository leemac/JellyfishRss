
def include_login_form(request):
	form = LoginView()
	return {'login_form': form}