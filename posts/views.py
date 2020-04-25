import re
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from .models import Post, PhotoForm, Photo, PostView, Comment, Reply
from home.models import Notif, NotifClick
from frutonp.utils import add_post_date, getExpireOfCookie, randomToken
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt # Exclude csrf validation
from django.contrib.auth.decorators import login_required

FOOD_TYPE = ['apple', 'banana', 'litchi', 'mango', 'orange', 'bitter-gourd', 'cabbage', 'cauli', 'ladies-finger', 'pumpkin']
QUANTITY = ['kg', '250gm', '200gm', '500gm', '2kg', '5kg', '10kg', '25kg', '50kg', 'quintal']

def index(request, id):    
    post = get_object_or_404(Post, pk=id)
    auth_id = request.user.id
    # If requesting object has already 
    visited = PostView.objects.filter(post=post, user=auth_id) and True or False

    # if not visited add to views
    if not visited:
        post_view = PostView(post=post, user=request.user)
        post_view.save()

    # Total views
    total_views = PostView.objects.filter(post=post).count()

    return render(request, "posts/post.html", {'post': post, 'views': total_views})

@login_required
@csrf_exempt
def selectThumbnail(request):
    """ To show thumbnail select page
        
        Limitations: Session of key name, '__set__th__', should have 32 length random value and expire date(30 minutes) separated by '///' 
    """
    x = request.session.get('__set__th__')
    x = x.split('///')
    expire = timezone.datetime.strptime(x[1], "%a, %d-%b-%Y %H:%M:%S GMT")
    current = timezone.make_naive(timezone.localtime())
    if len(x[0])==32 and expire>current and request.POST:
        post = Post.objects.filter(myuser=request.user).last()
        data = {}
        thumbnail = request.POST.get('thumbnail')
        if thumbnail:
            if thumbnail.startswith('post/'):
                post.thumbnail = thumbnail
                post.save(update_fields=['thumbnail']) 
                data['success'] = True
            else:
                data['success'] = False
                
            return JsonResponse(data)
        return render(request, 'posts/select_thumbnail.html', {'post': post})
    raise Http404()

@login_required
def addPost(request):
    err = {}
    if request.POST:
        title = request.POST.get('title')
        desc = (request.POST.get('desc')).strip()
        foodType = request.POST.get('vegetable')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        expire = request.POST.get('expire')  
        phone2 = request.POST.get('phone2')
        location = request.POST.get('location')
        try:
            if price[0]=="-":
                price = price[1:]
            price = int(price)
        except:
            err['price'] = "Price must be in numbers"

        if len(title)==0:
            err['title'] = "Title must be filled"

        if desc == "":
            err['desc'] = "Description must be filled"

        if foodType not in FOOD_TYPE:
            err['foodType'] = "Please select from the given options only"

        if quantity not in QUANTITY:
            err['quantity'] = "Please select from the given options only"

        if expire not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']:
            err['expire'] = "Please select from the given options only."
        else:
            expire = add_post_date(int(expire))

        if len(request.FILES.getlist('photos')) > 5:
            err['photos'] = "Max photo upload is 5"
        
        if not (len(phone2)==10 and re.match('^\d+$', phone2) or len(phone2)==0):
            err['phone2'] = "Phone should contain 10 numbers"


        photoform = PhotoForm(request.POST, request.FILES)
        if len(err)==0:
            if photoform.is_valid():
                data = {}
                post = Post(myuser=request.user, title=title, desc=desc, foodType=foodType, price=price, quantity=quantity, expire=expire, phone2=phone2, location=location)
                post.save()
                # if no file is uploaded us custom null_save() to save default photo
                if request.FILES.get('photos') is None:
                    img = Photo(post=post, photos=None)
                    img.null_save()
                    data['thumb_added'] = True
                else:
                    for i, photo in enumerate(request.FILES.getlist('photos')):
                        img = Photo(post=post, photos=photo)
                        img.save()
                        if i == 0:
                            post.thumbnail = img.photos
                            post.save(update_fields=['thumbnail'])

                    if len(request.FILES.getlist('photos')) == 1:
                        data['thumb_added'] = True
                    else:
                        request.session['__set__th__'] = randomToken(32)+"///"+getExpireOfCookie(30*60)    

                messages.success(request, 'Post added successfully')
                data['success'] = True
                return JsonResponse(data)

        post = {
            'title': title,
            'desc': desc,
            'price': price,
            'location': location,
            'phone2': phone2,
        }
        messages.error(request, 'Post errors!!!')
        return render(request, 'posts/add-post.html', {'err': err, 'post': post})
    else:
        post = {
            'location': request.user.myuserprofile.location,
            'phone2': request.user.myuserprofile.phone2,
        }
        
        return render(request, 'posts/add-post.html', {'err': err, 'post': post})

