import re
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.core import serializers
from .models import Post, PhotoForm, Photo, PostView, Comment, Reply
from home.models import Notif, NotifClick
from frutonp.utils import add_post_date, getExpireOfCookie, randomToken
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth.decorators import login_required

MAX_COMMENT_LOAD = 10

def index(request, id):    
    post = get_object_or_404(Post, pk=id)
    try:
        auth_id = request.user.id
        # If requesting object has already 
        visited = PostView.objects.filter(post=post, user=auth_id) and True or False

        # if not visited add to views
        if not visited:
            post_view = PostView(post=post, user=request.user)
            post_view.save()
    except:
        pass
    # Total views
    total_views = PostView.objects.filter(post=post).count()

    return render(request, "posts/post.html", {'post': post, 'views': total_views, 'max_comment': MAX_COMMENT_LOAD})

"""
def addPostTest(request):
    title = 'Title'
    desc = '(request.POST.get()).strip()'
    foodType = 'VCA'
    price = 45
    quantity = '250gm'
    expire = 8
    thumbnail = 'post/default/VCF.jpg'
    post = Post(myuser=request.user, title=title, desc=desc, foodType=foodType, price=price, thumbnail=thumbnail, quantity=quantity, expire=expire)
    post.save()
    return HttpResponse("Done")
"""
def postComment(request, id=None):
    if request.is_ajax():
        post = get_object_or_404(Post, pk=id)
        no_of_obj = int(request.POST.get("no"))
        comments = post.comment.all()[MAX_COMMENT_LOAD*no_of_obj:MAX_COMMENT_LOAD*(no_of_obj+1)]
        obj_finished = False
        if comments.count() == 0:
            return JsonResponse({"full_load": True})
        elif comments.count() < MAX_COMMENT_LOAD:
            obj_finished = True

        return render(request, 'posts/post-comment.html', {
            'comments': comments,
            'obj_finished': obj_finished
        })
    raise Http404()

@login_required
def editPost(request, id):  
    err = {}
    post = get_object_or_404(Post, pk=id)
    if post.myuser == request.user:
        if request.is_ajax():
            title = request.POST.get('title')
            desc = (request.POST.get('desc')).strip()
            foodType = request.POST.get('foodType')
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

            if (foodType not in Post.VEG) and (foodType not in Post.FRUIT):
                err['foodType'] = "Please select from the given options only"

            if quantity not in Post.QUANTITY:
                err['quantity'] = "Please select from the given options only"

            if expire not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']:
                err['expire'] = "Please select from the given options only."
            """
            else:
                expire = add_post_date(int(expire))
            """
            
            if not (len(phone2)==10 and re.match('^\d+$', phone2) or len(phone2)==0):
                err['phone2'] = "Phone should contain 10 numbers"

            if len(err)==0:
                data = {}
                json_send = {}
                update_fields = []
                if post.title != title:
                    post.title = title
                    json_send['title'] = title
                    update_fields.append('title')
                if post.desc != desc:
                    post.desc = desc
                    json_send['desc'] = desc
                    update_fields.append('desc')
                if post.price != price:
                    post.price = price
                    json_send['price'] = price
                    update_fields.append('price')
                if post.foodType != foodType:
                    post.foodType = foodType
                    json_send['foodType'] = post.outerFood()
                    update_fields.append('foodType')
                    if post.photos.all().count() == 1:
                        post.thumbnail = f"post/default/{foodType}.jpg"
                        photo = Photo.objects.get(post=post)
                        photo.photos = post.thumbnail
                        json_send['thumbnail'] = post.thumbnail
                        update_fields.append('thumbnail')
                if post.quantity != quantity:
                    post.quantity = quantity
                    json_send['quantity'] = post.quantity
                    update_fields.append('quantity')
                if post.expire != expire:
                    post.expire = expire
                    update_fields.append('expire')
                if post.phone2 != phone2:
                    post.phone2 = phone2
                    json_send['phone2'] = post.phone2
                    update_fields.append('phone2')
                if post.location != location:
                    post.location = location
                    json_send['location'] = post.location
                    update_fields.append('location')
                if json_send:
                    from django.db.models.signals import post_save
                    from django.dispatch import receiver
                    import channels.layers
                    from asgiref.sync import async_to_sync
                    import json

                    channel_layer = channels.layers.get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        f"post_id_{post.id}", {
                            "type": "post_edit_send",
                            "text": json.dumps({'desc': 'post_edit', 'me': request.user.id, 'data': json_send})
                        }
                    )
                try:
                    photo.save(update_fields=['photos'])
                except:
                    pass
                post.save(update_fields=update_fields)
                messages.success(request, 'Post edited successfully')
                data['success'] = True
                return JsonResponse(data)

            return JsonResponse(err)
        else:
            post = get_object_or_404(Post, pk=id)
            loc_n_phn = {
                'location': request.user.myuserprofile.location,
                'phone2': request.user.myuserprofile.phone2,
            }
        return render(request, 'posts/edit-post.html', {'err': err, 'loc_n_phn': loc_n_phn, 'post': post})
    raise Http404()

