from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .models import Song, Record
from .forms import AddSongForm
# Create your views here.

class SongsList(ListView):
	model = Song
	template_name = 'Music/index2.html'

	def get_context_data(self, **kwargs):
		# user = request.user
		# raise Exception('curr' not in self.kwargs)
		context = super().get_context_data(**kwargs)
		context['popular'] = self.popularList(**kwargs)
		if self.request.user.is_authenticated:
			context['cf'] = self.cfList(**kwargs)
			context['ocf'] = self.ocfList(**kwargs)
		if 'curr' not in self.kwargs:
			if self.request.user.is_authenticated:
				if 'cf' in context :
					context['curr'] = context['cf'][0]
				else:
					context['curr'] = None

			else :
				if 'popular' in context :
					context['curr'] = context['popular'][0]
				else:
					context['curr'] = None
		else:
			context['curr'] = Song.objects.get(pk=self.kwargs['curr'])
		# raise Exception(type(context['curr']))
		return context

	def popularList(self,**kwargs):
		# function to return most popular songs based on listen count 
		# from Music.models import Song,Record
		# raise Exception ( self.kwargs['curr'])
		if 'curr' not in self.kwargs:
			songs = Song.objects.all()
		else :
			songs = Song.objects.exclude(pk__exact=self.kwargs['curr'])
		songs_list = [x for x in songs]
		count = [[songs_list.index(x),0] for x in songs]
		# dic = { x:0 for x in songs}
		# raise Exception(dic)
		if 'curr' not in self.kwargs:
			records = Record.objects.all()
		else:
			records = Record.objects.exclude(song_id__exact=self.kwargs['curr'])
		for x in records:
			count[songs_list.index(x.song_id)][1] = count[songs_list.index(x.song_id)][1]+1
		

		import operator
		sorted_dic = sorted(count, key=operator.itemgetter(1), reverse=True)
		
		# raise Exception(sorted_dic)
		lst = [ songs_list[x[0]]  for x in sorted_dic  ]
		from django.core import serializers
		data = serializers.serialize('json', lst[:10], fields=('song_id','song_name'))
		return lst
		# return HttpResponse( data )#JsonResponse(lst,safe=False) )



	def cfList(self,**kwargs):
		# not working properly 
		# predicts completely random songs
		# maybe more training data is required
		from django.contrib.auth import get_user_model
		import numpy as np
		if 'curr' not in self.kwargs:
			songs_list = [x for x in Song.objects.all()]
		else:
			songs_list = [x for x in Song.objects.exclude(pk__exact=self.kwargs['curr'])]
		users_list = [x for x in get_user_model().objects.all()]
		is_rated = lambda s,u: Record.objects.filter(song_id=s,user_id=u).exists()
		np_rated = np.array([ [ is_rated(s,u)  for u in users_list] for s in songs_list] )
		np_cfmat = np.array([ [rate(s,u) for u in users_list] for s in songs_list] ) # rate function calculates the rating using history of each user
		# raise Exception(np_cfmat)
		
		# ---------------------------------------------------------------- 

		# from sklearn.metrics.pairwise import pairwise_distances as dist
		# user_similarity = dist(np_cfmat, metric='cosine')
		# item_similarity = dist(np_cfmat.T, metric='cosine')
		# raise Exception(user_similarity)

		# ---------------------------------------------------------------- 
		

		num_features = 5
		features = np.random.randn(len(songs_list),num_features)
		# raise Exception(features)
		theta = np.random.randn(len(users_list),num_features)
		theta, features = grad(np_rated, np_cfmat, songs_list, users_list, theta, features)
		
		user = self.request.user
		index = users_list.index(user)
		predicted_ratings = np.dot(features,theta[index].T)
		# raise Exception((predicted_ratings))
		i=0
		lst = [ [x,y] for x,y in zip(predicted_ratings,songs_list)]
		# raise Exception(lst)
		lst = sorted(lst,reverse=True)
		# raise Exception(lst)
		songs_lst = [s for rating,s in lst]
		return songs_lst

		# raise Exception(songs)
		from django.core import serializers
		data = serializers.serialize('json', songs, fields=('song_id','song_name'))
		# raise Exception(dic)
		return HttpResponse(data )	


	def ocfList(self,**kwargs):
		# from Music.models import Song,Record
		if 'curr' not in self.kwargs:
			return Song.objects.all()[:10]
		else:
			return Song.objects.exclude(pk__exact=self.kwargs['curr'])[:10]
		from django.core import serializers
		data = serializers.serialize('json', Song.objects.all()[:10], fields=('song_id','song_name'))
		# raise Exception(dic)
		return HttpResponse(data )

