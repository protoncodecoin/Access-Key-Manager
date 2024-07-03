from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from .tokens import generate_token
from django.contrib.auth.models import Group
from django.conf import settings
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.exceptions import ValidationError

from .models import CustomUser


def signup(request):
    if request.method == "POST":

        # Retrieve form data
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # validate email
        try:
            existing_user = CustomUser.objects.get(email=email)

            if existing_user.is_active:
                messages.error(request, "Email already exists!")
                return redirect("users:signup")
            else:
                existing_user.delete()
                messages.error(
                    request,
                    "Account verification wasn't completed for this account.\n\nPlease re-sign up again.",
                )
                return redirect("users:signup")

        except CustomUser.DoesNotExist:
            pass

        # validate password
        if password1 != password2:
            messages.error(request, "Passwords do not matchbb")
            return redirect("users:signup")

        try:
            validate_password(password1)
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect("users:signup")

        # create user object
        user_group = Group.objects.get(name="Personnel")
        new_user = CustomUser.objects.create_user(email, password1)
        new_user.is_active = False
        new_user.groups.add(user_group)
        new_user.save()

        try:
            # Send welcome email
            subject = "Welcome to Micro Finance Inc. Access Key Manager"
            message = "Hello there!\n\nThank you for registering to use the Access Key Manager"
            from_email = settings.EMAIL_HOST_USER
            to_list = [new_user.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)

            # send email confirmation link
            current_site = get_current_site(request)
            email_subject = "Confirm Your Email Address"
            message2 = render_to_string(
                "registration/email_confirmation.html",
                {
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(new_user.pk)),
                    "token": generate_token.make_token(new_user),
                },
            )
            send_mail(email_subject, message2, from_email, to_list, fail_silently=False)

            messages.success(
                request,
                "Your account has been created successfully! Please check your email to confirm your email address and activate your account.",
            )
        except Exception as e:
            messages.error(request, f"Error sending email: {e}")
            return redirect("users:login")

        return redirect("users:login")
    return render(request, "registration/signup.html")


def login_user(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        # if user is active
        if user:
            if user.is_active:
                login(request, user)
                return redirect("key_manager:dashboard")

        messages.error(request, "Invalid username or password provided")
        return redirect("users:login")
    return render(request, "registration/login.html")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = CustomUser.objects.get(pk=uid)

    except (TypeError, ValueError, CustomUser.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your account has been activated!")
        return redirect("users:login")
    return render(request, "registration/activation_failed.html")
