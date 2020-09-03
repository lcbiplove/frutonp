from random import randint
from .models import NotifClick
from posts.models import Post

def cookie_law_processors(request):
    try:
        cookie = request.COOKIES['__ck_law__']
        cookie = True
    except KeyError:
        cookie = False
    rand_int = randint(0, 100000000)
    return {'cookie_law': cookie, 'rand_int': rand_int}

def notif_nums(request):
    try:
        notif = NotifClick.objects.get(myuser=request.user)
        num = notif.new_count
        yes_no = num>0 and "yes" or "no"
        return {'notif_num': num, "yes_no": yes_no}
    except:
        return {'notif_num': "", "yes_no": "no"}

def veg_or_fruit_for_category(request):
    vegs = Post.VEG
    fruits = Post.FRUIT
    return {'cat_vegs': vegs, 'cat_fruits': fruits}