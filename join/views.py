from re import match as reMatch
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import user_passes_test, login_required
from join.models import MyUser, MyUserProfile
from django.conf import settings
from frutonp.utils import getCaptcha, account_activation_token, password_reset_token
from django.core.mail import  EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

def send_verify_email(user, request, isNotAjaxCall=True):
    if not user.is_activated:
        mail_subject = 'Verify your account'
        template_vars = {
            'name': user.name,
            'host_name': (request.is_secure() and "https" or "http") + "://" + get_current_site(request).domain,
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }
        plain_mssg = render_to_string('join/emails/verify_email.txt', template_vars)
        html_mssg = render_to_string('join/emails/verify_email.html', template_vars)
        email = EmailMultiAlternatives(subject=mail_subject, body=plain_mssg, from_email='noreply@frutonp.com', to=[user.email])
        email.attach_alternative(html_mssg, "text/html")
        email.send()
        if isNotAjaxCall:
            messages.info(request, 'Please check your email to verify your account')
    else:
        if isNotAjaxCall:
            messages.info(request, 'Your account is already verified.')

@login_required
def sendActivationEmail(request):
    if request.POST:
        user = request.user
        if request.is_ajax():
            send_verify_email(user, request, False)
            return JsonResponse({'email_sent_for_verification': True})
        else:
            send_verify_email(user, request)
    return redirect(request.GET.get('next', 'home'))

def activate(request, uidb64, token):
    mssg = {}
    mssg['success'] = False
    mssg['message'] = 'Invalid Link. Could not verify your email.'
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if user.is_activated:
            mssg['message'] = 'Your email is already verified.'
        else:
            auth_login(request, user)
            mssg['message'] = 'Congratulations, your email is now verified.'
        user.is_activated = True
        user.save()
        mssg['success'] = True
    
    return render(request, 'join/email_activation.html', mssg)

def not_logged_in(request):
    return not request.is_authenticated

def check(request):
    return HttpResponse()

def passwordResetConfirm(request, uidb64, token):
    mssg = {}
    mssg['success'] = False
    mssg['message'] = 'Invalid Link. Try again!!!'
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
    if user is not None and password_reset_token.check_token(user, token):
        if request.POST:
            newPass = request.POST.get('password')
            confPass = request.POST.get('confPass')
            if reMatch('^(?=.*[a-z])(?=.*[0-9])(?=.{8,})', newPass):
                user.set_password(newPass)
                user.password_updated = timezone.now()
                user.save(update_fields=['password', 'password_updated'])
                auth_login(request, user)
                messages.success(request, 'Password is saved successfully.')
                return redirect('home')
            else:
                messages.error(request, 'Password must be at least 8 characters with lower characters and numbers.')
        mssg['uidb64'] = uidb64
        mssg['token'] = token
        mssg['success'] = True

    return render(request, 'join/password_reset_confirm.html', mssg)

def passwordReset(request):
    if request.POST:
        email = request.POST.get('email')
        if request.user.is_authenticated:
            email = request.user.email

        if MyUser.objects.filter(email=email).exists():
            user = MyUser.objects.get(email=email)
            mail_subject = 'Reset Your Password'
            template_vars = {
                'name': user.name,
                'host_name': (request.is_secure() and "https" or "http") + "://" + get_current_site(request).domain,
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': password_reset_token.make_token(user)
            }
            plain_mssg = render_to_string('join/emails/reset_pw_email.txt', template_vars)
            html_mssg = render_to_string('join/emails/reset_pw_email.html', template_vars)
            email = EmailMultiAlternatives(subject=mail_subject, body=plain_mssg, from_email='noreply@frutonp.com', to=[user.email])
            email.attach_alternative(html_mssg, "text/html")
            email.send()
            messages.info(request, 'Please check your email to reset password.')
        else:
            messages.error(request, 'Email you entered does not exist. Please, check your email again.')

    return render(request, 'join/password_reset.html')

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
            if reMatch('^[A-Za-z]+([-_ ][A-Za-z]+)*$', name) is None:
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
            send_verify_email(user, request)
            return redirect(request.GET.get('next', 'home'))
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
        return redirect(request.GET.get('next', 'home'))
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
    if request.is_ajax():
        email = request.POST.get('em_ok_lkng_of')
        try:
            user = MyUser.objects.get(email=email)
            return JsonResponse({"status": "true"})
        except MyUser.DoesNotExist:
            return JsonResponse({"status": "false"})
    raise Http404()



