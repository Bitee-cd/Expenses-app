from collections.abc import Callable, Iterable, Mapping
from typing import Any
from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages, auth
from django.core.mail import EmailMessage, send_mail
from django.utils.encoding import force_bytes, force_str,  DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.shortcuts import redirect
from urllib.parse import urlencode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading

# Create your views here.


class EmailThread(threading.Thread):
    def __init__(self, email_subject, email_body, email):
        self.email = email
        self.email_subject = email_subject
        self.email_body = email_body
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.email_subject,
            self.email_body,
            "noreply@example.com",
            [self.email],
            fail_silently=False,
        )


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # Get user data
        # validate
        # create user account
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        context = {
            'fieldValues': request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)

                user.is_active = False
                user.save()

                # path_to_view
                # --get domain
                # --relative url to the verification view
                # --encode uid
                # --token
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                               'uidb64': uidb64, 'token': token_generator.make_token(user)})
                activate_url = 'http://'+domain+link
                email_subject = 'Activate your account'
                email_body = 'Hi ' + user.username + \
                    ' Please use this link to verify your account\n' + activate_url
                # email = send_mail(
                #     email_subject,
                #     email_body,
                #     "noreply@example.com",
                #     [email],
                #     fail_silently=False,
                # )
                EmailThread(email_subject=email_subject,
                            email_body=email_body, email=email).run()
                messages.success(request, 'Account successfully created')
                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')


class UserNameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'username already in use, choose another'}, status=409)
        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'email already in use, choose another'}, status=409)
        return JsonResponse({'email_valid': True})


class VerifiationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                messages.success(request, 'User already activated')
                return redirect('login')

            if user.is_active:
                messages.success(request, 'User already activated')
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as e:
            print('exception', e)
            pass
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        if username and password:

            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome' +
                                     user.username+'You are now logged in ')
                    return redirect('expenses')

                messages.error(
                    request, 'Account is not active, please check your email')
                return render(request, 'authentication/login.html')
            messages.error(
                request, 'Invalid Credentials ,Try again')
            return render(request, 'authentication/login.html')
        messages.error(
            request, 'Please fill all fields')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')


class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')

    def post(self, request):
        email = request.POST['email']
        context = {'values': request.POST}
        if not validate_email(email):
            messages.error(request, 'Please supplyu a valid email ')
            return render(request, 'authentication/reset-password.html', context)

        domain = get_current_site(request).domain
        user = User.objects.filter(email=email).first()
        if user is not None:
            print(user)
            email_contents = {
                'user': user,
                'domain': domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': PasswordResetTokenGenerator().make_token(user)
            }
            link = reverse('reset-user-password', kwargs={
                           'uidb64': email_contents['uid'], 'token': email_contents['token']})
            email_subject = "Reset your password"
            reset_url = 'http://' + get_current_site(request).domain + link
            # email = EmailMessage(
            #     email_subject,
            #     'Hi there, Please clik the link below to reset your password\n ' +
            #     reset_url, [email]

            # )
            email_body = 'Hi there, Please clik the link below to reset your password\n' + reset_url
            # email = send_mail(
            #     email_subject,
            #     email_body,
            #     "noreply@example.com",
            #     [email],
            #     fail_silently=False,
            # )

            EmailThread(email_subject=email_subject,
                        email_body=email_body, email=email).run()
        messages.success(
            request, "We have sent you an email to reset your password")
        return render(request, 'authentication/reset-password.html')


class CompletePasswordRest(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(
                    request, 'Password link is invalid,Please request a new one')
                return render('authentication/reset-password.html')
        except Exception as e:
            pass
        return render(request, 'authentication/set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'authentication/set-new-password.html', context)

        if len(password) < 6:
            messages.error(request, 'Passwords is too short')
            return render(request, 'authentication/set-new-password.html', context)
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        except Exception as e:
            messages.info(request, 'Something went wrong,Try again')
            return render(request, 'authentication/set-new-password.html', context)
