from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Story
from .forms import StoryForm


def story_list(request):
    stories = Story.objects.all().order_by('-created_at')

    return render(request, 'stories/story.html', {
        'stories': stories,
    })


def story_create(request):

    if request.method == 'POST':

        form = StoryForm(request.POST, request.FILES)

        if form.is_valid():

            story = form.save(commit=False)

            user = User.objects.first()

            story.user = user

            story.save()

            return redirect('stories:story_list')

    else:

        form = StoryForm()

    return render(request, 'stories/story_create.html', {
        'form': form,
    })
def story_delete(request, story_id):

    story = get_object_or_404(Story, id=story_id)

    story.delete()

    return redirect('stories:story_list')