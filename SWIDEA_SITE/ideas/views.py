from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Idea, DevTool
from .forms import IdeaForm, DevToolForm

def idea_list(request):
    sort = request.GET.get('sort')

    ideas = Idea.objects.all()

    if sort == 'interest':
        ideas = ideas.order_by('-interest')
    elif sort == 'name':
        ideas = ideas.order_by('title')
    elif sort == 'old':
        ideas = ideas.order_by('id')
    else:
        ideas = ideas.order_by('-id')

    return render(request, 'ideas/idea_list.html', {'ideas': ideas})

def idea_create(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save()
            return redirect('ideas:idea_detail', idea.pk)
    else:
        form = IdeaForm()

    return render(request, 'ideas/idea_form.html', {'form': form})

def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    return render(request, 'ideas/idea_detail.html', {'idea': idea})

def idea_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk)

    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            idea = form.save()
            return redirect('ideas:idea_detail', idea.pk)
    else:
            form = IdeaForm(instance=idea)

    return render(request, 'ideas/idea_form.html', {'form': form})

def idea_delete(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    idea.delete()
    return redirect('ideas:idea_list')

def interest_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    action = request.POST.get('action')

    if action == 'plus':
        idea.interest += 1
    elif action == 'minus':
        idea.interest -= 1

    idea.save()
    return JsonResponse({'interest': idea.interest})

def star_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    idea.is_star = not idea.is_star
    idea.save()
    return redirect('ideas:idea_detail', idea.pk)

def devtool_list(request):
    devtools = DevTool.objects.all()
    return render(request, 'ideas/devtool_list.html', {'devtools': devtools})

def devtool_create(request):
    if request.method == 'POST':
        form = DevToolForm(request.POST)
        if form.is_valid():
            devtool = form.save()
            return redirect('ideas:devtool_detail', devtool.pk)
    else:
        form = DevToolForm()

    return render(request, 'ideas/devtool_form.html', {'form': form})

def devtool_detail(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    ideas = Idea.objects.filter(devtool=devtool)
    return render(request, 'ideas/devtool_detail.html', {
        'devtool': devtool,
        'ideas' : ideas,
    })

def devtool_update(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)

    if request.method == 'POST':
        form = DevToolForm(request.POST, instance=devtool)
        if form.is_valid():
            devtool = form.save()
            return redirect('ideas:devtool_detail', devtool.pk)
    else:
        form = DevToolForm(instance=devtool)

    return render(request, 'ideas/devtool_form.html', {'form': form})

def devtool_delete(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    devtool.delete()
    return redirect('ideas:devtool_list')