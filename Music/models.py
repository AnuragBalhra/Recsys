from django.db import models
from accounts.models import User
# Create your models here.
class Song(models.Model):
	song_id = models.AutoField(primary_key=True)
	song_name = models.CharField(max_length=200,blank=True)
	song_file = models.FileField(upload_to='music',blank=True,null=True)
	# song_url = models.URLField(blank=True)
	# release_date = models.DateField('date released', null=True,blank=True)
	added_on = models.DateField('date added',auto_now_add=True,null=True,blank=True)
	# artist = models.CharField(max_length=100, blank=True)
	# album = models.CharField(max_length=100, blank=True)
	# genre = models.CharField(max_length=100, blank=True)
	# country = models.CharField(max_length=100, blank=True)
	readonly_fields=('song_id')
	user_id = models.ForeignKey(User,blank=True, null=True)

	def attrs(self):
		for field in self._meta.fields:
			yield field.name, getattr(self, field.name)

	def __str__(self):
		return self.song_name

class Record(models.Model):
	record_id = models.AutoField(primary_key=True)
	song_id = models.ForeignKey(Song,related_name='current_song')
	user_id = models.ForeignKey(User)
	song_name = models.CharField(max_length=200)
	next_song = models.ForeignKey(Song,related_name='next_song', blank=True, null=True)
	percent_played = models.IntegerField(default=0)

	listen_date = models.DateTimeField(auto_now_add=True)
	
	def attrs(self):
		for field in self._meta.fields:
			yield field.name, getattr(self, field.name)

	def __str__(self):
		return str(self.user_id)+" " + str(self.song_id)+" "+self.song_name 