from django.conf.urls import url
# from django.contrib.auth.views import LoginView,LogoutView
from .views import SignUp, ProfileView, LoginView, LogoutView, DashboardView
from django.contrib.auth.decorators import login_required

app_name='accounts'
urlpatterns = [
    url(r'^signup/$',SignUp.as_view(),name='signup'),
    url(r'^profile/(?P<pk>\d+)$',ProfileView.as_view(),name='profile'),
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'^logout/$',LogoutView.as_view(),name='logout'),
    url(r'^dashboard/$',login_required(DashboardView.as_view()),name='dashboard'),

]
