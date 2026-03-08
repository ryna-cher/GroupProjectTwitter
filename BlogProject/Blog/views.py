from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import MyUserCreationForm, EditProfileForm
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
    total_likes = sum(post.likes.count() for post in posts)
    total_dislikes = sum(post.dislikes.count() for post in posts)

    context = {
        'profile_user': user,
        'posts': posts,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
    }

    return render(request, 'profile.html', context)


def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.posts.all().order_by('-created_at')
    total_likes = sum(post.likes.count() for post in posts)
    total_dislikes = sum(post.dislikes.count() for post in posts)

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
    }

    return render(request, 'profile.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(parent__isnull=True).order_by('created_at')

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
def toggle_dislike(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    if user in post.dislikes.all():
        post.dislikes.remove(user)
    else:
        post.dislikes.add(user)
        if user in post.likes.all():
            post.likes.remove(user)
    return redirect(request.META.get('HTTP_REFERER', 'index'))


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


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=user)

    context = {'form': form}
    return render(request, 'edit_profile.html', context)


@login_required
def delete_profile(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('index')
    return render(request, 'delete_profile.html')


@login_required
def add_comment_reply(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    parent_comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        text = request.POST.get('text')
        Comment.objects.create(
            post=post,
            author=request.user,
            text=text,
            parent=parent_comment
        )
    return redirect('post_detail', pk=post_id)