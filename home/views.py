from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import datetime
from django.utils import timezone
from posts.models import Post, Photo
from .models import NotifClick

# Create your views here.
def home(request):
    all_post = Post.objects.all().order_by('-uploaded_at')
    veg_posts = all_post.filter(category="vegetable")
    fruit_posts = all_post.filter(category="fruit")
    return render(request, 'home/home.html', {
        'veg_posts': veg_posts,
        'fruit_posts': fruit_posts,
    })

def reloadNotif(request):
    notif = NotifClick.objects.get(myuser=request.user)
    notif.new_count = 0
    notif.save(update_fields=['new_count'])
    return redirect("home")

def cookieLaw(request):
    response = render(request, 'profile_base.html')
    max_age = 2*365*24*60*60    # 2 year
    expires = datetime.datetime.strftime(timezone.localtime() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie('__ck_law__', 'Accepted', max_age, expires)
    return response
