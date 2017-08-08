from django.contrib import admin

# Register your models here.

from .models import Song,Record

class MySongAdmin(admin.ModelAdmin):
	list_display = [
					'song_id',
					'song_name',
					'song_file',
					'user_id',
					'added_on',
					# 'artist',
					# 'album',
					# 'genre',
					# 'country',
					# 'release_date'
					]
	list_display_links = ['song_id',
					'song_name',
					'song_file',
					'user_id',
					'added_on',
					# 'artist',
					# 'album',
					# 'genre',
					# 'country',
					# 'release_date'
					]

class MyRecordAdmin(admin.ModelAdmin):
	list_display = ['record_id','user_id','song_name','song_id','next_song','percent_played','listen_date']
	list_display_links = ['record_id','user_id','song_name','song_id','next_song','percent_played','listen_date']


admin.site.register(Song,MySongAdmin)
admin.site.register(Record, MyRecordAdmin)