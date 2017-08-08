from django.shortcuts import render
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def index(request):
	return render(request, 'recsys/index.html')