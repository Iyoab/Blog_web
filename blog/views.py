from typing import Optional
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post


def home(request):
    return render(request, 'home/home.html')


def post_list(request):
    posts = Post.objects.all().order_by('-date_posted')
    message = None
    if not posts:
        message = "No posts are available yet."
    context = {'posts': posts, 'message' : message}
    return render(request,'blog/post_list.html', context)


def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk) #Get posts by primary key
    context = {'post': post}
    return render(request,'blog/post_detail.html', context)


def home(request):
    return render(request, 'home/home.html')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class CustomSignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registration_form.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    success_url = reverse_lazy('post_list')
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
 #Redirect to the list view after sucessful post creation


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    success_url = reverse_lazy('post_list') 

    def test_func(self):
        #Ensure the user is the author of the post before allowing editing
        return self.request.user == self.get_object().author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

    def test_func(self):
        #Ensure the user is the author of the post before allowing deletion
        return self.request.user == self.get_object().author