def editedPost(request, id):
    if request.is_ajax():
        if int(request.POST.get('pid')) is id:
            data = {}
            post = get_object_or_404(Post, pk=id)
            data['title']=post.title
            #posts_serialized = serializers.serialize('json', posts)
            return JsonResponse(data) 

    raise Http404()

@login_required
def deletePost(request):
    data = {}
    if request.is_ajax():
        id = request.POST.get('pid')
        post = get_object_or_404(Post, pk=id)
        post = Post.objects.get(pk=id)
        if post.myuser == request.user:
            post.delete()
            data['status']=True
            return JsonResponse(data)
    raise Http404()
    

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
        post = Post.objects.filter(myuser=request.user).first()
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
    if request.is_ajax():
        title = request.POST.get('title')
        desc = (request.POST.get('desc')).strip()
        foodType = request.POST.get('foodType')
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

        if (foodType not in Post.VEG) and (foodType not in Post.FRUIT):
            err['foodType'] = "Please select from the given options only"

        if quantity not in Post.QUANTITY:
            err['quantity'] = "Please select from the given options only"

        if expire not in Post.EXPIRE:
            err['expire'] = "Please select from the given options only."
        #else:
            #expire = add_post_date(int(expire))

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
            else:
                err['photos'] = "Unable to upload photos"

        return JsonResponse(err)
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
    if request.is_ajax():            
        user = request.user
        comment = get_object_or_404(Comment, pk=comment_id)
        return render(request, 'posts/added-comment.html', {'comment': comment})
    raise Http404()

@login_required
def newComment(request, post_id, last_cm_id):
    if request.is_ajax():
        user = request.user
        post = Post.objects.get(pk=post_id)
        comments = reversed(post.comment.filter(id__gt=last_cm_id).order_by('-commented_at'))
        return render(request, 'posts/new-comments.html', {'comments': comments})
    raise Http404()

@login_required
def commentOption(request, post_id, comment_id):
    if request.is_ajax():
        user = request.user
        comment = get_object_or_404(Comment, pk=comment_id)
        return render(request, 'posts/comment-option.html', {'comment': comment})
    raise Http404()

@login_required
def deleteComment(request, post_id, comment_id):
    result = {}
    result['status'] = False
    if request.POST and request.is_ajax():
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
    raise Http404()

@login_required
def addReply(request, post_id, comment_id):
    result = {}
    if request.POST and request.is_ajax():
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
    raise Http404()

def addedReply(request, post_id, comment_id, reply_id):
    user = request.user
    reply = get_object_or_404(Reply, pk=reply_id)
    return render(request, 'posts/added-reply.html', {'reply': reply})

def viewReply(request, post_id, comment_id):
    if request.is_ajax():
        user = request.user
        comments = get_object_or_404(Comment, pk=comment_id)
        replies = comments.reply.all().order_by('replied_at')

        return render(request, 'posts/view-replies.html', {'replies': replies})
    raise Http404()
    
@login_required
def deleteReply(request, post_id, comment_id, reply_id):
    if request.POST and request.is_ajax():
        rp_id = request.POST.get('rp_id')
        reply = get_object_or_404(Reply, pk=rp_id)
        if request.user == reply.myuser or request.user == reply.comment.post.myuser:
            reply.delete()
        return JsonResponse({'status': True})
    raise Http404()
