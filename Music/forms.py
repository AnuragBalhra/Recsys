from django.forms.models import ModelForm
from django import forms
from .models import Song

class AddSongForm(forms.Form):
	song_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'plceholder':'File Name'}))
	song_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder':'Song Name'}))

	# def clean(self):
		# raise Exception(self.request)

	# class Meta:
		# model = Song
		# exclude = ('added_on','user_id',)

