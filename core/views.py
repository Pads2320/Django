from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.urls import reverse_lazy

# Custom login view
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')  # Redirect to home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

# Home view (this is where the user will go after logging in)
@login_required
def home(request):
    return render(request, 'core/home.html')  # You can customize this view as needed

# Create your views here.
def home(request):
    return render(request, 'core/home.html')  # Render an HTML template

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            return redirect("login")  # Redirect to the login page
    else:
        form = CustomUserCreationForm()
    
    return render(request, "core/register.html", {"form": form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Automatically set the logged-in user as the author
            post = form.save(commit=False)
            post.author = request.user  # Set the logged-in user as the author
            post.save()
            return redirect('post_list')  # Redirect to the list of posts
    else:
        form = PostForm()

    return render(request, 'core/create_post.html', {'form': form})

def post_list(request):
    posts = Post.objects.all()  # Retrieve all posts from the database
    return render(request, 'core/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'core/post_detail.html', {'post': post})

def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'core/update_post.html', {'form': form})

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'core/delete_post.html', {'post': post})

class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'core/post_edit.html'
    success_url = '/post_detail/'  # Redirect after updating  
    
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('post_detail')
    template_name = 'core/post_confirm_delete.html'      