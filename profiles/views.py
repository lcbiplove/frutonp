import os
import re
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from join.models import MyUser, MyUserProfile, ProfilePicForm
from posts.models import Post
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.conf import settings
from django.utils import timezone

MAX_POST_LOAD = 20

def index(request, id=None):
    if id is None:
        if request.user.is_authenticated:
            id = request.user.id
        else:
            raise Http404()
    
    user_id = request.user.id
    user_from_id = get_object_or_404(MyUser, pk=id)
    profile_from_id = get_object_or_404(MyUserProfile, myuser_id=id)
    return render(request, 'profiles/profile.html', {
        'myuser': user_from_id,
        'my_profile': profile_from_id,
        'is_authorized': user_id==user_from_id.id and True or False,
        'max_post': MAX_POST_LOAD,
    })

def profilePost(request, id=None):
    if id is None:
        if request.user.is_authenticated:
            id = request.user.id
        else:
            raise Http404()

    if request.is_ajax():
        user = get_object_or_404(MyUser, pk=id)
        no_of_obj = int(request.POST.get("no"))
        posts = user.post_set.all()[MAX_POST_LOAD*no_of_obj:MAX_POST_LOAD*(no_of_obj+1)]
        obj_finished = False
        if posts.count() == 0:
            return JsonResponse({"full_load": True})
        elif posts.count() < MAX_POST_LOAD:
            obj_finished = True

        return render(request, 'profiles/profile-post.html', {
            'posts': posts,
            'obj_finished': obj_finished
        })
    raise Http404()

@login_required
def changeName(request):
    render_template = 'profiles/change-name.html'
    status = {}
    status['wait'] = True
    is_ajax = False
    if request.is_ajax():
        is_ajax = True
        render_template = 'profiles/change-name_ajax.html'
    if request.POST:
        name = request.POST.get('name')
        password = request.POST.get('pass')
        name_updated = request.user.name_updated
        
        if check_password(password, request.user.password):
            if len(name) > 4 and len(name) < 48 and re.match('^[A-Za-z]+([-_ ][A-Za-z]+)*$', name):
                if name_updated is not None:
                    try:
                        days = int(str(timezone.localtime() - name_updated).split()[0])
                    except:
                        days = 0

                    if days < 45:
                        error = "You updated your name %s days ago." % (days)
                        if is_ajax:
                            status['error'] = error
                            status['wait'] = False
                        else:
                            messages.error(request, error)
                        days = False
                    else:
                        days = True
                else:
                    days = True
                                
                if days:
                    user = get_object_or_404(MyUser, pk=request.user.id)
                    user.name = name
                    user.name_updated = timezone.now()
                    user.save(update_fields=['name', 'name_updated'])
                    mssg = "Your name updated succesfully."
                    if is_ajax:
                        status['success'] = mssg
                    else:
                        messages.success(request, mssg)
            else:
                error = "Invalid name pattern entered."
                if is_ajax:
                    status['error'] = error
                else:
                    messages.error(request, error)
        else:
            error = "Password doesn't match."
            if is_ajax:
                status['error'] = error
            else:
                messages.error(request, error)
        if is_ajax:
            return JsonResponse(status)
        return redirect('profile')
        
    return render(request, render_template)

@login_required
def changePhone(request):
    render_template = 'profiles/change-phone.html'
    status = {}
    status['wait'] = True
    is_ajax = False
    if request.is_ajax():
        render_template = 'profiles/change-phone_ajax.html'
        is_ajax = True
    if request.POST:
        phone = request.POST.get('phone')
        password = request.POST.get('pass')
        phone_updated = request.user.phone_updated
        
        if check_password(password, request.user.password):
            if len(phone) == 10 and re.match('^\d+$', phone):
                if phone_updated is not None:
                    try:
                        days = int(str(timezone.localtime() - phone_updated).split()[0])
                    except:
                        days = 0

                    if days < 15:
                        error = "You updated your phone %s days ago." % (days)
                        if is_ajax:
                            status['error'] = error
                            status['wait'] = False
                        else:
                            messages.error(request, error)
                        days = False
                    else:
                        days = True
                else:
                    days = True
                                
                if days:
                    user = get_object_or_404(MyUser, pk=request.user.id)
                    user.phone1 = phone
                    user.phone_updated = timezone.now()
                    user.save(update_fields=['phone1', 'phone_updated'])
                    mssg = "Your phone changed succesfully."
                    if is_ajax:
                        status['success'] = mssg
                    else:
                        messages.success(request, mssg)
            else:
                error = "Invalid phone pattern entered."
                if is_ajax:
                    status['error'] = error
                else:
                    messages.error(request, error)
        else:
            error = "Password doesn't match."
            if is_ajax:
                status['error'] = error
            else:
                messages.error(request, error)
        if is_ajax:
            return JsonResponse(status)

        return redirect('profile')
    return render(request, render_template)