@login_required
def AddSong(request):
	if request.method == "POST" :
		NewSongForm = AddSongForm(request.POST, request.FILES)

		if NewSongForm.is_valid():
			newsong = Song()
			newsong.song_name = NewSongForm.cleaned_data['song_name']
			newsong.song_file = NewSongForm.cleaned_data['song_file']
			newsong.user_id = request.user
			newsong.save()
	else:
		form = AddSongForm()

	return render(request, 'Music/song_form.html', locals())

def index(request):
	# return render(request, 'Music/index.html' )
	return HttpResponse("inside Music(RecSys)")

def updateSongs(request):
	param = request.GET.get('q','')
	if(param=="optimised"):
		return optimisedList(request=request)
	elif(param == "cf"):
		return cfList(request=request)
	else :
		return popularList(request=request)
	

def saveNewSongs(request):
	import os
	BASE_DIR = os.path.dirname(os.path.dirname(__file__))
	# return HttpResponse("inside Music(trendy)")
	files = os.listdir(os.path.join(BASE_DIR, "static/Music/Songs/"))
	#dic = { str(x):x for x in files}
	count=0
	from Music.models import Song
	for x in files:
		if(Song.objects.filter(song_name=x).count()==0):
			s = Song(song_name=x)
			s.save()
			count=count+1
		else:
			pass
			# raise Exception(x)
	# raise Exception(dic)
	return HttpResponse("recorded "+str(count)+" songs" )


def record(request):
	if 'song_id' in request.POST and 'per' in request.POST and 'next_song' in request.POST:
		# from Music.models import Record,Song
		# from login.models import User
		s = Song.objects.get(song_id=request.POST['song_id'])
		next_song = Song.objects.get(song_id=request.POST['next_song'])
		from accounts.models import User
		u = User.objects.get(pk=request.user.pk)
		r = Record(song_id=s, user_id=u, song_name=s.song_name,next_song=next_song,percent_played=float(request.POST['per']) )
		r.save()
		# return HttpResponse("all found")
	else :
		return HttpResponse("Invalid Data")

	return HttpResponse("recorded "+str(s) )

def suggestNext(request):
	if 'user' in request:
		# User Specific Suggestion for next Song
		return HttpResponse("Suggestions coming soon..." )
	else:
		# Popularity based Suggestion for next song 
		return HttpResponse("Personalised Suggestions coming soon..." )



def rate(s,u):
	""" Function to give rating to songs based on previous history of the user """
	from Music.models import Record
	# unknown_song = True
	rating = 0
	count = 0
	for r in Record.objects.filter(user_id=u,song_id=s):
		count = count + 1;
		rating = rating + r.percent_played/100
		# unknown_song=False

	# if(unknown_song == True):
		# return -1
	# else:
	if(count==0):
		return 0
	else:
		return (rating / count)

def grad(np_rated, np_cfmat, songs_list, users_list, theta, features):
	""" Function for gradient descent used in Collaborative filtering """

	import numpy as np
	alpha = 0.5
	# raise Exception(theta.shape[1])
	for k in range(theta.shape[1]):
		# print(k)
		del_x = 0
		del_t = 0
		for i in range(len(songs_list)):
			for j in range(len(users_list)):
				if(np_rated[i][j]):
					del_x = del_x + (np.dot(features[i],theta[j].T) - np_cfmat[i][j]) * features[i][k] 
					del_t = del_t + (np.dot(features[i],theta[j].T) - np_cfmat[i][j]) * theta[j][k] 
		features[:,k] = features[:,k] - alpha * del_x
		theta[:,k] = theta[:,k] - alpha * del_t
		# raise Exception(features[:][0])
	# raise Exception(theta)
	return (theta, features)
