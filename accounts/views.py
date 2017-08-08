from django.shortcuts import render, redirect, resolve_url
# from django import forms
from django.views.generic.edit import FormView
from django.views.generic import DetailView, TemplateView
from django.views import View
# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy
from .models import User
from .forms import SignUpForm, LoginForm
from django.shortcuts import redirect, reverse
from django.contrib.auth.views import LoginView as Login,LogoutView as Logout

class SignUp(FormView):
	template_name = 'accounts/signup.html'
	form_class = SignUpForm
	success_url = reverse_lazy('accounts:login')
	redirect_authenticated_user = True
	def get(self, request):
		if request.user.is_authenticated:
			return redirect(reverse('accounts:dashboard'))
		return super().get(request)

	def form_valid(self, form):
		form.save()
		return super(SignUp, self).form_valid(form)

class LoginView(Login):
	template_name = 'registration/login.html'
	redirect_authenticated_user = True
	# form_class = LoginForm
	# def post(self,request, **kwargs):
	# 	form = self.form_class(request.POST)
	# 	if form.is_valid():
			
	# 		raise Exception(form)
	
	def get_success_url(self):
		# url = super().get_redirect_url()
		redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
		# raise Exception(self.get_redirect_url() )
		return redirect_to or reverse_lazy('accounts:dashboard')

class LogoutView(Logout):
	pass

class ProfileView(DetailView):
	model = User
	# self.pk = self.request.user.pk


class DashboardView(TemplateView):
	template_name = 'accounts/dashboard.html';
	# def get(self, request):
	# 	context = self.get_context_data
		

	def get_context_data(self,**kwargs):
		# raise Exception('hello')
		context = super( **kwargs).get_context_data()
		context['object'] = self.request.user
		return context