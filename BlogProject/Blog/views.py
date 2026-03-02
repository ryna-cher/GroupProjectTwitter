from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import MyUserCreationForm
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


def index(request):
    if request.method == 'POST' and request.user.is_authenticated:
        text = request.POST.get('text')
        image = request.FILES.get('image')
        if text:
            Post.objects.create(author=request.user, text=text, image=image)
            return redirect('index')

    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'posts': posts})


def register(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = MyUserCreationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    user = request.user

    posts = user.posts.all().order_by('-created_at')

    context = {
        'profile_user': user,
        'posts': posts
    }

    return render(request, 'profile.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    comments = post.comments.all().order_by('created_at')

    context = {
        'post': post,
        'comments': comments
    }

    return render(request, 'post_detail.html', context)

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('index')


@login_required
def add_comment(request, pk):

    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        text = request.POST.get('text')

        if text:
            Comment.objects.create(
                post=post,
                author=request.user,
                text=text
            )

    return redirect('post_detail', pk=pk)