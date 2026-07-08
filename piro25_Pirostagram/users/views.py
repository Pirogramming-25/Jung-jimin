from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Follow


def user_search(request):
    keyword = request.GET.get('q', '')

    me = User.objects.first()

    if keyword:
        users = User.objects.filter(username__icontains=keyword)
    else:
        users = User.objects.all()

    following_ids = Follow.objects.filter(
        follower=me
    ).values_list('following_id', flat=True)

    return render(request, 'users/user_search.html', {
        'users': users,
        'keyword': keyword,
        'following_ids': following_ids,
    })

def follow_user(request, user_id):

    me = User.objects.first()

    target = get_object_or_404(User, id=user_id)

    if me != target:

        follow = Follow.objects.filter(
            follower=me,
            following=target
        )

        if follow.exists():
            follow.delete()
        else:
            Follow.objects.create(
                follower=me,
                following=target
            )

    return redirect('users:user_search')