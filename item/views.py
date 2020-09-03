from django.shortcuts import render, HttpResponse, Http404
from posts.models import Post

PAGE_SIZE = 24

def get_display_food_choice(value):
    return dict(Post.FOOD_CHOICES).get(value)

def getPostData(page, paramToCompare, isForEachItem=False, foodType='veg'):
    data = {}
    is_finished = False
    if page is not 1:
        try:
            page = int(page)
        except:
            page = 1
    
    if isForEachItem:
        total_count = Post.objects.filter(foodType=paramToCompare).count()
        posts = Post.objects.filter(foodType=paramToCompare)[(page-1)*PAGE_SIZE:page*PAGE_SIZE]
        data['foodType'] = foodType
        data['itemName'] = get_display_food_choice(paramToCompare) 
    else:
        total_count = Post.objects.filter(foodType__in=paramToCompare).count()
        posts = Post.objects.filter(foodType__in=paramToCompare)[(page-1)*PAGE_SIZE:page*PAGE_SIZE]

    if total_count <= page*PAGE_SIZE:
        is_finished = True

    data['page'] = page+1
    data['is_finished'] = is_finished
    data['posts'] = posts
    
    return data

def veg(request):
    page = request.GET.get('page', 1)
    veg_data = getPostData(page, Post.VEG)
    
    return render(request, 'item/veg.html', veg_data)

def fruit(request):
    page = request.GET.get('page', 1)
    fruit_data = getPostData(page, Post.FRUIT)
    
    return render(request, 'item/fruit.html', fruit_data)

def vegName(request, veg_name):
    is_finished = False
    if veg_name not in Post.VEG:
        raise Http404
    else:
        page = request.GET.get('page', 1)
        data = getPostData(page, veg_name, isForEachItem=True)
        return render(request, 'item/each_item.html', data)

def fruitName(request, fruit_name):
    if fruit_name not in Post.FRUIT:
        raise Http404()
    else:
        page = request.GET.get('page', 1)
        data = getPostData(page, fruit_name, isForEachItem=True, foodType='fruit')
        return render(request, 'item/each_item.html', data)