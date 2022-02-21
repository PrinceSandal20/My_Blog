from email.mime import audio
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
	 ListView, 
	 DetailView,
	 CreateView,
	 UpdateView,
	 DeleteView
) 
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Post
#posts = [{'author':'Prince','title':'Blog Post 1','content':'First post content','date_posted':'January 1, 2022'},{'author':'Razab','title':'Blog Post 2','content':'Second post content','date_posted':'January 1, 2022'}]
from verify_email.email_handler import send_verification_email

def home(request):
	context = {
	    #'posts': posts
        'posts' : Post.objects.all()
	}
	return render(request,'home.html',context)

class PostListView(ListView):
	model = Post
	template_name = 'home.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5

class UserPostListView(ListView):
	model = Post
	template_name = 'user_posts.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title','content']

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title','content']

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False	

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False				

def about(request):
	return render(request,'about.html',{'title':'About'})
