from re import match as reMatch
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import user_passes_test, login_required
from join.models import MyUser, MyUserProfile
from django.conf import settings
from frutonp.utils import getCaptcha

def not_logged_in(request):
    return not request.is_authenticated

def check(request):
    return HttpResponse()

@user_passes_test(not_logged_in, 'home')
def signup(request):
    if request.POST:
        email = request.POST.get('email')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        password = request.POST.get('pass')
        confPass = request.POST.get('confPass')
        recaptcha = request.POST.get('g-recaptcha-response')
        result = getCaptcha(recaptcha)
        err = {}
        
        if result['success'] == False:
            err = " "
            messages.error(request, "Recaptcha is not verified. Try again!!!")

        if len(name) > 4 and len(name) < 48:
            if reMatch('^[a-zA-Z-_ ]+$', name) is None:
                err['name'] = "Invalid name pattern"
        else:
            err['name'] = "Must be more than 4 characters"

        if not (len(phone)==10 and reMatch('^\d+$', phone)):
            err['phone'] = "Phone number must be of 10 numbers"

        if reMatch('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email):
            try:
                user = MyUser.objects.get(email=email)
                err['email'] = "Email already exists"
            except:
                pass
        else:
            err['email'] = "Invalid email pattern"

        if password==confPass:
            if reMatch('^(?=.*[a-z])(?=.*[0-9])(?=.{8,})', password) is None:
                err['pass'] = "Password must be at least 8 characters with lower characters and numbers"
        else:
            err['pass'] = "Password does not match"

        if len(err) == 0:
            user = MyUser.objects.create_user(email=email, name=name, password=password, phone1=phone)
            auth_login(request, user)
            messages.success(request, 'Your account is created successfully.')
            messages.info(request, 'Please check your email to verify your account')
            return redirect('home')
        
        return render(request, 'join/signup.html', {'err': err})
        
    else:
        err = {}
        return render(request, 'join/signup.html', {'err': err})

@user_passes_test(not_logged_in, 'home')
def login(request):
    if request.POST:
        email=request.POST.get('email')
        password = request.POST.get('pass')
        user = authenticate(email=email, password=password)
        if user is None:
            messages.error(request, "Incorrect username or password")
            return render(request, 'join/login.html', {'email': email})

        if request.POST.get('remember_me') is None:
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE  = True
        else:
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE  = False

        auth_login(request, user)
        messages.success(request, "Logged in successfully")
        return redirect('home')
    else:
        return render(request, 'join/login.html')

def logout(request):
    try:
        logout = request.POST['logout']
        auth_logout(request)
        messages.success(request, "Logged out successfully")
        return redirect('login')
    except:
        messages.error(request, "Could not complete logout")
        return redirect('home')

def ajax_email(request):
    if request.POST:
        email = request.POST.get('em_ok_lkng_of')
        try:
            user = MyUser.objects.get(email=email)
            return JsonResponse({"status": "true"})
        except MyUser.DoesNotExist:
            return JsonResponse({"status": "false"})
    return redirect('signup')

