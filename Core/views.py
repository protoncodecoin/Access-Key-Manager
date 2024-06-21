from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout

from .tokens import generate_token


def user_login(request):
    """
    Authenticate the user with the provided email and password and redirect the user to the dashboard
    """
    User = get_user_model()
    if request.method == "POST":
        email:str = request.POST.get("email")
        password:str = request.POST.get("password")

        # check if a user exist with the given email
        if not User.objects.filter(email=email).exists():
            messages.error(request, "Invalid credentials provided")
            return redirect("users:login")
        
        # Authenticate the user with the provided email
        user = authenticate(email=email, password=password)

        if user is None:
            # Display an error message
            messages.error(request, "No account Found. Please register for an account.")
            return redirect("users:login")
        else:
            # log in the user and redirect the user to the dashboard
            login(request, user)
            messages.success(request, "Welcome!")
            return redirect("key_manager:dashboard")
    return render(request, "registration/login.html")



def signup(request):
    """
    Create user account with the provided email and password
    """
    if request.method == "POST":
        email:str = request.POST.get("email")
        password1:str = request.POST.get("password1")
        password2:str = request.POST.get("password2")

        # Instantiate the user model
        User = get_user_model()

        # Validate email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect("users:signup")
        
        # Validate password match
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("users:signup")
        
        # validate password strength
        if not password1.isalnum:
            messages.error(request, "Provide a strong password")
            return redirect("users:signup")
        
        # Create user object
        newuser = User.objects.create_user(email, password1)
        newuser.is_active = False   # Disable account until email confirmation
        newuser.save()

        # send welcome email
        subject = "Welcome to Micro-Focus Inc. Access Key Manager."
        message = f"Thamk you for registering"
        from_email = settings.EMAIL_HOST_USER
        to_list = [newuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # send email confirmation link
        current_site = get_current_site(request)
        email_subject = "Confirm Your Email Address"
        messages2 = render_to_string('registration/email_confirmation.html', {
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(newuser.pk)),
            'token': generate_token.make_token(newuser)
        })
        email = EmailMessage(
            email_subject,
            messages2,
            settings.EMAIL_HOST_USER,
            [newuser.email]
        )
        send_mail(email_subject, messages2, from_email, to_list, fail_silently=True)
        messages.success(request, "Your account has been created successfully! Please check your email to confirm your email address and activate your account.")
        return redirect("users:login")
    return render(request, "registration/signup.html")


def activate(request, uidb64, token):
    """
    Activate the user's account after clicking on the verification link
    """
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your account has been activated!")
        return redirect('users:login')
    else:
        return render(request, "registration/activatation_failed.html")