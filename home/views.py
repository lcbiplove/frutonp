from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import datetime
from django.utils import timezone
from posts.models import Post, Photo, PostView
from join.models import MyUser
from .models import NotifClick, Notif
from django.db.models import Q, Count

NOTIF_COUNT = 15
""" If you change this, might need to change nav_all__.js """
TAB_CONST = {
    'veg': 'vegetable',
    'fruit': 'fruit',
    'loc': 'location',
    'users': 'name',
}
SORT_BY_CONST = {
    'newest': 'new',
    'most_viewed': 'views',
    'cheapest': 'value',
}
NUM_OF_POST_AT_BEGINING = 10

def home(request):
    veg_posts = Post.objects.filter(foodType__in=Post.VEG)[:NUM_OF_POST_AT_BEGINING]
    fruit_posts = Post.objects.filter(foodType__in=Post.FRUIT)[:NUM_OF_POST_AT_BEGINING]
    return render(request, 'home/home.html', {
        'veg_posts': veg_posts,
        'fruit_posts': fruit_posts,
    })

''' Reload notification click to 0 '''
def reloadNotif(user):
    notif = NotifClick.objects.get(myuser=user)
    notif.new_count = 0
    notif.save(update_fields=['new_count'])

@login_required
def showNotif(request):
    if request.POST and request.is_ajax():
        page_no = request.GET.get('page', 1)
        total_notifs = Notif.objects.filter(notif_click__myuser=request.user).count()
        if page_no != 1 or page_no != '1':
            try:
                page_no = int(page_no)

                if total_notifs <= (page_no-1)*NOTIF_COUNT:
                    return JsonResponse({"finished": True})
            except:
                pass
        notifs = Notif.objects.filter(notif_click__myuser=request.user).order_by('-received_at')[NOTIF_COUNT*(page_no-1):NOTIF_COUNT*page_no]
        reloadNotif(request.user)

        return render(request, 'home/show-notif.html', {'notifs': notifs})
    raise Http404()

@login_required
def makeNotifSeen(request, id):
    if request.POST and request.is_ajax():
        notif = get_object_or_404(Notif, pk=id)
        if notif.notif_click.myuser == request.user:
            notif.is_seen = True
            notif.save(update_fields=['is_seen'])
            return JsonResponse({'success': True})
    raise Http404()


def cookieLaw(request):
    response = render(request, 'profile_base.html')
    max_age = 2*365*24*60*60    # 2 year
    expires = datetime.datetime.strftime(timezone.localtime() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie('__ck_law__', 'Accepted', max_age, expires)
    return response

def search(request):
    query = request.GET.get("q")
    tab = request.GET.get("q") is None and 'vegetable' or request.GET.get("q")
    if query == None or len(query) == 0:
        return redirect("home")
    
    return searchQuery(request, query)

def searchQuery(request, query):
    query = query.lower()
    tab = request.GET.get("tab")
    sort_by = request.GET.get("sort-by")
    posts = {}
    if tab == TAB_CONST['veg'] or tab == TAB_CONST['fruit'] or tab == TAB_CONST['loc'] or  tab == TAB_CONST['users']:
        if tab == TAB_CONST['veg']:
            posts = Post.objects.filter(Q(foodType__contains=query), Q(foodType__in=Post.VEG))
        elif tab == TAB_CONST['fruit']:
            posts = Post.objects.filter(Q(foodType__contains=query), Q(foodType__in=Post.FRUIT))
        elif tab == TAB_CONST['loc']:
            posts = Post.objects.filter(location__icontains=query)
        elif tab == TAB_CONST['users']:
            posts = MyUser.objects.filter(name__icontains=query)

        if sort_by and tab != TAB_CONST['users']:
            if sort_by == SORT_BY_CONST['most_viewed']:
                posts = posts.annotate(number_of_views=Count('post_views')).order_by('-number_of_views')
            elif sort_by == SORT_BY_CONST['cheapest']:
                posts = sorted(posts, key=lambda obj: obj.priceToWeightRatio())
    else:
        fruit = Post.objects.filter(Q(foodType__contains=query), Q(foodType__in=Post.FRUIT))
        veg = Post.objects.filter(Q(foodType__contains=query), Q(foodType__in=Post.VEG))
        loc = Post.objects.filter(location__icontains=query)
        name = MyUser.objects.filter(name__icontains=query)
        if veg.count() > fruit.count() and veg.count() > loc.count() and veg.count() > name.count():
            posts = veg
            tab = TAB_CONST['veg']
        elif fruit.count() > veg.count() and fruit.count() > loc.count() and fruit.count() > name.count():
            posts = fruit
            tab = TAB_CONST['fruit']
        elif loc.count() > veg.count() and loc.count() > fruit.count():
            posts = loc
            tab = TAB_CONST['loc']
        elif name.count() > loc.count() and name.count() > veg.count() and name.count() > fruit.count():
            posts = MyUser.objects.filter(name__icontains=query)
            tab = TAB_CONST['users']

    return render(request, 'home/search.html', {
        'posts': posts,
        'tab': tab,
        'query': query,
        'sort_by': sort_by,
        'tab_const': TAB_CONST,
        'sort_by_const': SORT_BY_CONST,
    })