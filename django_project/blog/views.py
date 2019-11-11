from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post


##
## function based view appraoch
## this would do the same thing as PostListView
##
# def home(request):
# 	context = {
# 		'posts': Post.objects.all()
# 	}
# 	return render(request, 'blog/home.html', context)

##
## class-based view approach
##
class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'

	# sort posts newest to oldest
	ordering = ['-date_posted']

class PostDetailView(DetailView):
	model = Post

# LoginRequiredMixin makes it so that a user who isn't logged in can't access 
# the page to create a view
class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']

	# these methods are overriding methods in the classes they inherited
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()

		# users can only update their own posts
		return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()

		# users can only update their own posts
		return self.request.user == post.author

def about(request):
	return render(request, 'blog/about.html', {'title': 'About'})
