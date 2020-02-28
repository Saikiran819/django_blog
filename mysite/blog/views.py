from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Post
from django.views.generic import (
	ListView, 
	DetailView,
	CreateView,
	DeleteView,
	UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

"""
posts = [
			{
			'author' : "Sai Kiran",
			'title'  : "Blog post 1",
			'date_posted' : 'Feb 5 2020',
			'content' : 'First blog post!'
			},
			{
			'author' : "Sai Ki",
			'title'  : "Blog post 2",
			'date_posted' : 'Feb 6 2020',
			'content' : 'Second blog post!'
			}
]
"""
def home(request):
	context = {
				'posts': Post.objects.all()
	}
	return render(request, 'blog/home.html', context)

def about(request):
	return render(request, 'blog/about.html', {'title' : 'About'}) 

"""
Class based views
"""
class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	ordering = ['-date_posted'] #to display the latest post at top
	
	paginate_by = 2

class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html' #<app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	paginate_by = 2
	
	def get_queryset(self):
		user = get_object_or_404(User, username = self.kwargs.get('username'))
		return Post.objects.filter(author = user).order_by('-date_posted')
			
	
class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		else:
			return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/blog/'
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		else:
			return False

"""
def home(request):
	return HttpResponse('<h1>Blog Home</h1>')

def about(request):
	return HttpResponse('<h1>Blog About</h1>')
	"""