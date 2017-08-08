from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from Music.views import *

app_name='Music'

urlpatterns = [
    url(r'^$', SongsList.as_view(), name='music'),
    url(r'^(?P<curr>[0-9]*)$', SongsList.as_view(), name='music'),
    url(r'^update/', updateSongs, name='updateSongs'),
    url(r'^record/$', record, name='record'),
    url(r'^add/$', AddSong, name='add'),  # needs improvement
    # url(r'^test/$', test, name='test'),  # needs improvement
    # url(r'^test/$', cfList ,name='test'),

]