@login_required
def addComment(request, id):
    result = {}
    result['status'] = False
    if request.POST:
        cm_id = request.POST.get('cm_id')
        user_id = request.user.id
        post= Post.objects.get(pk=id)
        user = request.user
        comment_text = request.POST.get('comment')
        if len(comment_text) != 0:
            if cm_id is None:
                """ New Comment is added """
                comment = Comment(post=post, myuser=user, text=comment_text)
                comment.save()
                result['status'] = True

                if user != post.myuser:
                    notif_click, created = NotifClick.objects.get_or_create(myuser=post.myuser)
                    notif = Notif(notif_click=notif_click, sender=user, post=post, comment=comment)
                    notif.save()
                    
            else:
                """ Comment is editted """
                comment = get_object_or_404(Comment, pk=cm_id)
                if user.id == comment.myuser.id:
                    comment.text = comment_text
                    comment.editted = True
                    comment.save(update_fields=['text', 'editted'])
                    result['edit'] = True
                    result['status'] = True
                    result['text'] = comment.text

            result['id'] = comment.id
    return JsonResponse(result)

@login_required
def addedComment(request, post_id, comment_id):
    user = request.user
    comment = get_object_or_404(Comment, pk=comment_id)
    return render(request, 'posts/added-comment.html', {'comment': comment})

@login_required
def newComment(request, post_id, last_cm_id):
    user = request.user
    post = Post.objects.get(pk=post_id)
    comments = reversed(post.comment.filter(id__gt=last_cm_id).order_by('-commented_at'))
    return render(request, 'posts/new-comments.html', {'comments': comments})

@login_required
def commentOption(request, post_id, comment_id):
    user = request.user
    comment = get_object_or_404(Comment, pk=comment_id)
    return render(request, 'posts/comment-option.html', {'comment': comment})

@login_required
def deleteComment(request, post_id, comment_id):
    result = {}
    result['status'] = False
    if request.POST:
        cm_id = request.POST.get('cm_id')
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user == comment.myuser or request.user == comment.post.myuser:
            if request.user != comment.post.myuser:
                notif_click, created = NotifClick.objects.get_or_create(myuser=comment.post.myuser)
                notif = Notif(notif_click=notif_click, sender=request.user, post=comment.post, comment=comment)
                notif.save()
                
            comment.delete()
            result['status'] = True
            
    return JsonResponse(result)

@login_required
def addReply(request, post_id, comment_id):
    result = {}
    if request.POST:
        cm_id = request.POST.get('cm_id')
        user_id = request.user.id
        comment = get_object_or_404(Comment, pk=cm_id)
        reply_text = request.POST.get('reply')
        if len(reply_text) != 0:
            """ New reply is added """
            reply = Reply(comment=comment, myuser=request.user, text=reply_text)
            reply.save()
            result['id'] = reply.id

            if request.user != reply.comment.post.myuser:
                notif_click, created = NotifClick.objects.get_or_create(myuser=comment.post.myuser)
                notif = Notif(notif_click=notif_click, sender=request.user, post=comment.post, comment=comment)
                notif.save()
            
    return JsonResponse(result)

def addedReply(request, post_id, comment_id, reply_id):
    user = request.user
    reply = get_object_or_404(Reply, pk=reply_id)
    return render(request, 'posts/added-reply.html', {'reply': reply})

def viewReply(request, post_id, comment_id):
    user = request.user
    comments = get_object_or_404(Comment, pk=comment_id)
    replies = comments.reply.all().order_by('replied_at')

    return render(request, 'posts/view-replies.html', {'replies': replies})
    
@login_required
def deleteReply(request, post_id, comment_id, reply_id):
    if request.POST:
        rp_id = request.POST.get('rp_id')
        reply = get_object_or_404(Reply, pk=rp_id)
        if request.user == reply.myuser or request.user == reply.comment.post.myuser:
            reply.delete()
            
    return JsonResponse({'status': True})