@login_required
def changePassword(request):
    render_template = 'profiles/change-password.html'
    status = {}
    status['wait'] = True
    is_ajax = False
    if request.is_ajax():
        render_template = 'profiles/change-password_ajax.html'
        is_ajax = True
    if request.POST:
        oldPassword = request.POST.get('oldPassword')
        newPass = request.POST.get('newPass')
        confPass = request.POST.get('confPass')
        password_updated = request.user.password_updated
        response = redirect('changePassword')

        if not request.user.is_activated:
            error = "You have to verify email to change your password."
            if is_ajax:
                status['redirect'] = True
            else:
                messages.error(request, error)
                return redirect('profile')
        
        if check_password(oldPassword, request.user.password):
            if newPass == confPass:
                if re.match('^(?=.*[a-z])(?=.*[0-9])(?=.{8,})', newPass):
                    response = redirect('profile')
                    user = get_object_or_404(MyUser, pk=request.user.id)
                    user.set_password(newPass)
                    user.password_updated = timezone.now()
                    user.save(update_fields=['password', 'password_updated'])
                    update_session_auth_hash(request, user)
                    mssg = "Password changed succesfully."
                    if is_ajax:
                        status['redirect'] = True
                    messages.success(request, mssg)
                else:
                    error = "Password must be at least 8 characters with lower characters and numbers."
                    if is_ajax:
                        status['error'] = error
                    else:
                        messages.error(request, error)
            else:
                error = "Two passwords does not match."
                if is_ajax:
                    status['error'] = error
                else:
                    messages.error(request, error)
        else:
            error = "Wrong password entered."
            if is_ajax:
                status['error'] = error
            else:
                messages.error(request, error)
        if is_ajax:
            return JsonResponse(status)
            
        return response
    return render(request, render_template)
    
@login_required(login_url='login')
def changePhoneLocDesc(request):
    render_template = 'profiles/change-phone-loc-desc.html'
    status = {}
    status['wait'] = True
    is_ajax = False
    if request.is_ajax():
        render_template = 'profiles/change-phone-loc-desc_ajax.html'
        is_ajax = True

    if request.POST:
        is_pure_number = False
        phone2 = request.POST.get('phone2')
        desc = (request.POST.get('description')).strip()
        location = request.POST.get('location')
        password = request.POST.get('password')
        user = request.user
        actual_pw = user.password
        if (len(phone2)==10 and re.match('^\d+$', phone2) or len(phone2)==0):
            is_pure_number = True
        
        if check_password(password, actual_pw):
            if is_pure_number:
                profile = MyUserProfile(id=user.myuserprofile.id, myuser=user, phone2=phone2, location=location, desc=desc, pp=user.myuserprofile.pp,)
                profile.save()
                mssg = "Profile updated successfully!!!"
                if is_ajax:
                    status['success'] = mssg
                else:
                    messages.success(request, mssg)
                    return redirect('profile')      
            else:
                error = "Phone should contain 10 numbers"
                if is_ajax:
                    status['error'] = error
                else:
                    messages.error(request, error)          
        else:
            error = "Wrong password entered."
            if is_ajax:
                status['error'] = error
            else:
                messages.error(request, error)
        
        my_profile = {
            'phone2': phone2,
            'desc': desc,
            'location': location,
        } 
        if is_ajax:
            return JsonResponse(dict(my_profile, **status))
        return render(request, render_template, {
            'my_profile': my_profile,            
        })
    
    id = request.user.id
    user_id = request.user.id
    user_from_id = get_object_or_404(MyUser, pk=id)
    profile_from_id = get_object_or_404(MyUserProfile, myuser_id=id)
    return render(request, render_template, {
        'my_profile': profile_from_id,
    })

@login_required(login_url='login')
def uploadPP(request, id=None):
    if request.POST:
        pp = ProfilePicForm(request.POST, request.FILES)
        my_profile = request.user.myuserprofile
        if pp.is_valid():
            pp=get_object_or_404(MyUserProfile, pk=my_profile.id)
            pp.pp = request.FILES.get('pp')
            pp.save(update_fields=['pp'])
            messages.success(request, "Uploaded successfully.")
    return redirect('profile')

@login_required(login_url='login')
def deletePP(request, id=None):
    if request.POST and request.POST.get('pp') == "//":
        id = request.user.id
        my_profile = request.user.myuserprofile
        pp=get_object_or_404(MyUserProfile, pk=my_profile.id)
        if pp.pp != MyUserProfile.default_pp:
            # pp.pp.delete(False)
            pp.pp = MyUserProfile.default_pp
            pp.save(update_fields=['pp'])
    return redirect('profile')

