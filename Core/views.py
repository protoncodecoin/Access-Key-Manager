from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login
from .tokens import generate_token
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


def signup(request):
    if request.method == "POST":

        # get the user model
        userModel = get_user_model()

        # Retrieve form data
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # validate email
        try:
            existing_user = userModel.objects.get(email=email)

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

        except userModel.DoesNotExist():
            pass

        # validate password match
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("users:signpu")

        if len(password1) < 8:
            messages.error(request, "Password must be least 8 characters long")

        # create user object
        new_user = userModel.objects.create_user(email, password1)
        new_user.is_active = False
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
    userModel = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = userModel.objects.get(pk=uid)

    except (TypeError, ValueError, userModel.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your account has been activated!")
        return redirect("users:login")
    return render(request, "registration/activation_failed.html")
