import os
import tempfile

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .services.ocr_service import extract_nutrition
from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm

# Create your views here.
def main(request):
    posts = Post.objects.all()

    search_txt = request.GET.get('search_txt')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if search_txt:
        posts = posts.filter(title__icontains=search_txt)  # 대소문자 구분 없이 검색
    
    try:
        if min_price:
            posts = posts.filter(price__gte=int(min_price))
        if max_price:
            posts = posts.filter(price__lte=int(max_price))
    except (ValueError, TypeError):
        pass  # 필터를 무시하되, 기존 검색 필터를 유지

    context = {
        'posts': posts,
        'search_txt': search_txt,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'posts/list.html', context=context)

def create(request):
    if request.method == 'GET':
        form = PostForm()
        context = { 'form': form }
        return render(request, 'posts/create.html', context=context)
    else:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/')

def detail(request, pk):
    target_post = Post.objects.get(id = pk)
    context = { 'post': target_post }
    return render(request, 'posts/detail.html', context=context)

def update(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'GET':
        form = PostForm(instance=post)
        context = {
            'form': form, 
            'post': post
        }
        return render(request, 'posts/update.html', context=context)
    else:
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return redirect('posts:detail', pk=pk)

def delete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('/')

@require_POST
def analyze_nutrition(request):
    nutrition_image = request.FILES.get('nutrition_image')

    if not nutrition_image:
        return JsonResponse(
            {
                'success': False,
                'error': '영양성분 이미지를 선택해주세요.',
            },
            status=400,
        )

    allowed_types = [
        'image/jpeg',
        'image/png',
        'image/webp',
    ]

    if nutrition_image.content_type not in allowed_types:
        return JsonResponse(
            {
                'success': False,
                'error': 'JPG, PNG, WEBP 이미지만 업로드할 수 있습니다.',
            },
            status=400,
        )

    temp_path = None

    try:
        suffix = os.path.splitext(nutrition_image.name)[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:
            for chunk in nutrition_image.chunks():
                temp_file.write(chunk)

            temp_path = temp_file.name

        nutrition = extract_nutrition(temp_path)

        return JsonResponse(
            {
                'success': True,
                'calories': nutrition.get('calories'),
                'carbohydrates': nutrition.get('carbohydrates'),
                'protein': nutrition.get('protein'),
                'fat': nutrition.get('fat'),
                'ocr_text': nutrition.get('ocr_text', ''),
            }
        )

    except Exception as error:
        import traceback

        print('OCR 오류:', error)
        traceback.print_exc()

        return JsonResponse(
            {
                'success': False,
                'error': f'이미지를 분석하지 못했습니다: {error}',
            },
            status=500,
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)