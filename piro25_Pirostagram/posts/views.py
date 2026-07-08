from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .forms import PostForm
from .models import Post, Like, Comment

def main(request):
    posts = Post.objects.all().order_by('-created_at')

    context = {
        'posts': posts,
    }

    return render(request, 'posts/main.html', context)

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            user = User.objects.first()

            if user is None:
                user = User.objects.create_user(username='admin', password='1234')

            post.author = user
            post.save()
            return redirect('posts:main')
    else:
        form = PostForm()

    return render(request, 'posts/post_create.html', {'form':form})

def post_update(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":

        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            return redirect("posts:main")

    else:
        form = PostForm(instance=post)

    return render(request, "posts/post_create.html", {
        "form": form,
    })

def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        post.delete()
        return redirect('posts:main')

    return render(request, 'posts/post_delete.html', {'post': post})

def post_like(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    user = User.objects.first()

    like = Like.objects.filter(post=post, user=user)

    if like.exists():
        like.delete()
    else:
        Like.objects.create(post=post, user=user)

    return redirect('posts:main')

def comment_create(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    user = User.objects.first()

    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            Comment.objects.create(
                post=post,
                user=user,
                content=content
            )

    return redirect('posts:main')

def user_search(request):
    keyword = request.GET.get('q', '')

    if keyword:
        users = User.objects.filter(username__icontains=keyword)
    else:
        users = User.objects.all()

    return render(request, 'users/user_search.html', {
        'users': users,
        'keyword': keyword,
    })